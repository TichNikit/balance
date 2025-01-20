FROM python

# Устанавливаем рабочую директорию
WORKDIR /app

# Скопируем файл зависимостей first
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Если у вас есть миграции Alembic, то можно их применить
CMD ["alembic", "upgrade", "head"]


# Если у вас есть миграции Alembic, то можно их применить
# CMD ["alembic", "upgrade", "head"]