FROM python:3.10
#ENV SDL_AUDIODRIVER="dummy"

LABEL authors="shahrom-aminov"
RUN pip install requests pygame

WORKDIR .

COPY . .
CMD ["python3", "main.py"]
