import whisper_timestamped as whisper
from pydub import AudioSegment
import src.constants as constants
import torch

def transcripe(
  path_file: str,
  device="cpu",
  model_type="tiny",
  task="transcribe",
  lang="auto",
  vad:bool | str =True,
  verbose=False
):
  audio = whisper.load_audio(path_file)
  if not device in constants.DEVICE_TYPES:
    raise ValueError( f"Invalid value for parameter `device`: {device}. Please choose from one of: {constants.DEVICE_TYPES}" )
  if device == "cuda":
    if not torch.cuda.is_available():
      device = "cpu"
      print("Warning. GPU acceleration unavailable. Switch to CPU mode.")
  if not model_type in constants.MODEL_TYPES:
    raise ValueError( f"Invalid value for parameter `model_type`: {model_type}. Please choose from one of: {constants.MODEL_TYPES}")
  if not task in constants.TASK_TYPES:
    raise ValueError(f"Invalid value for parameter `task`: {task}. Please choose from one of: {constants.TASK_TYPES}")
  if lang == "auto":
    lang = None
  elif lang not in [x[0] for x in constants.LANGUAGE_CODES]:
    raise ValueError(f"Invalid value for parameter `language`: {lang}. Expected a supported language by openai-whisper")
  if isinstance(vad, str):
    if not vad in constants.VAD_TYPES:
      raise ValueError(f"Invalid value for parameter `task`: {vad}. Please choose from one of: {constants.VAD_TYPES}")
  
  model = whisper.load_model(model_type, device=device)
  results = whisper.transcribe(model=model, audio=audio, vad=vad, language=lang, task="transcribe", verbose=verbose)
  
  return results['segments']