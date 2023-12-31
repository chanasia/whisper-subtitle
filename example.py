import warnings
import locale
import YTGenerateSubtitle

locale.getpreferredencoding = lambda: "UTF-8"
warnings.filterwarnings('ignore')

def main():
  url = "https://youtu.be/oMHH_iNXUNo?si=cfPrfWLO4UXcU4aK"
  
  subtitle = YTGenerateSubtitle()
  subtitle.load_model("tiny", "cpu")
  subtitle.generate_subtitle(url_video=url,  
                             lang="ja",
                             task="transcribe",
                             vad=True)
  subtitle.save_to_vtt()
if __name__ == "__main__":
  main()