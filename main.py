import os
import time
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path


class FileSelectorApp:
    last_selected_directory_json = Path.home() / "last_selected_directory.json"
    default_extension = ".lrmx"

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Select File Directory")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        window_width = int(screen_width / 2)
        window_height = int(screen_height / 2)

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        self.window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.window.resizable(False, False)

        self.open_folder_btn = tk.Button(self.window, text="Select Directory", command=self.select_directory)
        self.open_folder_btn.pack()

        self.selected_directory_label = tk.Label(self.window, text="Selected Directory:")
        self.selected_directory_label.pack()

        self.filename_entry = tk.Text(self.window, width=int(window_width*0.5*0.25), height=int(window_height*0.5*0.12))
        self.filename_entry.pack()

        self.open_file_btn = tk.Button(self.window, text="Open File", command=self.open_file)
        self.open_file_btn.pack()

        self.extension = self.default_extension
        self.extension_btn = tk.Button(self.window, text="Set Extension", command=self.set_extension)
        self.extension_btn.pack()

        self.load_last_selected_directory()

    def load_last_selected_directory(self):
        if self.last_selected_directory_json.is_file():
            with self.last_selected_directory_json.open() as f:
                data = json.load(f)
                self.selected_directory = data.get("selected_directory", "")
        else:
            self.selected_directory = ""

        self.selected_directory_label.config(text=f"Selected Directory: {self.selected_directory}")

    def save_last_selected_directory(self):
        data = {"selected_directory": self.selected_directory}
        with self.last_selected_directory_json.open(mode="w") as f:
            json.dump(data, f)

    def select_directory(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.selected_directory = selected_directory
            self.selected_directory_label.config(text=f"Selected Directory: {self.selected_directory}")
            self.save_last_selected_directory()

    def set_extension(self):
        self.extension = simpledialog.askstring("Set Extension", f"Enter file extension (default: {self.default_extension})") or self.default_extension

    def open_file(self):
        filenames = self.filename_entry.get("1.0", tk.END).strip().split('\n')

        if not self.selected_directory:
            messagebox.showwarning("Warning", "Please select a valid directory first!")
            return

        not_found_files = filenames.copy()
        file_paths = {}

        for root, dirs, files in os.walk(self.selected_directory):
            for file in files:
                for filename in filenames:
                    file_with_ext = f"{filename}{self.extension}"
                    if file.lower() == file_with_ext.lower():
                        file_path = os.path.join(root, file)
                        file_paths[filename] = file_path
                        if filename in not_found_files:
                            not_found_files.remove(filename)

        for filename in filenames:
            if filename in file_paths:
                file_path = file_paths[filename]
                print(f"Opening file: {file_path}")
                try:
                    os.startfile(file_path)
                    time.sleep(1)
                except FileNotFoundError:
                    print(f"Failed to open file {filename}: File not found")
                except Exception as e:
                    print(f"Failed to open file {filename}: {e}")

        if not_found_files:
            messagebox.showwarning("Warning", f"The following files do not exist:\n{', '.join(not_found_files)}")


if __name__ == "__main__":
    app = FileSelectorApp()
    app.window.mainloop()


