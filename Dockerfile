FROM jupyter/scipy-notebook:latest

USER $NB_USER

COPY . /home/jovyan/work
RUN pip install -r /home/jovyan/app/requirements.txt


