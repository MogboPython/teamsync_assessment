FROM python:3.9

RUN mkdir build

WORKDIR /build

COPY ./requirements.txt /build/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /build/requirements.txt

COPY ./app /build/app

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]