import traceback
import sys

try:
    import cursorhide
    cursorhide.TrayApp().run()
except Exception as e:
    traceback.print_exc()
    input("\nPress Enter to close...")
