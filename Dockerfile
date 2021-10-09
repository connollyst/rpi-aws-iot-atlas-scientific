FROM balenalib/raspberry-pi-debian:bullseye-build-20210912

MAINTAINER Sean Connolly <connolly.st@gmail.com>

RUN sudo apt-get update && \
    sudo apt-get install -y \
    python3-pip \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt


COPY src/main/python/*.py /
COPY src/main/python/app/*.py /app/
COPY src/main/python/app/atlas/*.py /app/atlas/
COPY src/main/python/app/atlas/comms/*.py /app/atlas/comms/
COPY src/main/python/app/aws/*.py /app/aws/
COPY src/main/python/app/comms/*.py /app/comms/
COPY src/main/python/app/rpi/*.py /app/rpi/
COPY certs/ /certs/

CMD [ "python3", "./main.py" ]