FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install pytelegrambotapi python-dotenv anthropic
CMD ["python", "main.py"]
