@echo off
echo 🔨 Đang build app...
python -m PyInstaller --noconsole --onefile main.py

echo ✅ Đang sao chép file JSON...
copy todo.json dist\
copy static.json dist\

echo 🧹 Đang dọn rác...
rmdir /s /q build
del main.spec

echo 🚀 Chạy app...
start dist\main.exe

pause
