FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY src .

CMD [ "python3", "data_transfer.py" ]