"""
CursorHide - Sembunyikan kursor Windows dengan kursor transparan.
F9    : toggle sembunyikan/pulihkan kursor
F11   : keluar
Klik kanan tray icon -> menu tersedia.
Tray icon: hijau = visible, merah = hidden
"""

import ctypes
import ctypes.wintypes
import tempfile
import os
import struct
import time
import traceback

# ── Windows API ────────────────────────────────────────────────
user32  = ctypes.windll.user32
shell32 = ctypes.windll.shell32
gdi32   = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32

# ── cursor registry ────────────────────────────────────────────
CURSOR_VALUE_NAMES = [
    "Arrow","Help","AppStarting","Wait","Crosshair","IBeam",
    "NWPen","No","SizeNS","SizeWE","SizeNWSE","SizeSWNE",
    "SizeAll","UpArrow","Hand",
]

def make_transparent_cur() -> str:
    width = height = 1
    icondir     = struct.pack("<HHH", 0, 2, 1)
    bmp_size    = 40 + 8 + 4 + 4
    entry       = struct.pack("<BBBBHHiI", width, height, 0, 0, 0, 0, bmp_size, 22)
    bih         = struct.pack("<IiiHHIIiiII", 40, width, height*2, 1, 1, 0, 0, 0, 0, 0, 0)
    color_table = struct.pack("<BBBBBBBB", 0,0,0,0, 255,255,255,0)
    xor_mask    = b"\x00\x00\x00\x00"
    and_mask    = b"\x80\x00\x00\x00"
    data = icondir + entry + bih + color_table + xor_mask + and_mask
    tmp = tempfile.NamedTemporaryFile(suffix=".cur", delete=False)
    tmp.write(data)
    tmp.close()
    return tmp.name

def get_current_scheme() -> dict:
    import winreg as _reg
    scheme = {}
    try:
        key = _reg.OpenKey(_reg.HKEY_CURRENT_USER, r"Control Panel\Cursors")
        for name in CURSOR_VALUE_NAMES:
            try:
                val, _ = _reg.QueryValueEx(key, name)
                scheme[name] = val
            except FileNotFoundError:
                scheme[name] = ""
        _reg.CloseKey(key)
    except Exception:
        pass
    return scheme

def set_scheme(scheme: dict):
    import winreg as _reg
    try:
        key = _reg.OpenKey(_reg.HKEY_CURRENT_USER, r"Control Panel\Cursors",
                           0, _reg.KEY_SET_VALUE)
        for name, val in scheme.items():
            _reg.SetValueEx(key, name, 0, _reg.REG_SZ, val)
        _reg.CloseKey(key)
    except Exception:
        pass
    user32.SystemParametersInfoW(0x0057, 0, None, 3)

def set_all_transparent(cur_path: str):
    set_scheme({name: cur_path for name in CURSOR_VALUE_NAMES})

# ── tray constants ─────────────────────────────────────────────
WM_TRAY         = 0x8001
NIM_ADD         = 0
NIM_MODIFY      = 1
NIM_DELETE      = 2
NIF_MESSAGE     = 0x01
NIF_ICON        = 0x02
NIF_TIP         = 0x04
WM_RBUTTONUP    = 0x0205
TPM_BOTTOMALIGN = 0x0040
TPM_RIGHTALIGN  = 0x0008
MF_STRING       = 0x0000
MF_SEPARATOR    = 0x0800
IDM_SHOW        = 1001
IDM_HIDE        = 1002
IDM_QUIT        = 1003
ID_TOGGLE       = 1
ID_QUIT         = 3
WM_HOTKEY       = 0x0312
VK_F9           = 0x78
VK_F11          = 0x7A

class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize",           ctypes.wintypes.DWORD),
        ("hWnd",             ctypes.wintypes.HWND),
        ("uID",              ctypes.wintypes.UINT),
        ("uFlags",           ctypes.wintypes.UINT),
        ("uCallbackMessage", ctypes.wintypes.UINT),
        ("hIcon",            ctypes.wintypes.HANDLE),
        ("szTip",            ctypes.wintypes.WCHAR * 128),
        ("dwState",          ctypes.wintypes.DWORD),
        ("dwStateMask",      ctypes.wintypes.DWORD),
        ("szInfo",           ctypes.wintypes.WCHAR * 256),
        ("uVersion",         ctypes.wintypes.UINT),
        ("szInfoTitle",      ctypes.wintypes.WCHAR * 64),
        ("dwInfoFlags",      ctypes.wintypes.DWORD),
    ]

def make_icon(color_rgb: tuple, size: int = 16) -> ctypes.wintypes.HANDLE:
    r, g, b = color_rgb
    colorref = r | (g << 8) | (b << 16)
    hdc_screen = user32.GetDC(None)
    hdc        = gdi32.CreateCompatibleDC(hdc_screen)
    hbmp       = gdi32.CreateCompatibleBitmap(hdc_screen, size, size)
    gdi32.SelectObject(hdc, hbmp)
    hbr_bg = gdi32.CreateSolidBrush(0)
    rect   = ctypes.wintypes.RECT(0, 0, size, size)
    user32.FillRect(hdc, ctypes.byref(rect), hbr_bg)
    gdi32.DeleteObject(hbr_bg)
    hbr  = gdi32.CreateSolidBrush(colorref)
    hpen = gdi32.CreatePen(0, 0, colorref)
    gdi32.SelectObject(hdc, hbr)
    gdi32.SelectObject(hdc, hpen)
    gdi32.Ellipse(hdc, 1, 1, size-1, size-1)
    gdi32.DeleteObject(hbr)
    gdi32.DeleteObject(hpen)
    hbmp_mask = gdi32.CreateCompatibleBitmap(hdc_screen, size, size)
    class ICONINFO(ctypes.Structure):
        _fields_ = [
            ("fIcon",    ctypes.wintypes.BOOL),
            ("xHotspot", ctypes.wintypes.DWORD),
            ("yHotspot", ctypes.wintypes.DWORD),
            ("hbmMask",  ctypes.wintypes.HANDLE),
            ("hbmColor", ctypes.wintypes.HANDLE),
        ]
    ii = ICONINFO(fIcon=True, xHotspot=0, yHotspot=0,
                  hbmMask=hbmp_mask, hbmColor=hbmp)
    hicon = user32.CreateIconIndirect(ctypes.byref(ii))
    gdi32.DeleteObject(hbmp_mask)
    gdi32.DeleteDC(hdc)
    user32.ReleaseDC(None, hdc_screen)
    return hicon


class TrayApp:
    CLASS_NAME = "CursorHideTray"

    def __init__(self):
        self.hwnd            = None
        self.nid             = None
        self.icon_visible    = None
        self.icon_hidden     = None
        self.hidden          = False
        self.original_scheme = {}
        self.cur_path        = ""
        self._last_toggle    = 0.0

    def _create_window(self):
        WNDPROC = ctypes.WINFUNCTYPE(
            ctypes.c_longlong,
            ctypes.wintypes.HWND,
            ctypes.wintypes.UINT,
            ctypes.wintypes.WPARAM,
            ctypes.wintypes.LPARAM,
        )
        self._wndproc_ref = WNDPROC(self._wndproc)

        class WNDCLASS(ctypes.Structure):
            _fields_ = [
                ("style",         ctypes.wintypes.UINT),
                ("lpfnWndProc",   WNDPROC),
                ("cbClsExtra",    ctypes.c_int),
                ("cbWndExtra",    ctypes.c_int),
                ("hInstance",     ctypes.wintypes.HANDLE),
                ("hIcon",         ctypes.wintypes.HANDLE),
                ("hCursor",       ctypes.wintypes.HANDLE),
                ("hbrBackground", ctypes.wintypes.HANDLE),
                ("lpszMenuName",  ctypes.wintypes.LPCWSTR),
                ("lpszClassName", ctypes.wintypes.LPCWSTR),
            ]

        wc = WNDCLASS()
        wc.lpfnWndProc   = self._wndproc_ref
        wc.hInstance     = kernel32.GetModuleHandleW(None)
        wc.lpszClassName = self.CLASS_NAME
        user32.RegisterClassW(ctypes.byref(wc))

        user32.CreateWindowExW.restype = ctypes.wintypes.HWND
        HWND_MESSAGE = ctypes.wintypes.HWND(-3)
        self.hwnd = user32.CreateWindowExW(
            0, self.CLASS_NAME, "CursorHide",
            0, 0, 0, 0, 0,
            HWND_MESSAGE, None, None, None
        )

    def _add_tray(self):
        self.icon_visible = make_icon((46, 204, 113))   # hijau
        self.icon_hidden  = make_icon((231, 76,  60))   # merah
        nid = NOTIFYICONDATA()
        nid.cbSize           = ctypes.sizeof(NOTIFYICONDATA)
        nid.hWnd             = self.hwnd
        nid.uID              = 1
        nid.uFlags           = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid.uCallbackMessage = WM_TRAY
        nid.hIcon            = self.icon_visible
        nid.szTip            = "CursorHide — Visible  [F9 toggle]"
        self.nid = nid
        shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(nid))

    def _update_tray(self):
        if self.hidden:
            self.nid.hIcon = self.icon_hidden
            self.nid.szTip = "CursorHide — HIDDEN  [F9 pulihkan]"
        else:
            self.nid.hIcon = self.icon_visible
            self.nid.szTip = "CursorHide — Visible  [F9 sembunyikan]"
        self.nid.uFlags = NIF_ICON | NIF_TIP
        shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(self.nid))

    def _remove_tray(self):
        if self.nid:
            shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(self.nid))

    def _show_menu(self):
        hmenu = user32.CreatePopupMenu()
        if self.hidden:
            user32.AppendMenuW(hmenu, MF_STRING, IDM_SHOW, "Pulihkan Kursor  (F9)")
        else:
            user32.AppendMenuW(hmenu, MF_STRING, IDM_HIDE, "Sembunyikan Kursor  (F9)")
        user32.AppendMenuW(hmenu, MF_SEPARATOR, 0, "")
        user32.AppendMenuW(hmenu, MF_STRING, IDM_QUIT, "Keluar  (F11)")
        pt = ctypes.wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        user32.SetForegroundWindow(self.hwnd)
        user32.TrackPopupMenu(hmenu, TPM_BOTTOMALIGN | TPM_RIGHTALIGN,
                              pt.x, pt.y, 0, self.hwnd, None)
        user32.DestroyMenu(hmenu)

    def do_toggle(self):
        now = time.time()
        if now - self._last_toggle < 0.5:
            return
        self._last_toggle = now
        if self.hidden:
            self.do_show()
        else:
            self.do_hide()

    def do_hide(self):
        if not self.hidden:
            set_all_transparent(self.cur_path)
            self.hidden = True
            self._update_tray()

    def do_show(self):
        if self.hidden:
            set_scheme(self.original_scheme)
            self.hidden = False
            self._update_tray()

    def do_quit(self):
        set_scheme(self.original_scheme)
        self._remove_tray()
        user32.UnregisterHotKey(self.hwnd, ID_TOGGLE)
        user32.UnregisterHotKey(self.hwnd, ID_QUIT)
        user32.PostQuitMessage(0)

    def _wndproc(self, hwnd, msg, wparam, lparam):
        if msg == WM_TRAY:
            if lparam & 0xFFFF == WM_RBUTTONUP:
                self._show_menu()
                return 0
        elif msg == WM_HOTKEY:
            if wparam == ID_TOGGLE:
                self.do_toggle()
            elif wparam == ID_QUIT:
                self.do_quit()
            return 0
        elif msg == 0x0111:  # WM_COMMAND
            cmd = wparam & 0xFFFF
            if cmd == IDM_HIDE:
                self.do_hide()
            elif cmd == IDM_SHOW:
                self.do_show()
            elif cmd == IDM_QUIT:
                self.do_quit()
            return 0
        return user32.DefWindowProcW(hwnd, msg, wparam, ctypes.c_longlong(lparam))

    def run(self):
        self.original_scheme = get_current_scheme()
        self.cur_path        = make_transparent_cur()

        self._create_window()
        self._add_tray()

        user32.RegisterHotKey(self.hwnd, ID_TOGGLE, 0, VK_F9)
        user32.RegisterHotKey(self.hwnd, ID_QUIT,   0, VK_F11)

        msg = ctypes.wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == WM_HOTKEY:
                if msg.wParam == ID_TOGGLE:
                    self.do_toggle()
                elif msg.wParam == ID_QUIT:
                    self.do_quit()
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

        try:
            os.unlink(self.cur_path)
        except Exception:
            pass


if __name__ == "__main__":
    try:
        TrayApp().run()
    except Exception:
        import traceback
        with open(os.path.join(os.path.expanduser("~"), "CursorHide_error.txt"), "w") as f:
            f.write(traceback.format_exc())
