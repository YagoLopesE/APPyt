# 🎬 YouTube Downloader (Python)

Aplicativo desktop simples para baixar vídeos ou áudio do YouTube, desenvolvido em **Python**, com interface gráfica usando **CustomTkinter** e download via **yt-dlp**.

---

## ✨ Funcionalidades

- ✅ Download de vídeos em MP4
- 🎵 Download de áudio em MP3 (com FFmpeg)
- 🎧 Download de áudio original (M4A – sem conversão)
- 📊 Barra de progresso em tempo real
- 🖥 Interface moderna (Dark Mode)
- 📁 Organização automática dos downloads
- 🧠 Histórico de downloads
- 📦 Pronto para gerar executável `.exe`

---

## 🖼 Interface

Interface simples, moderna e intuitiva, focada em usabilidade e desempenho.

---

## 📦 Tecnologias utilizadas

- **Python 3.10+**
- **yt-dlp** – download de vídeos
- **CustomTkinter** – interface gráfica moderna
- **FFmpeg** – conversão de áudio (MP3)
- **PyInstaller** – geração de executável

---

## 📁 Estrutura do projeto

```text
pyult/
├── main.py
├── app/
│   ├── ui.py
│   ├── downloader.py
│   └── utils.py
├── downloads/
├── ffmpeg.exe
├── ffprobe.exe
├── history.json
└── assets/
    └── icon.ico
