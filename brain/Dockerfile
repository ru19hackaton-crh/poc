FROM python:3

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /brain/
ADD . /brain/

CMD ["python", "./main.py"]
