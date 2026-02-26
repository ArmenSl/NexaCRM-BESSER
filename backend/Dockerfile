FROM python:3.9

WORKDIR /app

# Create data directory for SQLite
RUN mkdir -p /app/data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python seed_data.py && python main_api.py"]