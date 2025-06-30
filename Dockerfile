FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "flask_app_env", "/bin/bash", "-c"]

COPY . .

# On ne met PAS de CMD ici : il sera défini par chaque service dans docker-compose
