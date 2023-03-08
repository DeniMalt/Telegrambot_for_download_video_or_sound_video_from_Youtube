import moviepy.editor
from pytube import YouTube
from aiogram import Bot, Dispatcher, executor, types
import logging
import time
from pathlib import Path


def download_sound_of_video_or_video(url, n):
    yt = YouTube(url)
    streams = YouTube(url).streams
    streams.filter(progressive=True, file_extension="mp4").desc().first().download()
    time.sleep(20)
    if n == 2:
        video_file = Path(f'{yt.title}.mp4')
        video = moviepy.editor.VideoFileClip(f'{video_file}')
        audio = video.audio
        audio.write_audiofile(f'{video_file.stem}.mp3')
    return yt.title


TOKEN = "5774149027:AAEBHkrvIyWGc9GhJRg5QMeQ2dwAKh1wPOw"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f"Привет, {user_name}")

urls = []
keyboard_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_2.add("Скачать видео")
keyboard_2.add("Скачать звук из видео")
keyboard_2.add("Удалить выбранные видео")
@dp.message_handler(commands=['get_video_or_sound_of_video'])
async def start(message: types.Message):
    await message.answer("Скиньте ссылку(-и) на видео", reply_markup=keyboard_2)

    @dp.message_handler()
    async def input_url(message: types.Message):
        print(message.text)
        chat_id = message.chat.id
        if message.text.startswith == 'https://youtu.be/' or 'https://www.youtube.com/':
            urls.append(str(message.text))
        if message.text == "Скачать видео":
            if len(urls) == 0:
                await message.answer("Вы не отправляли никаких ссылок")
            else:
                for i in range(len(urls)):
                   title = download_sound_of_video_or_video(urls[i], 1)
                   with open(f"{title}.mp4", 'rb') as video:
                       await bot.send_video(message.chat.id, video)
        if message.text == "Скачать звук из видео":
            if len(urls) == 0:
                await message.answer("Вы не отправляли никаких ссылок")
            else:
                for i in range(len(urls)):
                   title = download_sound_of_video_or_video(urls[i], 2)
                   with open(f"{title}.mp3", 'rb') as sound_of_video:
                       await bot.send_audio(message.chat.id, sound_of_video)
        if message.text == "Удалить выбранные видео":
            urls.clear()
            await message.answer("Скиньте ссылку(-и) на видео", reply_markup=keyboard_2)
        types.ReplyKeyboardRemove()

if __name__ == '__main__':
    executor.start_polling(dp)
    types.ReplyKeyboardRemove()
