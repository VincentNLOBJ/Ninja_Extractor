# ---------------------------------
# Ninja Extractor 1.1
# By VincentNL 25/04/2023
#
# Extract .NJ/.NJM/.NJL/.NJD files
# from any uncompressed archive.
# ---------------------------------

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


def search(magic, current_file, app_dir, filename):
    with open(current_file, "rb") as f:
        data = f.read()
        offset = 0
        curnum = 0
        addr_list = []

        '''You can modify this part to add other MAGIC / extension / filetypes'''

        if magic == b'NJCM': ext, filetype = ('.nj', 'ninja')
        elif magic == b'NMDM': ext, filetype = ('.njm', 'ninja')
        elif magic == b'NJTL': ext, filetype = ('.njl', 'ninja')
        elif magic == b'NMD\\': ext, filetype = ('.njd', 'ninja')

        while True:
            i = data.find(magic, offset)
            if i == -1: break
            offset = i + len(magic)
            addr_list.append(i)

        for i, addr in enumerate(addr_list):
            try:
                if filetype == 'ninja':
                    ''' 
                    
                    Replace / modify this part to extract other file types,
                    based on finding magic signature(s) into uncompressed archive(s).
                    
                    *** What you need to determine is the size of file after MAGIC offset. ***

                    i.e. for standard Ninja it's pretty simple:

                        MAGIC --> MODEL DATA --> POF DATA

                        1) Model size value = Magic offset + 0x4 bytes [uint32 le]
                        2) POF offset = Magic offset + 0x8 + model size
                        3) POF size value = POF offset +0x4 [uint32 le]
                        4) Ninja file size = (POF offset + POF size + 0x8) - Magic offset
                        
                    '''

                    f.seek(addr + 4)
                    size = int.from_bytes(f.read(4), byteorder='little')
                    POF_OFFSET = f.seek(addr + 8 + size)
                    POF_CHECK = int.from_bytes(f.read(3), byteorder='little')

                    if POF_CHECK == 4607824:  # "POF" in decimal value

                        f.seek(POF_OFFSET + 4)
                        POF_SIZE = int.from_bytes(f.read(4), byteorder='little')
                        FILE_END_OFFSET = POF_OFFSET + POF_SIZE + 8
                        f.seek(addr)
                        fsize = FILE_END_OFFSET - addr

                        # Save file
                        save_file(i, f, fsize, ext, curnum)
                        curnum += 1

            except: print(f'{current_file}\nFile error!')


def save_file(i, f, fsize, ext,curnum):
    # i = file , f = file, fsize = file size, ext = file extension, curnum = current file number

    if not os.path.exists(os.path.join(app_dir, 'Extracted', filename)):
        os.makedirs(os.path.join(app_dir, 'Extracted', filename))
    new_file = os.path.join(app_dir,f'Extracted/{filename}/{str(curnum).zfill(4)}{ext}')
    with open(new_file, "wb") as n:
        n.write(f.read(fsize))


# Open a file dialog to select the input file(s)
#iconPath = resource_path('ninja.ico')  # window icon
root = tk.Tk()
root.withdraw()
#root.iconbitmap(iconPath)

my_files = filedialog.askopenfilenames(initialdir=".", title="Select file(s) to scan", filetypes=[("*.*", "*.*")])

# Main Loop
for file in my_files:
    current_file = file
    source_dir, filename = os.path.split(file)
    app_dir = os.path.abspath(os.getcwd())

    '''You can modify this part to find other MAGICs'''

    for pattern in [b'NJCM', b'NMDM', b'NJTL', b'NMD\\']:
        search(pattern, current_file, app_dir, filename)
