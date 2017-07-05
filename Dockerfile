FROM python:2.7

RUN mkdir /sub
COPY . /sub
WORKDIR /sub

RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "10", "-b", "0.0.0.0:5000", "manage:app"]

ENV PYTHONPATH=/sub
EXPOSE 5000

