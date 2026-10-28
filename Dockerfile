# 1. استخدام صورة Python رسمية وخفيفة
FROM python:3.10-slim

# 2. تحديد مجلد العمل داخل الـ Container
WORKDIR /app

# 3. نسخ ملف المتطلبات أولاً لتسريع عملية الـ Build
COPY requirements.txt .

# 4. تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# 5. نسخ باقي كود التطبيق
COPY . .

# 6. تحديد المنفذ (Port) الذي يعمل عليه التطبيق
EXPOSE 10000

# 7. أمر تشغيل التطبيق بواسطة Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]