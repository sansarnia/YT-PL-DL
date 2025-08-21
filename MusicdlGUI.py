import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, font, scrolledtext
import subprocess
import threading

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
            command = [
                "yt-dlp",
                "--ffmpeg-location", "ffmpeg.exe",
                "-x", "--audio-format", "mp3",
                "-o", f"{path}/%(title)s.%(ext)s",
                url
            ]

            # Start process
            with subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            ) as process:

                # Stream output line by line
                for line in process.stdout:
                    output_box.insert(tk.END, line)
                    output_box.see(tk.END)  # auto-scroll

                process.wait()

                if process.returncode == 0:
                    messagebox.showinfo("Done", "Download finished!")
                else:
                    messagebox.showerror("Error", f"yt-dlp exited with code {process.returncode}")

        except FileNotFoundError:
            messagebox.showerror("Error", "yt-dlp not found. Did you install it with pip?")
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

        for file in mp3_files:
            normalized_file = file.replace(".mp3", "_normalized.mp3")
            command = [
                "ffmpeg",
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



# ---------------- GUI ----------------
root = tk.Tk()
root.title("YouTube Playlist to MP3 Downloader")
root.geometry("700x500")

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
