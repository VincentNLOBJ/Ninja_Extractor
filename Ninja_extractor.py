import os
import sys
import tkinter as tk
from tkinter import filedialog

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def search(pattern, current_file, app_dir, filename):
    with open(current_file, "rb") as f:
        data = f.read()
        offset = 0
        addr_list = []

        ext = None
        if pattern == b'NJCM': ext = '.nj'
        elif pattern == b'NMDM': ext = '.njm'
        elif pattern == b'NJTL': ext = '.njl'
        elif pattern == b'NMD\\': ext = '.njd'

        while True:
            i = data.find(pattern, offset)
            if i == -1: break
            offset = i + len(pattern)
            addr_list.append(i)

        for i, addr in enumerate(addr_list):
            try:
                f.seek(addr + 4)
                size = int.from_bytes(f.read(4), byteorder='little')

                new_file = os.path.join(app_dir, f'Extracted/{filename}/{filename[0:-4]}_{str(i).zfill(4)}{ext}')
                POF_OFFSET = f.seek(addr + 8 + size)
                POF_CHECK = int.from_bytes(f.read(3), byteorder='little')

                if POF_CHECK == 4607824:  # "POF" in decimal value

                    f.seek(POF_OFFSET + 4)
                    POF_SIZE = int.from_bytes(f.read(4), byteorder='little')
                    FILE_END_OFFSET = POF_OFFSET + POF_SIZE + 8
                    f.seek(addr)
                    fsize = FILE_END_OFFSET - addr

                    if not os.path.exists(os.path.join(app_dir, 'Extracted', filename)):
                        os.makedirs(os.path.join(app_dir, 'Extracted', filename))

                    with open(new_file, "wb") as n:
                        n.write(f.read(fsize))
            except: print(f'{current_file}\nNinja model file error!')


# Open a file dialog to select the input file(s)
iconPath = resource_path('ninja.ico')  # window icon
root = tk.Tk()
root.withdraw()
root.iconbitmap(iconPath)

my_files = filedialog.askopenfilenames(initialdir=".", title="Select file(s) to scan", filetypes=[("*.*", "*.*")])

# Main Loop
for file in my_files:
    current_file = file
    source_dir, filename = os.path.split(file)
    app_dir = os.path.abspath(os.getcwd())
    for pattern in [b'NJCM', b'NMDM', b'NJTL', b'NMD\\']:
        search(pattern, current_file, app_dir, filename)
