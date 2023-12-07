import asyncio
import logging
import os
import sys
from pathlib import Path

import config
import messages
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart

# from aiogram.filters.command import Command
from google.cloud import storage

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=config.logging_level)

BASE_DIR = Path(sys.argv[0]).resolve().parent

# Объект бота
bot = Bot(token=os.environ["BOT_TOKEN"])

# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(messages.start)


# # Хэндлер на команду /pricing
# @dp.message(Command("pricing"))
# async def cmd_pricing(message: types.Message):
#     logging.info(
#         f"New user registered. Username={message.from_user.username} id={message.from_user.id}"
#     )
#     await message.answer(Messages.pricing)


@dp.message(F.audio | F.voice | F.video)
async def process_audio(message: types.Message, bot: Bot):
    logging.info(
        f"User Username={message.from_user.username} id={message.from_user.id} send content"
    )
    content = message.audio or message.voice or message.video
    # Check max size violation
    size = content.file_size or 0
    if size > config.max_file_size:
        await message.answer(Messages.max_file_size)
    else:
        try:
            duration = content.duration + 10
            await message.answer(messages.transcribe_audio_start % duration)
            file_name = content.file_id or "Undefined"
            file_path = BASE_DIR / "tmp" / file_name
            logging.info(f"Downloading file `{file_name}` into `tmp`")
            await bot.download(content, destination=file_path)
            client = storage.Client()
            bucket = client.get_bucket(config.gcp_bucket)
            blob = bucket.blob(file_name)
            logging.info(f"Uploading file `{file_name}` into gcp bucket")
            blob.upload_from_filename(filename=file_path, timeout=9999999)
            logging.info(f"Call transcribation for `{file_name}`")
            response = requests.get(
                config.transcribe_base_url,
                params={"file_name": file_name, "model": config.model},
            )
            text = response.json()["text"]
            await message.answer(messages.transcribe_finished + text)
        except:
            await message.answer(messages.transcribe_error)
            raise
        finally:
            try:
                logging.info(f"Deleting file `{file_name}` localy")
                os.remove(file_path)
            except:
                ...


# @dp.message(F.voice)
# async def process_voice(message: types.Message, bot: Bot):
#     await message.answer('This is voice')


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
