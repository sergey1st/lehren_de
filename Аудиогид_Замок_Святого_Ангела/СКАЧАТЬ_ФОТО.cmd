@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3 download_photos.py 2>nul
if errorlevel 1 python download_photos.py
if errorlevel 1 echo Python 3 is required. Install from python.org or run download_photos.py manually.
pause
