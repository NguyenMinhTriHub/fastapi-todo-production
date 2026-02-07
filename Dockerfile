# Sử dụng Python phiên bản nhẹ (slim)
FROM python:3.11-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements vào trước để tận dụng cache
COPY requirements.txt .

# Cài đặt các thư viện (bao gồm cả bcrypt và python-jose đã dùng ở Cấp độ 5)
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Lệnh để chạy ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]