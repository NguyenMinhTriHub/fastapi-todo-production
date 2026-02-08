@echo off
title FastAPI Todo App
:: Di chuyển vào thư mục dự án
cd /d D:\23710141_NguyenMinhTri_Buoi5_AppDev
:: Kích hoạt môi trường ảo venv
call venv\Scripts\activate
:: Chạy ứng dụng FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000
pause