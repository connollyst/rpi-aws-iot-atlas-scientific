FROM balenalib/raspberry-pi-debian-python:latest

RUN apt-get update
RUN apt-get install gcc
RUN apt-get install make
RUN apt-get install cmake
RUN apt-get install libssl-dev


COPY requirements.txt /
RUN pip install -r requirements.txt

COPY atlas/ /atlas/
COPY aws/ /aws/
COPY comms/ /comms/
COPY main.py /
CMD [ "python", "./main.py" ]