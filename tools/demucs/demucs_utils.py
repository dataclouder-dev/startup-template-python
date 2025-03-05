import tempfile
from pathlib import Path

import torch
from demucs.apply import apply_model
from demucs.audio import AudioFile, save_audio
from demucs.pretrained import get_model
from pydub import AudioSegment  # Add pydub for MP3 conversion


def extract_vocals_from_bytes(audio_bytes: bytes, model_name: str = "htdemucs") -> bytes:
    """
    Extract vocals from an audio file provided as bytes.

    Args:
        audio_bytes: The input audio file as bytes
        model_name: The demucs model to use (default: htdemucs)

    Returns:
        bytes: The extracted vocals as MP3 bytes
    """
    # Create a temporary directory to store files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the input bytes to a temporary file
        input_path = Path(temp_dir) / "input.wav"
        with open(input_path, "wb") as f:
            f.write(audio_bytes)

        # Load the model
        model = get_model(model_name)
        model.cpu()
        model.eval()

        # Set up the output directory
        out_dir = Path(temp_dir) / "separated"
        out_dir.mkdir(exist_ok=True)

        # Load the audio file
        print("loading audio file")
        wav = AudioFile(input_path).read(streams=0, samplerate=model.samplerate, channels=model.audio_channels)
        ref = wav.mean(0)
        wav = (wav - ref.mean()) / ref.std()

        # Apply the model
        print("applying model wait around 1 minute...")
        with torch.no_grad():
            sources = apply_model(model, wav[None])[0]
            sources = sources * ref.std() + ref.mean()

        # Get the vocals (typically the third source in htdemucs)
        vocal_idx = 0
        for i, source_name in enumerate(model.sources):
            if source_name.lower() == "vocals":
                vocal_idx = i
                break

        print("getting vocals")

        vocals = sources[vocal_idx]

        # Save the vocals to a temporary WAV file
        vocal_wav_path = out_dir / "vocals.wav"
        vocal_mp3_path = out_dir / "vocals.mp3"
        save_audio(vocals, str(vocal_wav_path), model.samplerate)

        # Convert WAV to MP3
        print("Converting to MP3")
        audio = AudioSegment.from_wav(str(vocal_wav_path))
        audio.export(str(vocal_mp3_path), format="mp3")

        print("Finished vocals")
        # Read the MP3 file back as bytes
        with open(vocal_mp3_path, "rb") as f:
            vocal_bytes = f.read()

        return vocal_bytes


def extract_all_stems_from_bytes(audio_bytes: bytes, model_name: str = "htdemucs") -> dict:
    """
    Extract all stems (vocals, drums, bass, other) from an audio file provided as bytes.

    Args:
        audio_bytes: The input audio file as bytes
        model_name: The demucs model to use (default: htdemucs)

    Returns:
        dict: A dictionary containing all stems as MP3 bytes with keys: 'vocals', 'drums', 'bass', 'other'
    """
    # Create a temporary directory to store files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the input bytes to a temporary file
        input_path = Path(temp_dir) / "input.wav"
        with open(input_path, "wb") as f:
            f.write(audio_bytes)

        # Load the model
        model = get_model(model_name)
        model.cpu()
        model.eval()

        # Set up the output directory
        out_dir = Path(temp_dir) / "separated"
        out_dir.mkdir(exist_ok=True)

        # Load the audio file
        wav = AudioFile(input_path).read(streams=0, samplerate=model.samplerate, channels=model.audio_channels)
        ref = wav.mean(0)
        wav = (wav - ref.mean()) / ref.std()

        # Apply the model
        with torch.no_grad():
            sources = apply_model(model, wav[None])[0]
            sources = sources * ref.std() + ref.mean()

        # Save all stems and collect them as bytes
        result = {}
        for i, source_name in enumerate(model.sources):
            source_wav_path = out_dir / f"{source_name}.wav"
            source_mp3_path = out_dir / f"{source_name}.mp3"

            # Save as WAV first
            save_audio(sources[i], str(source_wav_path), model.samplerate)

            # Convert WAV to MP3
            audio = AudioSegment.from_wav(str(source_wav_path))
            audio.export(str(source_mp3_path), format="mp3")

            # Read the MP3 file as bytes
            with open(source_mp3_path, "rb") as f:
                result[source_name.lower()] = f.read()

        return result


# def create_test_audio_file(output_path: str = "sample.wav", duration: float = 3.0):
#     """
#     Create a simple test audio file with a sine wave.

#     Args:
#         output_path: Path to save the test audio file
#         duration: Duration of the test audio in seconds
#     """
#     sample_rate = 44100
#     # Create a simple sine wave
#     t = torch.arange(0, duration, 1 / sample_rate)
#     # Generate a tone at 440 Hz (A4)
#     sine_wave = 0.5 * torch.sin(2 * torch.pi * 440 * t)
#     # Add a higher frequency component to simulate vocals
#     sine_wave += 0.3 * torch.sin(2 * torch.pi * 880 * t)

#     # Convert to proper format for torchaudio
#     sine_wave = sine_wave.unsqueeze(0)  # Add channel dimension

#     # Save the audio file
#     torchaudio.save(output_path, sine_wave, sample_rate)
#     print(f"Created test audio file at {output_path}")

#     return output_path


# if __name__ == "__main__":
#     import os

#     # Create a test directory
#     test_dir = "test_demucs"
#     os.makedirs(test_dir, exist_ok=True)

#     # Create a test audio file
#     test_file = create_test_audio_file(os.path.join(test_dir, "sample.wav"))

#     print(f"Processing test file: {test_file}")

#     # Read the test audio file
#     with open(test_file, "rb") as f:
#         audio_bytes = f.read()

#     # Extract vocals
#     print("Extracting vocals...")
#     vocals_bytes = extract_vocals_from_bytes(audio_bytes)

#     # Save the vocals
#     vocals_path = os.path.join(test_dir, "vocals.wav")
#     with open(vocals_path, "wb") as f:
#         f.write(vocals_bytes)
#     print(f"Saved vocals to {vocals_path}")

#     # Extract all stems
#     print("Extracting all stems...")
#     stems = extract_all_stems_from_bytes(audio_bytes)

#     # Save all stems
#     for stem_name, stem_bytes in stems.items():
#         stem_path = os.path.join(test_dir, f"{stem_name}.wav")
#         with open(stem_path, "wb") as f:
#             f.write(stem_bytes)
#         print(f"Saved {stem_name} to {stem_path}")

#     print("Done!")


if __name__ == "__main__":
    print("starting")
    with open("./sample.mp3", "rb") as f:
        audio_bytes = f.read()
    print("extracting vocals")
    results = extract_vocals_from_bytes(audio_bytes)
    print("done")
    with open("vocals.mp3", "wb") as f:
        f.write(results)
