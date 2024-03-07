# Используй официальный образ Python как базовый
FROM python:3.9.18

# Установи рабочую директорию внутри контейнера
WORKDIR /app

# Установи pipenv
RUN pip install pipenv

# Скопируй только Pipfile и Pipfile.lock в рабочую директорию
COPY Pipfile Pipfile.lock /app/

# Установи pipenv и зависимости из Pipfile.lock
RUN pipenv install --deploy --ignore-pipfile

# Скопируй остальные файлы проекта в рабочую директорию
COPY . /app

# Устанавливаем bash в качестве команды по умолчанию
CMD ["bash"]

