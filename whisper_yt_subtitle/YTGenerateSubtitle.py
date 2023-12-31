import whisper_timestamped as whisper
from typing import Literal
import whisper_yt_subtitle.constants as constants
import torch
from pytube import YouTube
from datetime import datetime
import os

class YTGenerateSubtitle:
  def __init__(self):
    self.model = None
    self.media: str = None
    self.segments: [] = None
  
  def load_model(self,
                 model_type: Literal["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"] = "tiny",
                 device: Literal["cpu", "cuda", "mps"] = "cpu"):
    if not self.model is None:
        self.clear_memory()
    if not device in constants.DEVICE_TYPES:
      raise ValueError( f"Invalid value for parameter `device`: {device}. Please choose from one of: {constants.DEVICE_TYPES}" )
    if device == "cuda":
      if not torch.cuda.is_available():
        device = "cpu"
        print("Warning. GPU acceleration unavailable. Switch to CPU mode.")
    if not model_type in constants.MODEL_TYPES:
        raise ValueError( f"Invalid value for parameter `model_type`: {model_type}. Please choose from one of: {constants.MODEL_TYPES}")
    model = whisper.load_model(model_type, device=device)
    self.model = model
    
  def generate_subtitle(self,
                        url_video: str,
                        vad: bool = True,
                        lang: str = "auto",
                        task: Literal["transcribe", "translate"] = "transcribe",
                        verbose: bool = False,
                        tmp_output_dir = ""):
    if self.model is None:
      raise ImportError("Please use load_model() before using this function.")
    if not task in constants.TASK_TYPES:
      raise ValueError(f"Invalid value for parameter `task`: {task}. Please choose from one of: {constants.TASK_TYPES}")
    if lang == "auto":
      lang = None
    elif lang not in [x[0] for x in constants.LANGUAGE_CODES]:
      raise ValueError(f"Invalid value for parameter `language`: {lang}. Expected a supported language by openai-whisper")
    if isinstance(vad, str):
      if not vad in constants.VAD_TYPES:
        raise ValueError(f"Invalid value for parameter `task`: {vad}. Please choose from one of: {constants.VAD_TYPES}")

    if tmp_output_dir == "":
      tmp_output_dir = os.path.join('temp', 'media')
    
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    file_name = f"media-{current_datetime}"
    self.media = self.__handle_ydl_download(file_name=file_name, output_dir=tmp_output_dir, video_url=url_video)
    transcribe = whisper.transcribe(model=self.model, audio=self.media, vad=vad, language=lang, task=task, verbose=verbose)
    self.segments = transcribe['segments']
      
  def __handle_ydl_download(self, video_url: str, output_dir: str, file_name: str):
    yt = YouTube(video_url)
    media_stream = yt.streams.filter().first()
    file_type = "mp4"
    path_output_file = media_stream.download(output_path=output_dir, filename=f"{file_name}.{file_type}")
    return path_output_file
      
  def __format_timestamp(self, seconds, always_include_hours: bool = False, decimal_marker: str = '.') -> str:
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
      
  def save_to_vtt(self,
                  file_name = "",
                  output_dir = ""):
    if self.segments is None:
      raise ValueError('Ensure that subtitles are crafted before proceeding to save them.')
    if file_name == "":
      file_name = self.media
    if output_dir == "":
      output_dir = os.path.join('outputs', 'subtitle')
    
    path_file = os.path.join(output_dir, f"{file_name}.vtt")
    with open(path_file, 'w', encoding='utf-8') as file:
      file.write("WEBVTT\n\n")
      for subtitle in self.segments:
        start = self.__format_timestamp(float(subtitle['start']))
        end = self.__format_timestamp(float(subtitle['end']))
        file.write(f"{start} --> {end}\n")
        file.write(f"{subtitle['text']}\n\n")
            
  def save_to_srt(self,
                  file_name = "",
                  output_dir = ""):
    if self.segments is None:
      raise ValueError('Ensure that subtitles are crafted before proceeding to save them.')
    if file_name == "":
      file_name = self.media
    if output_dir == "":
      output_dir = os.path.join('outputs', 'subtitle')
    
    path_file = os.path.join(output_dir, f"{file_name}.srt")
    with open(path_file, "w", encoding="UTF-8") as f:
        for subtitle in self.segments:
            # write srt lines
            id = subtitle["id"]
            start = self.__format_timestamp(subtitle["start"], always_include_hours=True)
            end = self.__format_timestamp(subtitle["end"], always_include_hours=True)
            text = subtitle["text"].strip().replace("-->", "->")
            f.write(f"{id}\n{start} --> {end}\n{text}\n\n")
                  
  def clear_memory(self):
    if self.model is None: return
    del self.model.encoder
    del self.model.decoder
    torch.cuda.empty_cache()