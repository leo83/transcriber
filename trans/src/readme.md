# Don't forget ...
To predownload models with whispercpp local instllation and place it to `trnas/src/models/whispercpp`

# Build

```bash
gcloud auth configure-docker europe-west10-docker.pkg.dev (once)
export IMG=europe-west10-docker.pkg.dev/dataholic-playground/transcriber/transcribe
export TAG=universal
# to build docker from mac
docker build --platform linux/amd64 -t $IMG:$TAG .
docker push $IMG:$TAG
```
deploy to GCP cloud run (1CPU 1Gb)

```bash
export IMG=europe-west10-docker.pkg.dev/dataholic-playground/transcriber/transcribe
export TAG=universal
gcloud run deploy transcribe \
--image=$IMG:$TAG \
--region=europe-west10 \
--project=dataholic-playground \
 && gcloud run services update-traffic transcribe --to-latest
```


# Example of call:

```bash
export GCP_AUTH_TOKEN=$(gcloud auth print-identity-token)
# gcloud run services describe transcribe --region europe-west10 | grep URL
export TR_BASE_URL=$(gcloud run services list --platform managed | grep transcribe| awk '{print $4}')
curl -H "Authorization: Bearer $GCP_AUTH_TOKEN" "$TR_BASE_URL/trans?file_name=test_audio"
```