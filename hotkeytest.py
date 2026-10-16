"""Test hotkey dengan PeekMessage - non-blocking."""
import ctypes
import ctypes.wintypes
import time

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

MOD_CONTROL = 0x0004
WM_HOTKEY   = 0x0312
PM_REMOVE   = 0x0001

VK_F9  = 0x78
VK_F10 = 0x79

ret = user32.RegisterHotKey(None, 1, MOD_CONTROL, VK_F9)
print(f"RegisterHotKey Ctrl+F9: {ret}, err={kernel32.GetLastError()}")
ret2 = user32.RegisterHotKey(None, 2, MOD_CONTROL, VK_F10)
print(f"RegisterHotKey Ctrl+F10: {ret2}, err={kernel32.GetLastError()}")

print("Tekan Ctrl+F9... Ctrl+F10 untuk keluar. Tunggu 30 detik.")

msg = ctypes.wintypes.MSG()
for _ in range(3000):  # 30 detik
    while user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, PM_REMOVE):
        print(f"msg={msg.message:#06x} wparam={msg.wParam}")
        if msg.message == WM_HOTKEY:
            print(f">>> HOTKEY id={msg.wParam}")
            if msg.wParam == 2:
                break
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))
    time.sleep(0.01)

user32.UnregisterHotKey(None, 1)
user32.UnregisterHotKey(None, 2)
print("Selesai.")
