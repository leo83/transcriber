This is pet project. @Speech2txt_bot
It uses [ggerganov / whisper.cpp](https://github.com/ggerganov/whisper.cpp)
Here defined two services `bot` and `transcibe`. Both hosted on GCP.
All messages only in russian.
Feel free to reuse it.

No CI/CD.
No tests.

`transcibe` hosted as google cloud run.
`bot` hosted as docker on VM.

To deploy on GCP 
1. Create bucket `transcriber-audiofiles`
2. Create cloud run service with image `transcribe:universal`. No authorisation, only internal network
3. Create service account and give it admin privileges on GCP bucket
4. Use service account json to build bot  docker