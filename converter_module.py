from moviepy import VideoFileClip
from pydub import AudioSegment
import os

def convert_mp4_to_mp3(input_path: str, output_dir: str = "output", bitrate: str = "192k") -> str:
    """
    Convert MP4 video to MP3 audio.

    :param input_path: Path to input MP4 video file
    :param output_dir: Directory to save the output MP3 (default "output")
    :param bitrate: Bitrate for the MP3 (default "192k")
    :return: Path to the generated MP3 file
    """
    # Check if input file exists
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract the filename without extension
    filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{filename}.mp3")

    # Load video and get audio clip
    video_clip = VideoFileClip(input_path)
    audio = video_clip.audio
    
    # Check if video contains audio
    if audio is None:
        video_clip.close()
        raise ValueError("No audio track found in the video")

    # Export audio to temporary WAV file for pydub processing
    temp_wav_path = os.path.join(output_dir, f"{filename}_temp.wav")
    audio.write_audiofile(temp_wav_path, logger=None)
    video_clip.close()

    # Load WAV audio with pydub and export as MP3 with desired bitrate
    audio_segment = AudioSegment.from_wav(temp_wav_path)
    audio_segment.export(output_path, format="mp3", bitrate=bitrate)

    # Remove temporary WAV file to keep things clean
    os.remove(temp_wav_path)

    return output_path

# Пример ручного теста:
# if __name__ == "__main__":
#     mp3_file = convert_mp4_to_mp3("assets/sample_video.mp4")
#     print(f"Conversion successful! File saved at: {mp3_file}")