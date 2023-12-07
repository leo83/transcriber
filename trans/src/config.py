import logging

logging_level = logging.INFO

gcp_bucket = "transcriber-audiofiles"

model_basedir = "models"

ffmpeg_config = {"format": "s16le", "acodec": "pcm_s16le", "ac": 1, "ar": "16000"}
