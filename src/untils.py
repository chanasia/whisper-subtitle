from yt_dlp import YoutubeDL
# from pydub import AudioSegment
import os

def handle_ydl_download(video_url: str, output = "temp/videos"):
  output_file = os.path.join(output, "%(title)s.%(ext)s")
  ydl_opts = {
      "format": "mp4",
      "outtmpl": output_file,
      "quiet": True,
  }

  if video_url == None or video_url.strip() == "":
      return None

  with YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(video_url, download=True)
      download_file_path = ydl.prepare_filename(info)

  return download_file_path

def format_timestamp(seconds: float, always_include_hours: bool = False, decimal_marker: str = '.') -> str:
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
  
def save_to_vtt(subtitles, path_file):
  with open(path_file, 'w', encoding='utf-8') as file:
    file.write("WEBVTT\n\n")
    for subtitle in subtitles:
      start = format_timestamp(subtitle['start'])
      end = format_timestamp(subtitle['end'])
      file.write(f"{start} --> {end}\n")
      file.write(f"{subtitle['text']}\n\n")
  

# def audio_from_file(filename: str) -> AudioSegment:
#     try:
#         audio = AudioSegment.from_file(filename)
#     except FileNotFoundError:
#         raise ValueError(
#             f"Cannot load audio from file: `{filename}` not found. Do you forgot to install `ffmpeg`."
#         )

#     return audio
