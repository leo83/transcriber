FROM python:3.10.13-slim-bookworm
RUN mkdir -p /bot/tmp
WORKDIR /bot
COPY dataholic-playground-20834bb3f079.json /bot/
ENV GOOGLE_APPLICATION_CREDENTIALS=/bot/dataholic-playground-20834bb3f079.json
COPY requirements.txt /bot/
ARG bot_token
ENV BOT_TOKEN=$bot_token
RUN pip install -r requirements.txt
COPY *.py /bot/
CMD python /bot/bot.py