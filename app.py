import tkinter as tk
import requests
import time
from threading import Thread

API_URL = "http://SEU_SERVIDOR/render-url/obter"  # Substitua pela URL da API

def buscar_ph():
    try:
        resp = requests.get(API_URL)
        data = resp.json()
        valor = data.get("ph", "Indisponível")
        texto.set(f"Valor de pH: {valor}")
    except Exception as e:
        texto.set("Erro ao buscar dados")

def atualizar_em_loop():
    while True:
        buscar_ph()
        time.sleep(10)

# Interface Tkinter
janela = tk.Tk()
janela.title("Monitor de pH Online")
texto = tk.StringVar()
texto.set("Aguardando dados...")

label = tk.Label(janela, textvariable=texto, font=("Helvetica", 20))
label.pack(padx=20, pady=20)

# Thread para atualização automática
Thread(target=atualizar_em_loop, daemon=True).start()

janela.mainloop()
