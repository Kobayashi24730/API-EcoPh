import tkinter as tk
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_URL = "https://api-ecoph.onrender.com/obter"

def buscar_dados():
    try:
        resp = requests.get(API_URL)
        data = resp.json()
        return data[::-1]  # Mais novos por último
    except:
        return []

def mostrar_dados_sequencial(dados, i=0, valores=None, tempos=None):
    if valores is None: valores = []
    if tempos is None: tempos = []

    if i < len(dados):
        d = dados[i]
        ph = d.get("ph")
        horario = d.get("horario")
        listbox.insert(tk.END, f"pH: {ph:.2f}  |  {horario}")
        valores.append(ph)
        tempos.append(horario.split(" ")[1])  # Apenas hora

        # Atualiza o gráfico a cada novo dado
        ax.clear()
        ax.set_title("Variação do pH")
        ax.set_ylabel("pH")
        ax.set_xlabel("Hora")
        ax.grid(True)
        ax.plot(tempos, valores, marker='o', color='blue')
        ax.tick_params(axis='x', rotation=45)
        canvas.draw()

        # Próximo dado após 2 segundos
        root.after(2000, lambda: mostrar_dados_sequencial(dados, i+1, valores, tempos))

# ----- Interface Tkinter -----
root = tk.Tk()
root.title("Monitor de pH Online")

main_frame = tk.Frame(root)
main_frame.place(x=10,y=10,width=300,height=300)

listbox = tk.Listbox(main_frame, width=40, font=("Courier", 12))
listbox.place(x=400,y=10,width=300,height=300)

fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("Variação do pH")
ax.set_ylabel("pH")
ax.set_xlabel("Hora")

canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.draw()
canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

dados = buscar_dados()
listbox.delete(0, tk.END)
mostrar_dados_sequencial(dados)

root.mainloop()
