FROM python:3.7
WORKDIR /code
EXPOSE 5055
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "127.0.0.1", "--port", "5055"]
