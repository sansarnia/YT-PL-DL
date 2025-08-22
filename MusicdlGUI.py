import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, font, scrolledtext
import subprocess
import threading
import sys, os
import yt_dlp


# 🔹 Make app DPI aware on Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # or 2 for per-monitor DPI
except Exception:
    pass

def download_playlist():
    url = url_entry.get().strip()
    path = path_var.get().strip()

    if not url or not path:
        messagebox.showerror("Error", "Please provide both playlist link and download folder.")
        return

    output_box.delete("1.0", tk.END)  # clear previous logs

    def run_download():
        try:
            ffmpeg_path = resource_path("ffmpeg.exe")

            class TkLogger:
                def debug(self, msg):
                    if msg.startswith("[debug]"):
                        return
                    output_box.insert(tk.END, msg + "\n")
                    output_box.see(tk.END)
                def info(self, msg):
                    output_box.insert(tk.END, msg + "\n")
                    output_box.see(tk.END)
                def warning(self, msg):
                    output_box.insert(tk.END, "WARNING: " + msg + "\n")
                    output_box.see(tk.END)
                def error(self, msg):
                    output_box.insert(tk.END, "ERROR: " + msg + "\n")
                    output_box.see(tk.END)

            def progress_hook(d):
                if d.get('status') == 'downloading':
                    line = d.get('_default_template', '') or d.get('filename', '')
                    if 'speed' in d and 'eta' in d and 'downloaded_bytes' in d and 'total_bytes_estimate' in d:
                        output_box.insert(tk.END, f"Downloading: {d['filename']} {d.get('speed', '')} ETA {d.get('eta', '')}\n")
                    else:
                        output_box.insert(tk.END, f"Downloading: {line}\n")
                    output_box.see(tk.END)
                elif d.get('status') == 'finished':
                    output_box.insert(tk.END, "Download finished, now post-processing...\n")
                    output_box.see(tk.END)

            ydl_opts = {
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'noplaylist': False,
                'logger': TkLogger(),
                'progress_hooks': [progress_hook],
                'ffmpeg_location': ffmpeg_path,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            messagebox.showinfo("Done", "Download finished!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    threading.Thread(target=run_download, daemon=True).start()

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_var.set(folder)


def normalize_audio():
    path = path_var.get().strip()
    if not path:
        messagebox.showerror("Error", "Please choose a folder first.")
        return

    output_box.insert(tk.END, "\n🔊 Normalizing audio levels...\n")
    output_box.see(tk.END)

    def run_normalization():
        import os, glob

        mp3_files = glob.glob(os.path.join(path, "*.mp3"))
        if not mp3_files:
            messagebox.showerror("Error", "No MP3 files found in the selected folder.")
            return

        ffmpeg_exec = resource_path("ffmpeg.exe")

        for file in mp3_files:
            normalized_file = file.replace(".mp3", "_normalized.mp3")
            command = [
                ffmpeg_exec,
                "-y",  # overwrite
                "-i", file,
                "-af", "loudnorm",
                normalized_file
            ]
            try:
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                for line in process.stdout:
                    output_box.insert(tk.END, line)
                    output_box.see(tk.END)
                process.wait()
                # Replace original with normalized
                if process.returncode == 0:
                    os.replace(normalized_file, file)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                return

        messagebox.showinfo("Done", "All MP3s normalized!")

    threading.Thread(target=run_normalization, daemon=True).start()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("YouTube Playlist to MP3 Downloader")
root.geometry("700x500")
icon_path = resource_path("toilet_window_icon_pink.ico")
root.iconbitmap(icon_path)

# 🔹 Scale UI (fonts + dialogs)
root.tk.call('tk', 'scaling', 1.5)

# Set bigger default font
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=12)

tk.Label(root, text="Playlist URL:", font=("Segoe UI", 12, "bold")).pack(pady=5)
url_entry = tk.Entry(root, width=70, font=("Segoe UI", 11))
url_entry.pack(pady=5)

tk.Label(root, text="Save to Folder:", font=("Segoe UI", 12, "bold")).pack(pady=5)
frame = tk.Frame(root)
frame.pack(pady=5)
path_var = tk.StringVar()
tk.Entry(frame, textvariable=path_var, width=50, font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Browse", command=browse_folder, font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=5)

tk.Button(root, text="Download", command=download_playlist,
          font=("Segoe UI", 13, "bold"), bg="green", fg="white", padx=20, pady=10).pack(pady=10)

tk.Button(root, text="Normalize Audio", command=normalize_audio,
          font=("Segoe UI", 12, "bold"), bg="blue", fg="white", padx=15, pady=8).pack(pady=5)


# 🔹 Output log box
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15, font=("Consolas", 10))
output_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

root.mainloop()
