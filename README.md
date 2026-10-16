# CursorHide - Portable Windows

A lightweight Windows utility to toggle cursor visibility using hotkeys.

## ⌨️ Shortcut / Hotkey

- **`Ctrl + Alt + H`**: Menyembunyikan kursor (mengganti kursor Windows dengan kursor transparan).
- **`Ctrl + Alt + S`**: Memulihkan skema kursor Windows default.
- **`Ctrl + Alt + Q`**: Keluar dari aplikasi dan memulihkan skema kursor.

---

## ⚠️ Catatan Penting

- Mengubah skema kursor Windows sementara.
- **Google Meet / Zoom**: Aplikasi streaming atau video call tertentu dapat menangkap kursor secara terpisah (hardware/compositor capture), sehingga kursor mungkin tidak tersembunyi pada seluruh mode share screen.
- **Keluar dengan aman**: Selalu gunakan `Ctrl + Alt + Q` agar kursor dipulihkan ke posisi semula. Hindari mematikan paksa via *End task*.
- **Jika kursor hilang/bermasalah**: Buka **Settings** > **Bluetooth & devices** > **Mouse** > **Additional mouse settings** > tab **Pointers**, lalu pilih skema default dan klik **Apply**, atau restart Windows.
- Shortcut dapat bentrok jika kombinasi tombol telah digunakan oleh aplikasi lain.

---

## 🛠️ Cara Build ke EXE

1. Pastikan telah memasang **Python 3.10+** di Windows (centang *Add Python to PATH*).
2. Jalankan `build.bat` atau gunakan PyInstaller langsung:
   ```cmd
   build.bat
   ```
3. File eksekusi akan dibuat di folder `dist\CursorHide.exe`.
