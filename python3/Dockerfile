FROM python:3

ADD script.py /

RUN pip install python-dateutil pytz

ENTRYPOINT [ "python", "./script.py" ]