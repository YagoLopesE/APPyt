import customtkinter as ctk
import threading
from tkinter import messagebox
from app.downloader import baixar
from app.utils import localizar_ffmpeg, carregar_historico, salvar_historico

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("520x360")
        self.resizable(False, False)

        self.ffmpeg = localizar_ffmpeg()
        self.historico = carregar_historico()

        self._ui()

    def _ui(self):
        ctk.CTkLabel(self, text="YouTube Downloader",
                     font=("Segoe UI", 22, "bold")).pack(pady=15)

        self.url = ctk.CTkEntry(self, placeholder_text="Cole a URL do vídeo")
        self.url.pack(fill="x", padx=40)

        self.formato = ctk.CTkOptionMenu(self, values=["mp4", "mp3"])
        self.formato.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(fill="x", padx=40, pady=15)
        self.progress.set(0)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack()

        ctk.CTkButton(self, text="Baixar", command=self.start).pack(pady=10)

    def start(self):
        url = self.url.get().strip()
        if not url:
            messagebox.showerror("Erro", "Cole uma URL válida.")
            return

        if self.formato.get() == "mp3" and not self.ffmpeg:
            messagebox.showerror("Erro", "FFmpeg não encontrado.")
            return

        self.progress.set(0)
        self.status.configure(text="Baixando...")

        threading.Thread(target=self.run, args=(url,), daemon=True).start()

    def hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total:
                self.progress.set(d['downloaded_bytes'] / total)

    def run(self, url):
        try:
            info = baixar(url, self.formato.get(), self.ffmpeg, self.hook)
            self.historico.append({"title": info["title"], "url": url})
            salvar_historico(self.historico)
            self.status.configure(text=f"✔ {info['title']}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
