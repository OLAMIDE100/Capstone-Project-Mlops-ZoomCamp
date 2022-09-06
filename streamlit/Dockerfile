FROM python:3.8


RUN pip3 install pipenv 

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "frontend.py", "frontend.py" ]

COPY images/* images/

EXPOSE 8501

ENTRYPOINT [ "streamlit", "run", "frontend.py"]