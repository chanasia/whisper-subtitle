import warnings
import locale
import src.untils as untils;
import src.whisper as whisper

locale.getpreferredencoding = lambda: "UTF-8"
warnings.filterwarnings('ignore')

def main():
  path_save = untils.handle_ydl_download('https://www.youtube.com/watch?v=ODybtx21T7Q')
  print(path_save)
  results = whisper.transcripe(
    path_file=path_save,
    model_type="base",
    device="cpu",
    lang="th",
  )
  untils.save_to_vtt(results, 'text.vtt')
  print("Subtitles to save file successfully!")

if __name__ == "__main__":
  main()