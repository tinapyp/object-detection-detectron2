FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y ninja-build && \
    apt-get install -y g++ gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt && \
    python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

EXPOSE 5000

CMD ["python", "app.py"]