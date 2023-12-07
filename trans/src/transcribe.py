import logging
import os
from pathlib import Path

import config
import ffmpeg
import numpy as np
from fastapi import FastAPI, HTTPException
from google.cloud import storage
from whispercpp import Whisper, api

logging.basicConfig(level=config.logging_level)

app = FastAPI()


@app.get("/trans")
async def transcribe(file_name, model):
    logging.info(f"Get transcribe request {file_name}")

    try:
        # Read file from GCP Bucket
        client = storage.Client()
        bucket = client.get_bucket(config.gcp_bucket)

        blob = bucket.get_blob(file_name)
        logging.info(f"Downloading file `{file_name}` from gcp bucket")
        blob.download_to_filename(f"tmp/{file_name}")

        # Params for Whisper model
        params = (  # noqa # type: ignore
            api.Params.from_enum(api.SAMPLING_GREEDY)
            .with_print_progress(True)
            .with_print_realtime(False)
            .with_language("auto")
            .build()
        )

        # define dir to load models from
        model_basedir = Path(os.getcwd()) / config.model_basedir
        # Initit Whisper object
        logging.info(
            f"Initialising whisper object. Use `{model_basedir}` use model {model}."
        )
        w = Whisper.from_params(model, params, basedir=model_basedir)

        logging.info(f"Converting file `{file_name}` with ffmpeg")
        buffer, _ = (
            ffmpeg.input(f"tmp/{file_name}", threads=0)
            .output("-", **config.ffmpeg_config)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
        logging.info("Converting to numpy array")
        np_arr = np.frombuffer(buffer, np.int16).flatten().astype(np.float32) / 32768.0

        logging.info(f"Transcribing file `{file_name}`")
        text = w.transcribe(np_arr)

        return {"text": text}

    except ffmpeg.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to load audio: {e.stderr.decode()}"
        ) from e
    except Exception as e:
        logging.exception("Exception during transcribation")
        raise HTTPException(status_code=500, detail=e)

    finally:
        logging.info(f"Deleting file `{file_name}` localy")
        try:
            os.remove(f"tmp/{file_name}")
        except:
            ...
