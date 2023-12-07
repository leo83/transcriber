# Build

```bash
gcloud auth configure-docker europe-west10-docker.pkg.dev (once)
export TAG=latest
export IMG="europe-west10-docker.pkg.dev/dataholic-playground/transcriber/bot"
docker build --platform linux/amd64 -t $IMG:$TAG --build-arg bot_token=$TRANS_BOT_TG_TOKEN .
docker push $IMG:$TAG
```