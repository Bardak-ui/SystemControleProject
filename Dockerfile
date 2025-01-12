# Указываем базовый образ
FROM python:3.12.8

# Устанавливаем рабочую директорию
WORKDIR /scp

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

COPY . /scp/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

