#----------------------------------
# Ninja extractor v1.0     
# By VincentNL 2023/04/25
#
#----------------------------------
# Extract .NJ/.NJM/.NJL/.NJD files
# From any uncompressed archive.
#----------------------------------

import os
import tkinter as tk
from tkinter import filedialog

def search(pattern, current_file, app_dir, filename):
    with open(current_file, "rb") as f:

        data = f.read()
        offset = 0
        addr_list = []

        if pattern == b'NJCM':
            ext = '.nj'
        elif pattern == b'NMDM':
            ext = '.njm'
        elif pattern == b'NJTL':
            ext = '.njl'
        elif pattern == b'NMD\\':
            ext = '.njd'

        while True:
            i = data.find(pattern, offset)
            if i == -1: # no other file found
                ttl_files = len(addr_list)

                break

            offset = i + len(pattern)  # move cursor after string match
            addr_list.append(i)

        # extraction
        for i in range (ttl_files):
            f.seek(addr_list[i]+4)
            size = int.from_bytes(f.read(4), byteorder='little')

            new_file = os.path.join(app_dir, f'Extracted', filename, f'{filename[0:-4]}_{(str(i)).zfill(4)}{ext}')

            # check if POF at the end of size
            POF_OFFSET = f.seek(addr_list[i]+8+size)
            POF_CHECK = int.from_bytes(f.read(3), byteorder='little')


            if POF_CHECK != 4607824:
                print('invalid')
            # invalid file

            else:
                # extract
                f.seek(POF_OFFSET + 4)
                POF_SIZE = int.from_bytes(f.read(4), byteorder='little')


                FILE_END_OFFSET = POF_OFFSET+POF_SIZE+8
                f.seek(addr_list[i])
                fsize = FILE_END_OFFSET-addr_list[i]


                if not os.path.exists(os.path.join(app_dir, 'Extracted', filename)):
                    os.makedirs(os.path.join(app_dir, 'Extracted', filename))

                with open(new_file, "wb") as n:
                    n.write(f.read(fsize))

# ---------
# Main Loop
# ---------

# Open a file dialog to select the input file(s)
root = tk.Tk()
root.withdraw()

my_file = filedialog.askopenfilenames(
    initialdir=".",
    title="Select file(s) to scan",
    filetypes=[("*.*", "*.*")]
)

for filename in my_file:
    current_file = filename
    source_dir, filename = os.path.split(filename)

    app_dir = os.path.abspath(os.path.join(os.getcwd()))
    search(b'NJCM', current_file, app_dir, filename)
    search(b'NMDM', current_file, app_dir, filename)
    search(b'NJTL', current_file, app_dir, filename)
    search(b'NMD\\', current_file, app_dir, filename)
