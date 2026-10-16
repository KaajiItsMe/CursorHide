@echo off
cd /d "%~dp0"
py -m pip install --upgrade pyinstaller
py -m PyInstaller --onefile --console --name CursorHide cursorhide.py
echo.
if exist "dist\CursorHide.exe" (
  echo Selesai: dist\CursorHide.exe
) else (
  echo Build gagal. Periksa pesan error di atas.
)
pause
