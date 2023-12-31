### Generate subtitles from YouTube using Whisper.

# Features
- Supports 50 languages.
- Includes Voice Activity Detection (VAD).
- Supports transcripe and translate.

# Installation
```bash
pip install git+https://github.com/chanasia/whisper-subtitle.git
```

## For Windows
If you are using Windows, you need to install [FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z).


# Example in Python Script
```python
from whisper_subtitle import YTGenerateSubtitle

url = "https://youtu.be/PUdyzSS3Ef0?si=ZurO7_eJYDF3y-0o"

subtitle = YTGenerateSubtitle()
subtitle.load_model("tiny", "cpu")
subtitle.generate_subtitle(url_video=url,  
                            lang="ja",
                            task="transcribe",
                            vad=True)
subtitle.save_to_vtt()
```
# Class YTGenerateSubtitle

## load_model()
| Parameters   | Description          | Data Type |
|--------------|----------------------|-----------|
| `model_type` | Specify model type.   | String    |
| `device`     | Specify device.       | String    |



## generate_subtitle()
| Parameters      | Description                                | Data Type           |
|-----------------|--------------------------------------------|---------------------|
| `url_video`     | Link to the YouTube video.                   | String              |
| `vad`           | Specify Voice Activity Detection.            | Boolean or String            |
| `lang`          | Specify the language.                        | String              |
| `task`          | Specify the task (transcribe/translate).     | String              |
| `verbose`       | Show detailed output.                       | Boolean             |
| `tmp_output_dir`| Temporary directory to save the YouTube video.| String              |

## save_to_vtt()
| Parameters      | Description                                | Data Type           |
|-----------------|--------------------------------------------|---------------------|
| `file_name`     | file name.                  | String              |
| `output_dir`           | Output dirictory folder.            | String            |

## save_to_srt()
| Parameters      | Description                                | Data Type           |
|-----------------|--------------------------------------------|---------------------|
| `file_name`     | file name.                  | String              |
| `output_dir`           | Output dirictory folder.            | String            |


# LICENSE
MIT
