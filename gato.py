import tkinter as tk
from tkinter import messagebox
import random

class GatoJuego:
    def __init__(self, parent, dificultad, al_cerrar):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Gato IA - Nivel {dificultad}")
        self.window.geometry("450x680")
        self.window.configure(bg="#1B396B")
        
        # Protocolo para la "X" de la ventana
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar_juego)
        
        self.dificultad = dificultad
        self.al_cerrar_callback = al_cerrar
        self.tablero = [' ' for _ in range(9)]
        
        # Variables de puntuación solicitadas
        self.ganados = 0
        self.perdidos = 0
        self.empates = 0
        self.juegos_totales = 0
        
        self.setup_ui()
        self.nueva_partida()

    def setup_ui(self):
        # Frame del Marcador
        self.score_frame = tk.Frame(self.window, bg="#1B396B")
        self.score_frame.pack(pady=15)
        
        self.lbl_ronda = tk.Label(self.score_frame, text="", font=("Arial", 14, "bold"), fg="#D4AF37", bg="#1B396B")
        self.lbl_ronda.pack()
        
        # Marcador con el formato solicitado
        self.lbl_score = tk.Label(self.score_frame, text="", font=("Arial", 11), fg="white", bg="#1B396B")
        self.lbl_score.pack(pady=5)
        
        # Tablero visual
        self.grid_frame = tk.Frame(self.window, bg="black", bd=2)
        self.grid_frame.pack(pady=10)
        
        self.botones = []
        for i in range(9):
            btn = tk.Button(self.grid_frame, text="", font=("Arial", 22, "bold"), width=5, height=2,
                            bg="#F0F0F0", command=lambda idx=i: self.click_usuario(idx))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.botones.append(btn)
            
        # Controles
        self.control_frame = tk.Frame(self.window, bg="#1B396B")
        self.control_frame.pack(pady=20)
        
        self.btn_reiniciar = tk.Button(self.control_frame, text="Reiniciar Serie", bg="#D4AF37", fg="white", 
                                      font=("Arial", 10, "bold"), width=18, command=self.reset_completo)
        self.btn_reiniciar.pack(pady=5)

        self.btn_abandonar = tk.Button(self.control_frame, text="Abandonar", bg="#cc0000", fg="white", 
                                      font=("Arial", 10, "bold"), width=18, command=self.cerrar_juego)
        self.btn_abandonar.pack(pady=5)

    def nueva_partida(self):
        if self.juegos_totales >= 5:
            self.finalizar_serie()
            return
            
        self.tablero = [' ' for _ in range(9)]
        self.juegos_totales += 1
        self.actualizar_texto_marcador(f"PARTIDA {self.juegos_totales} DE 5")
        
        for btn in self.botones:
            btn.config(text="", state="normal", bg="#F0F0F0")
        
        self.btn_abandonar.config(text="Abandonar", bg="#cc0000", command=self.cerrar_juego)

    def reset_completo(self):
        self.ganados = 0
        self.perdidos = 0
        self.empates = 0
        self.juegos_totales = 0
        self.nueva_partida()

    def click_usuario(self, idx):
        if self.tablero[idx] == ' ':
            self.mover(idx, 'X')
            if not self.verificar_estado():
                self.window.after(400, self.turno_ia)

    def turno_ia(self):
        vacias = [i for i, x in enumerate(self.tablero) if x == ' ']
        if vacias:
            idx = self.inteligencia_artificial()
            self.mover(idx, 'O')
            self.verificar_estado()

    def mover(self, idx, jugador):
        self.tablero[idx] = jugador
        color = "#1B396B" if jugador == 'X' else "#cc0000"
        self.botones[idx].config(text=jugador, fg=color, state="disabled", disabledforeground=color)

    def verificar_estado(self):
        ganador = self.obtener_ganador(self.tablero)
        if ganador == 'X':
            self.ganados += 1
            self.terminar_ronda("¡PUNTO PARA TI!")
            return True
        elif ganador == 'O':
            self.perdidos += 1
            self.terminar_ronda("PUNTO PARA LA IA")
            return True
        elif ' ' not in self.tablero:
            self.empates += 1
            self.terminar_ronda("EMPATE")
            return True
        return False

    def obtener_ganador(self, b):
        v = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for via in v:
            if b[via[0]] == b[via[1]] == b[via[2]] != ' ': return b[via[0]]
        return None

    def inteligencia_artificial(self):
        vacias = [i for i, x in enumerate(self.tablero) if x == ' ']
        if self.dificultad == 1: return random.choice(vacias)
        if self.dificultad == 2:
            for p in ['O', 'X']:
                for i in vacias:
                    copia = list(self.tablero); copia[i] = p
                    if self.obtener_ganador(copia): return i
            return random.choice(vacias)
        return self.minimax(self.tablero, 'O')[1]

    def minimax(self, b, jugador):
        ganador = self.obtener_ganador(b)
        if ganador == 'O': return 1, None
        if ganador == 'X': return -1, None
        if ' ' not in b: return 0, None
        vacias = [i for i, x in enumerate(b) if x == ' ']
        movs = []
        for i in vacias:
            b[i] = jugador
            pts, _ = self.minimax(b, 'X' if jugador == 'O' else 'O')
            b[i] = ' '
            movs.append((pts, i))
        return max(movs) if jugador == 'O' else min(movs)

    def terminar_ronda(self, msg):
        for btn in self.botones: btn.config(state="disabled")
        self.actualizar_texto_marcador(msg)
        self.btn_abandonar.config(text="Siguiente Juego", command=self.nueva_partida, bg="#28a745")

    def finalizar_serie(self):
        res = "¡EMPATE!"
        if self.ganados > self.perdidos: res = "¡ERES EL CAMPEÓN!"
        elif self.perdidos > self.ganados: res = "LA IA GANÓ LA SERIE"
        
        messagebox.showinfo("Fin de la Serie", f"{res}\n\nFinal - Ganados: {self.ganados} | Empates: {self.empates} | Perdidos: {self.perdidos}")
        self.cerrar_juego()

    def actualizar_texto_marcador(self, titulo):
        self.lbl_ronda.config(text=titulo)
        # Formato de puntaje solicitado
        marcador_txt = f"Ganados: {self.ganados}  |  Empates: {self.empates}  |  Perdidos: {self.perdidos}"
        self.lbl_score.config(text=marcador_txt)

    def cerrar_juego(self):
        self.window.destroy()
        self.al_cerrar_callback()