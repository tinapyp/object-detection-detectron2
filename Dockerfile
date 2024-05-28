FROM python:3.10-slim

RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY . /app

RUN pip install -U torch torchvision
RUN pip install cython pyyaml
RUN pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
RUN python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
RUN pip install -r requirements.txt

RUN 

EXPOSE 5000

CMD ["python", "app.py"]