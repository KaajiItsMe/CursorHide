"""
KeyLogger mini - deteksi VK code tombol yang ditekan.
Jalankan, tekan tombol yang ingin dijadikan shortcut, lihat VK code-nya.
Tekan ESC untuk keluar.
"""
import ctypes
import ctypes.wintypes
import time

user32 = ctypes.windll.user32

print("Tekan tombol apapun untuk lihat VK code-nya.")
print("Tekan ESC untuk keluar.\n")

VK_ESCAPE = 0x1B
prev = set()

while True:
    for vk in range(256):
        state = user32.GetAsyncKeyState(vk)
        if state & 0x8000:
            if vk not in prev:
                prev.add(vk)
                name = f"0x{vk:02X} ({vk})"
                print(f"VK: {name}")
        else:
            prev.discard(vk)
    if user32.GetAsyncKeyState(VK_ESCAPE) & 0x8000:
        break
    time.sleep(0.01)

print("Selesai.")
