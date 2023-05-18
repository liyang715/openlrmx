import os
import time
import tkinter as tk
from tkinter import filedialog

def get_input_list():
    return text_box.get('1.0', tk.END).strip().split('\n')

def search_file(search_path, target_file):
    for root, dirs, files in os.walk(search_path):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def open_files():
    names = get_input_list()
    with tk.Tk().withdraw():
        folder_path = filedialog.askdirectory(title="选择干审表文件夹路径")
    if folder_path:
        for name in names:
            openfile = f'{name.strip()}.lrmx'
            openfile_path = search_file(folder_path, openfile)
            if openfile_path:
                os.startfile(openfile_path)
                time.sleep(1)

root = tk.Tk()
root.title('请输入姓名')

text_box = tk.Text(root, width=50, height=50)
text_box.pack(side=tk.LEFT, padx=5, pady=5)

button = tk.Button(root, text='处理', command=open_files)
button.pack(side=tk.RIGHT, padx=5, pady=5)

root.mainloop()
