FROM python:3.9.18

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --ignore-pipfile

COPY . /app

CMD ["bash"]

