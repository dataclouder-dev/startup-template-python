import argparse
import subprocess


# Note: this works but i think i can't send 3 multiple request or ill be blocked.
def download_tiktok(url, output_filename="tik1.mp4"):
    """
    Download a TikTok video using yt-dlp with additional parameters to avoid blocking

    Args:
        url (str): The TikTok video URL
        output_filename (str): The desired output filename (default: tik1.mp4)
    """
    try:
        command = [
            "yt-dlp",
            "-o",
            output_filename,
            "--user-agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "--add-header",
            "Referer:https://www.tiktok.com/",
            "--add-header",
            'sec-ch-ua:"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            "--add-header",
            "sec-ch-ua-mobile:?0",
            "--add-header",
            'sec-ch-ua-platform:"macOS"',
            "--cookies-from-browser",
            "chrome",
            url,
        ]
        subprocess.run(command, check=True)
        print(f"Successfully downloaded video to {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download TikTok videos from the command line")
    parser.add_argument("url", help="The TikTok video URL to download")
    parser.add_argument("-o", "--output", default="tik1.mp4", help="Output filename (default: tik1.mp4)")

    args = parser.parse_args()
    download_tiktok(args.url, args.output)


# example usage:
# python tools/tiktok_analizer/tiktik_analizer.py "https://www.tiktok.com/@polilan_app/video/7362685720835788038" -o my_video_adamo.mp4
