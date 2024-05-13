FROM python:3.10
#ENV SDL_AUDIODRIVER="dummy"

LABEL authors="shahrom-aminov"
RUN pip install requests pygame
ENV DISPLAY=host.docker.internal:0.0

WORKDIR .

COPY . .
CMD ["python3", "main.py"]
