FROM python:3.9
 
WORKDIR /app
 
COPY requirements.txt ./
 
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt
 
COPY ./reddit_telegram_bot .
 
ENTRYPOINT ["python3", "main.py"]