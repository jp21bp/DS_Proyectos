FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./backend.py /code/backend.py

CMD ["uvicorn", "backend:app", "--port", "8000"]
