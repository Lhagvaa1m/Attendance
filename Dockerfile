# 1. Албан ёсны Python image-ээр эхэлнэ
FROM python:3.10

# 2. Ажиллах директори үүсгэнэ
WORKDIR /app

# 3. Кодыг хуулж авна
COPY . .

# 4. Хэрэгтэй package-уудаа суулгана
RUN pip install --no-cache-dir -r requirements.txt

# 5. App-г ажиллуулна
CMD ["python", "main.py"]
