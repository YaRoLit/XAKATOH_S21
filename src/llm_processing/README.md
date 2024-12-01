# Запуск локального сервера

Клонируйте репозиторий:
```
$ https://github.com/YaRoLit/XAKATOH_S21.git
```
Установите необходимые для работы приложения библиотеки python:
```
$ cd /src/llm_reocessing && pip install -r requirements.txt 
```
Скачайте большую яыковую модель, поддерживающую llama-cpp, например:
```
https://huggingface.co/bartowski/Qwen2.5-14B_Uncensored_Instruct-GGUF
```
Укажите путь к модели в скрипте llm_server.py
```
Запустите приложение:
```
$ python3 llm_server.py
```