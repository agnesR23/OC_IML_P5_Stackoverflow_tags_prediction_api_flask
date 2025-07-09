FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "flask_app_env", "/bin/bash", "-c"]

COPY . .

EXPOSE 5001

CMD ["conda", "run", "--no-capture-output", "-n", "flask_app_env", "gunicorn", "-b", "0.0.0.0:5001", "app:app"]
