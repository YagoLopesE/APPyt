import customtkinter as ctk
import yt_dlp
import os
import threading
import json
import urllib.request
from tkinter import messagebox
from PIL import Image

# ---------- CONFIG ----------
ctk.set_appearance_mode("dark")  # dark / light / system
ctk.set_default_color_theme("blue") # blue, green, dark-blue

DOWNLOAD_DIR = "downloads"
HISTORY_FILE = "history.json"

# ---------- UTIL ----------
def localizar_ffmpeg():
    caminhos = [
        os.getcwd(),
        os.path.join(os.getcwd(), "ffmpeg-8.0.1", "bin")
    ]
    for c in caminhos:
        if os.path.exists(os.path.join(c, "ffmpeg.exe")):
            return c
    return None

def carregar_historico():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_historico(dados):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

# ---------- APP ----------
class YouTubeDownloader(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("620x520")
        self.resizable(False, False)

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        self.ffmpeg_path = localizar_ffmpeg()
        self.historico = carregar_historico()

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="YouTube Downloader",
                     font=("Segoe UI", 22, "bold")).pack(pady=10)

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Cole a URL do vídeo")
        self.url_entry.pack(fill="x", padx=40, pady=10)

        self.format_option = ctk.CTkOptionMenu(
            self, values=["Vídeo (MP4)", "Áudio (MP3)"])
        self.format_option.pack(pady=5)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(fill="x", padx=40, pady=15)
        self.progress.set(0)

        self.thumb_label = ctk.CTkLabel(self, text="")
        self.thumb_label.pack(pady=10)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(pady=5)

        self.btn_download = ctk.CTkButton(self, text="Baixar", command=self.start)
        self.btn_download.pack(pady=10)

        self.btn_open = ctk.CTkButton(
            self, text="Abrir pasta", command=self.abrir_pasta)
        self.btn_open.pack()

        if not self.ffmpeg_path:
            self.status.configure(text="⚠ MP3 indisponível (FFmpeg não encontrado)")

    def abrir_pasta(self):
        os.startfile(DOWNLOAD_DIR)

    def start(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Erro", "Cole uma URL válida.")
            return

        if self.format_option.get() == "Áudio (MP3)" and not self.ffmpeg_path:
            messagebox.showerror("Erro", "FFmpeg não encontrado.")
            return

        self.btn_download.configure(state="disabled")
        self.progress.set(0)
        self.status.configure(text="Preparando download...")

        threading.Thread(target=self.download, args=(url,), daemon=True).start()

    def hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total:
                percent = d['downloaded_bytes'] / total
                self.after(0, lambda: self.progress.set(percent))

    def download(self, url):
        try:
            ydl_opts = {
                'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                'progress_hooks': [self.hook],
            }

            if self.format_option.get() == "Áudio (MP3)":
                ydl_opts.update({
                    'format': 'bestaudio',
                    'ffmpeg_location': self.ffmpeg_path,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts['format'] = 'best'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

            self.salvar_historico(info)
            self.carregar_thumb(info)

            self.after(0, lambda: self.status.configure(
                text=f"✔ Concluído: {info.get('title')}"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Erro", str(e)))
        finally:
            self.after(0, lambda: self.btn_download.configure(state="normal"))

    def salvar_historico(self, info):
        self.historico.append({
            "title": info.get("title"),
            "url": info.get("webpage_url")
        })
        salvar_historico(self.historico)

    def carregar_thumb(self, info):
        try:
            url = info.get("thumbnail")
            path = "thumb.jpg"
            urllib.request.urlretrieve(url, path)
            img = ctk.CTkImage(Image.open(path), size=(320, 180))
            self.after(0, lambda: self.thumb_label.configure(image=img))
            self.thumb_label.image = img
        except:
            pass


if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()
