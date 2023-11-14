FROM python:3.8

RUN mkdir /flask_smart_parking
COPY flask_smart_parking/ /flask_smart_parking/
WORKDIR /flask_smart_parking
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt