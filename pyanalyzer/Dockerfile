FROM alpine:3.13

WORKDIR /app
# wireshark installation
RUN apk add wireshark && apk add tshark

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY src .

CMD [ "python3", "runner.py" ]