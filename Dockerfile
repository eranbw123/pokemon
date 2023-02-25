FROM python:3.10-bullseye
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "pokemon.main:app", "--host", "0.0.0.0", "--port", "8080"]