import tkinter as tk
from tkinter import ttk,filedialog
import requests
import os
# https://referrals.brave.com/latest/BRV002/Brave-Browser.dmg
class Downloader:
    def __init__(self):
        self.saveto=""
        self.window = tk.Tk()
        self.window.title("GUI Downloader")
        self.url_label=tk.Label(text="Enter Url")
        self.url_label.pack()
        self.url_entry=tk.Entry()
        self.url_entry.pack()
        self.browse_button = tk.Button(text="Browse", command=self.browse_file)
        self.browse_button.pack()
        self.download_button = tk.Button(text="download", command=self.download)
        self.download_button.pack()
        self.window.geometry("800x400")
        self.progress_bar = ttk.Progressbar(self.window , orient="horizontal", maximum=100 , length=300, mode="determinate")
        self.progress_bar.pack()
        self.download_percentage_label = ttk.Label(self.window, text="0%")
        self.download_percentage_label.pack()
        self.window.mainloop()

    def browse_file(self):
        saveto=filedialog.asksaveasfilename(initialfile=self.url_entry.get().split("/")[-1])
        self.saveto = saveto

    def download(self):
        url = self.url_entry.get()
        response = requests.get(url,stream=True)
        total_size_in_bytes = 100
        if(response.headers.get("content-length")):
          total_size_in_bytes = int(response.headers.get("content-length"))
        block_size=10000
        self.progress_bar["value"] = 0
        filename=self.url_entry.get().split("/")[-1]
        if self.saveto == "":
            self.saveto = filename
        with open(self.saveto, "wb") as f:
            for data in response.iter_content(block_size):
                self.progress_bar["value"] += (100*block_size)/total_size_in_bytes
                self.download_percentage_label.config(text=f"{self.progress_bar['value']}%")
                # print(self.progress_bar["value"])
                self.window.update()
                f.write(data)





Downloader()