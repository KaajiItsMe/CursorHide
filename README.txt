CursorHide - Portable Windows (source starter)

Fungsi:
- Ctrl+Alt+H: mengganti kursor Windows dengan kursor transparan.
- Ctrl+Alt+S: memulihkan skema kursor Windows.
- Ctrl+Alt+Q: keluar dan mencoba memulihkan skema kursor.

PENTING:
- Ini adalah prototipe sumber, belum berupa EXE.
- Mengubah skema kursor Windows sementara. Uji terlebih dahulu.
- Google Meet/Zoom dapat menangkap kursor secara terpisah; karena itu tool ini tidak menjamin kursor hilang dari share screen pada semua mode.
- Tutup dengan Ctrl+Alt+Q agar kursor dipulihkan. Jika kursor bermasalah, buka Settings > Bluetooth & devices > Mouse > Additional mouse settings > Pointers, lalu pilih skema default dan Apply, atau restart Windows.
- Jangan gunakan "End task" jika bisa menghindarinya.

Membuat EXE:
1. Pasang Python 3.10+ di Windows (centang Add Python to PATH).
2. Buka folder ini.
3. Klik dua kali build.bat.
4. EXE akan dibuat di dist\CursorHide.exe.

Pin ke taskbar:
- Klik kanan dist\CursorHide.exe > Show more options > Pin to taskbar.
- Saat berjalan, jendela konsol akan terlihat untuk menunjukkan status. Jangan tutup jendela kecuali ingin keluar.

Shortcut dapat gagal jika Ctrl+Alt+H/S/Q sudah digunakan program lain.
