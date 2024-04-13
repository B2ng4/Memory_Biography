# Memory_Biography

## Описание
Телеграмм-бот для быстрого заполнения анкетных данных

## Технологии
aiogram, torch, vosk, silero, num2words, ffmpeg.

Интеграция с GigaChat.

## Алгоритм работы
- Генерация биографии по ключевым словам
- Генерация эпитафии по ключевым словам

## Запуск проекта

Клонируйте репозиторий и перейдите в него в командной строке:
``` 
git clone https://github.com/tim26006/Memory_Biography
cd Memory_Biography
```
Cоздайте и активируйте виртуальное окружение:
```
python -m venv venv
. env/Scripts/activate
```
Установите зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### Модели Vosk и Silero, а также FFmpeg

*Vosk* - оффлайн-распознавание аудио и получение из него текста. Модели доступны на сайте [проекта](https://alphacephei.com/vosk/models "Vosk - оффлайн-распознавание аудио"). Скачайте модель, разархивируйте и поместите папку model с файлами в папку models/vosk.
- [vosk-model-ru-0.22       - 1.5 Гб](https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip "Модель vosk-model-ru-0.22 - 1.5 Гб") - лучше распознает, но дольше и весит много.
- [vosk-model-small-ru-0.22 - 45 Мб](https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip "Модель vosk-model-small-ru-0.22 - 45 Мб") - хуже распознает, но быстрее и весит мало.

*Silero* - оффлайн-создание аудио сообщения из текста.
В классе TTS проекта указана [модель Silero v3.1 ru - 60 Мб](https://models.silero.ai/models/tts/ru/v3_1_ru.pt "Модель Silero v3.1 ru - 60 Мб"), которая сама скачается при первом запуске проекта. Остальные модели можно скачать [тут](https://github.com/snakers4/silero-models/blob/master/models.yml "Silero - оффлайн-создание аудио из текста") или на сайте [проекта](https://github.com/snakers4/silero-models "Silero - оффлайн-создание аудио из текста").

*FFmpeg* - набор open-source библиотек для конвертирования аудио- и видео в различных форматах.
Скачайте набор exe файлов с сайта [проекта](https://ffmpeg.org/download.html "FFmpeg - набор open-source библиотек для конвертирования аудио- и видео в различных форматах.") и поместите файл ffmpeg.exe в папки models/vosk и models/silero.


После скачивания моделей запустите код bot.py в Python.