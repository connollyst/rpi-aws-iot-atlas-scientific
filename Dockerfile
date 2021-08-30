FROM python:3

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY atlas/ /atlas/
COPY aws/ /aws/
COPY comms/ /comms/
COPY main.py /
CMD [ "python", "./main.py" ]