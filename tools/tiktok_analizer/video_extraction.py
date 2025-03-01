import os

import cv2
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip

from app.storage import image_utils_service, storage
from app.storage.storage_models import CloudStorageDataDict

MAX_FRAME_DIFF = 125
MAX_EXPORTED_FRAMES = 15


def extract_frames(video_path: str, output_dir: str = "output") -> int:
    """Extract frames from video and save key frames
    Parameters:
        video_path (str): Path to the video file
        output_dir (str): Directory to save extracted content
    Returns:
        int: Number of frames processed
    """
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    prev_frame = None
    frame_exported_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Save frame if it's significantly different from previous frame
        if prev_frame is not None:
            diff = np.mean(np.abs(frame - prev_frame))
            if diff > MAX_FRAME_DIFF:  # Threshold for scene change
                frame_path = f"{output_dir}/frame_{frame_count:04d}.jpg"
                cv2.imwrite(frame_path, frame)
                frame_exported_count = frame_exported_count + 1
        prev_frame = frame.copy()
        frame_count += 1

    cap.release()
    print(f"Total Extracted {frame_exported_count} frames")
    return frame_count


def extract_audio(video_path: str, output_dir: str = "output") -> str:
    """Extract audio from video and save as WAV with reduced size
    Parameters:
        video_path (str): Path to the video file
        output_dir (str): Directory to save extracted content
    Returns:
        str: Path to the extracted audio file
    """
    os.makedirs(output_dir, exist_ok=True)
    video = VideoFileClip(video_path)
    audio = video.audio

    # Convert to mono and reduce sample rate
    audio_path = f"{output_dir}/audio.mp3"  # Changed extension to .mp3
    audio.write_audiofile(
        audio_path,
        fps=16000,  # Reduce sample rate from 44100 to 16000 Hz
        nbytes=2,  # 16-bit depth instead of 32-bit
        codec="libmp3lame",  # Use 16-bit PCM codec
        ffmpeg_params=[
            "-ac",
            "1",  # Convert to mono (1 channel)
            "-b:a",
            "64k",  # Bitrate of 64kbps (you can adjust: 32k, 64k, 96k, 128k)
        ],
    )
    video.close()
    print("saving path")
    return audio_path


def extract_frames_and_upload(video_bytes: bytes, output_dir: str = "output") -> list[CloudStorageDataDict]:
    """Extract frames from video bytes and save key frames
    Parameters:
        video_bytes (bytes): Video content as bytes
        output_dir (str): Directory to save extracted content
    Returns:
        int: Number of frames processed
    """

    print(" 🖼️ extracting frames from bytes")

    results = []

    # Create a temporary file to store the video
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        temp_file.write(video_bytes)
        temp_path = temp_file.name

    try:
        # Use the temporary file path with VideoCapture
        cap = cv2.VideoCapture(temp_path)
        frame_count = 0
        prev_frame = None
        frame_exported_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Save frame if it's significantly different from previous frame
            if prev_frame is not None:
                diff = np.mean(np.abs(frame - prev_frame))
                if diff > MAX_FRAME_DIFF:  # Threshold for scene change
                    frame_exported_count = frame_exported_count + 1
                    webp_img_io = image_utils_service.transform_to_webp_bytes(frame)

                    frame_path = f"{output_dir}/frame_{frame_count:04d}.webp"
                    print(f" 📄 {frame_exported_count} uploaded frame", frame_path)
                    storage_data = storage.upload_bytes_to_ref(frame_path, webp_img_io.getvalue())
                    print("DAta:", storage_data)
                    results.append(storage_data)
                    # cv2.imwrite(frame_path, frame)
            prev_frame = frame.copy()
            frame_count += 1
            if frame_exported_count > MAX_EXPORTED_FRAMES:
                break

        cap.release()
        print(f"Total Extracted {frame_exported_count} frames")
        return results

    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def analyze_video(video_path: str, output_dir: str = "output") -> dict:
    """
    Analyze video file: extract frames, audio, and generate transcription
    Parameters:
        video_path (str): Path to the video file
        output_dir (str): Directory to save extracted content
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Execute analysis
    print("Extracting frames...")
    num_frames = extract_frames(video_path, output_dir)
    print(f"Extracted {num_frames} frames")

    print("Extracting audio...")
    audio_path = extract_audio(video_path, output_dir)
    print("Audio extracted successfully")

    print("Generating transcription...")
    # transcription = transcribe_audio(audio_path)
    print("Analysis complete!")

    return {
        "num_frames": num_frames,
        "audio_path": audio_path,
        # "transcription": transcription
    }


# Example usage
