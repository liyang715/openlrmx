import os
import time
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox


class FileSelectorApp:
    # 添加一个文件名，用于存储上次选定的路径
    last_selected_directory_pickle = "last_selected_directory.pickle"

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("选择文件所在的目录")

        # 获取屏幕宽度和高度
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # 计算窗口大小，设置为屏幕的一半
        window_width = int(screen_width / 2)
        window_height = int(screen_height / 2)

        # 计算窗口在屏幕中的位置
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        # 设置窗口大小和位置
        self.window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # 禁止窗口调整大小
        self.window.resizable(False, False)

        self.open_folder_btn = tk.Button(self.window, text="选择目录", command=self.select_directory)
        self.open_folder_btn.pack()

        self.selected_directory_label = tk.Label(self.window, text="选择的目录：")
        self.selected_directory_label.pack()

        # 更改为多行文本输入框，并设置宽度和高度
        self.filename_entry = tk.Text(self.window, width=int(window_width*0.5*0.25), height=int(window_height*0.5*0.12))
        self.filename_entry.pack()

        self.open_file_btn = tk.Button(self.window, text="打开文件", command=self.open_file)
        self.open_file_btn.pack()

        # 读取上次选定的路径
        self.load_last_selected_directory()

    def load_last_selected_directory(self):
        if os.path.exists(self.last_selected_directory_pickle):
            with open(self.last_selected_directory_pickle, 'rb') as f:
                self.selected_directory = pickle.load(f)
        else:
            self.selected_directory = ""

        self.selected_directory_label.config(text=f"选择的目录：{self.selected_directory}")

    def save_last_selected_directory(self):
        with open(self.last_selected_directory_pickle, 'wb') as f:
            pickle.dump(self.selected_directory, f)

    def select_directory(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:  # 当选择有效路径时才更新
            self.selected_directory = selected_directory
            self.selected_directory_label.config(text=f"选择的目录：{self.selected_directory}")
            self.save_last_selected_directory()

    def open_file(self):
        filenames = self.filename_entry.get("1.0", tk.END).strip().split('\n')

        if not self.selected_directory:
            messagebox.showwarning("警告", "请先选择一个有效的文件夹路径！")
            return

        not_found_files = filenames.copy()  # 初始化未找到文件列表
        file_paths = {}  # 用于存储找到的文件路径

        for root, dirs, files in os.walk(self.selected_directory):
            for file in files:
                for filename in filenames:
                    file_with_ext = f"{filename}.lrmx"
                    if file.lower() == file_with_ext.lower():
                        file_path = os.path.join(root, file)

                        # 将找到的文件路径添加到字典中，而不是立即打开
                        file_paths[filename] = file_path

                        # 从 not_found_files 中移除找到的文件名
                        if filename in not_found_files:
                            not_found_files.remove(filename)

        # 按照输入文本中的文件名的顺序打开文件
        for filename in filenames:
            if filename in file_paths:
                print(f"打开文件：{file_paths[filename]}")
                os.startfile(file_paths[filename])
                time.sleep(1)

        # 如果仍有未找到的文件
        if not_found_files:
            messagebox.showwarning("警告", f"以下文件不存在：\n{', '.join(not_found_files)}")


if __name__ == "__main__":
    app = FileSelectorApp()
    app.window.mainloop()
