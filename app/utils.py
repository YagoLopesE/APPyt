import os
import json

HISTORY_FILE = "history.json"

def localizar_ffmpeg():
    caminhos = [os.getcwd()]
    for c in caminhos:
        if os.path.exists(os.path.join(c, "ffmpeg.exe")):
            return c
    return None

def carregar_historico():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_historico(historico):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)
