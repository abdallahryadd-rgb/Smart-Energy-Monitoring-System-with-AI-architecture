# 1. اختار نسخة بايثون خفيفة
FROM python:3.10-slim

# 2. حدد مسار العمل جوه الحاوية
WORKDIR /app

# 3. انسخ ملف المتطلبات وسطب المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. انسخ كل ملفات المشروع (الكود والموديلات) للحاوية
COPY . .

# 5. افتح بورت 8000 عشان نعرف نكلم الـ API
EXPOSE 8000

# 6. أمر تشغيل السيرفر
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]