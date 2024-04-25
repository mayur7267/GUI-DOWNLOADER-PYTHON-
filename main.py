import tkinter as tk
from tkinter import ttk, filedialog
import requests
import os
import threading
import shutil

class Downloader:
    def __init__(self):
        self.saveto = ""
        self.download_state = "not_started"
        self.stop_event = threading.Event()
        self.window = tk.Tk()
        self.window.title("GUI Downloader")

        self.url_label = tk.Label(text="Enter Url")
        self.url_label.pack()

        self.url_entry = tk.Entry()
        self.url_entry.pack()

        self.browse_button = tk.Button(text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.download_button = tk.Button(text="Download", command=self.toggle_download)
        self.download_button.pack()

        self.window.geometry("800x400")
        self.progress_bar = ttk.Progressbar(self.window, orient="horizontal", maximum=100, length=300, mode="determinate")
        self.progress_bar.pack()

        self.download_percentage_label = ttk.Label(self.window, text="0%")
        self.download_percentage_label.pack()

        self.cancel_resume_button = ttk.Button(self.window, text="Cancel", command=self.cancel_download)
        self.cancel_resume_button.pack()

        self.window.mainloop()

    def browse_file(self):
        saveto = filedialog.asksaveasfilename(initialfile=self.url_entry.get().split("/")[-1])
        if saveto:
            self.saveto = saveto

    def toggle_download(self):
        if self.download_state == "not_started":
            self.start_download()
        elif self.download_state == "downloading":
            self.pause_download()
        elif self.download_state == "paused":
            self.resume_download()
        elif self.download_state == "canceled":
            self.cancel_download()

    def start_download(self):
        self.stop_event.clear()
        self.download_thread = threading.Thread(target=self.download_wrapper)
        self.download_thread.start()
        self.download_state = "downloading"
        self.download_button.config(text="Pause")
        self.cancel_resume_button.config(text="Cancel")

    def pause_download(self):
        self.stop_event.set()
        self.download_state = "paused"
        self.download_button.config(text="Resume")

    def resume_download(self):
        self.stop_event.clear()
        self.download_thread = threading.Thread(target=self.download_wrapper)
        self.download_thread.start()
        self.download_state = "downloading"
        self.download_button.config(text="Pause")

    def download_wrapper(self):
        self.download(self.saveto)

    def download(self, filename):
        if self.stop_event.is_set():
            return

        url = self.url_entry.get()

        print("Downloading from:", url)
        print("Saving to:", filename)

        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get("content-length", 0))

        block_size = 1024
        download_byte = 0

        with open(filename, "wb") as f:
            for data in response.iter_content(block_size):
                if self.stop_event.is_set():
                    break
                f.write(data)
                download_byte += len(data)
                progress = int((download_byte / total_size_in_bytes) * 100)
                self.progress_bar["value"] = progress
                self.download_percentage_label.config(text=f"{progress}%")
                self.window.update_idletasks()

        if not self.stop_event.is_set():
            self.download_state = "completed"
            self.download_button.config(text="Download")
            self.cancel_resume_button.config(text="Cancel")
            print("Download completed.")

    def cancel_download(self):
        self.stop_event.set()
        self.download_state = "canceled"
        self.download_button.config(text="Download")
        self.cancel_resume_button.config(text="Cancel")
        self.progress_bar["value"] = 0
        self.download_percentage_label.config(text="0%")

        if os.path.exists(self.saveto):
            os.remove(self.saveto)


Downloader()
