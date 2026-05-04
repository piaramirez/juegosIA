"""
================================================================
P01 - JUEGO DEL GATO CON INTELIGENCIA ARTIFICIAL
================================================================
Fecha: 04 de Mayo de 2026
Escuela: Universidad Nacional Autónoma de México (UNAM) FES Aragón
Grupo: 2907
Materia: Inteligencia Artificial
Docente: MARTIN ROMERO UGALDE
Integrantes del equipo (Orden alfabético por apellido):
            1. Ramírez Alcántara, Pedro Antonio
            2. Victor Flores, Felix Omar
================================================================
"""

import tkinter as tk
from tkinter import messagebox
import random

class GatoJuego:
    def __init__(self, parent, dificultad, al_cerrar):
        self.window = tk.Toplevel(parent)
        self.window.title(f"P01: Gato IA - Nivel {dificultad}")
        self.window.geometry("450x750")
        self.window.configure(bg="#1B396B")
        
        # Protocolo para la "X" de la ventanas
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar_juego)
        
        self.dificultad = dificultad
        self.al_cerrar_callback = al_cerrar
        self.tablero = [' ' for _ in range(9)]
        self.modo_inicio = None 
        
        # Variables de puntuación
        self.ganados = 0
        self.perdidos = 0
        self.empates = 0
        self.juegos_totales = 0
        
        self.setup_ui()
        self.seleccionar_quien_inicia()

    def setup_ui(self):
        # Frame del Marcador
        self.score_frame = tk.Frame(self.window, bg="#1B396B")
        self.score_frame.pack(pady=15)
        
        self.lbl_ronda = tk.Label(self.score_frame, text="CONFIGURACIÓN", font=("Arial", 14, "bold"), fg="#D4AF37", bg="#1B396B")
        self.lbl_ronda.pack()
        
        self.lbl_score = tk.Label(self.score_frame, text="Esperando inicio...", font=("Arial", 11), fg="white", bg="#1B396B")
        self.lbl_score.pack(pady=5)
        
        # Área de juego (Tablero o Selección)
        self.grid_frame = tk.Frame(self.window, bg="#1B396B")
        self.grid_frame.pack(pady=10, expand=True)
        
        # Controles inferiores
        self.control_frame = tk.Frame(self.window, bg="#1B396B")
        self.control_frame.pack(pady=20, side="bottom")
        
        self.btn_reiniciar = tk.Button(self.control_frame, text="Reiniciar Serie (0-0)", bg="#D4AF37", fg="#1B396B", 
                                      font=("Arial", 10, "bold"), width=20, command=self.reset_completo)
        self.btn_reiniciar.pack(pady=5)

        self.btn_abandonar = tk.Button(self.control_frame, text="Cerrar Programa", bg="#cc0000", fg="white", 
                                      font=("Arial", 10, "bold"), width=20, command=self.cerrar_juego)
        self.btn_abandonar.pack(pady=5)

    def seleccionar_quien_inicia(self):
        """Pantalla intermedia para elegir el modo de juego"""
        for w in self.grid_frame.winfo_children(): w.destroy()
        self.lbl_ronda.config(text="¿QUIÉN INICIA LA SERIE?")
        
        btn_style = {"font": ("Arial", 12, "bold"), "bg": "#D4AF37", "fg": "#1B396B", "width": 20, "pady": 10}
        
        tk.Button(self.grid_frame, text="Yo inicio (X)", command=lambda: self.preparar_partida(1), **btn_style).pack(pady=10)
        tk.Button(self.grid_frame, text="IA inicia (O)", command=lambda: self.preparar_partida(2), **btn_style).pack(pady=10)
        tk.Button(self.grid_frame, text="IA vs IA (Simulación)", command=lambda: self.preparar_partida(3), **btn_style).pack(pady=10)

    def preparar_partida(self, modo):
        self.modo_inicio = modo
        for w in self.grid_frame.winfo_children(): w.destroy()
        
        # Crear los botones del tablero físico
        self.botones = []
        for i in range(9):
            btn = tk.Button(self.grid_frame, text="", font=("Arial", 24, "bold"), width=5, height=2,
                            bg="#F0F0F0", command=lambda idx=i: self.click_usuario(idx))
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.botones.append(btn)
        self.nueva_partida()

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

        if self.modo_inicio == 2: # Inicia IA
            self.window.after(600, self.turno_ia)
        elif self.modo_inicio == 3: # IA contra IA
            self.window.after(600, self.duelo_ias)

    def duelo_ias(self):
        if not self.verificar_estado():
            vacias = self.tablero.count(' ')
            # X mueve en turnos pares de espacios vacíos (9, 7, 5...) si IA inicia segunda
            # Aquí ajustamos para que se vean ambos símbolos
            jugador = 'X' if vacias % 2 != 0 else 'O'
            
            idx = self.minimax(self.tablero, jugador)[1] if self.dificultad == 3 else self.ia_basica(jugador)
            self.mover(idx, jugador)
            self.window.after(600, self.duelo_ias)

    def click_usuario(self, idx):
        if self.tablero[idx] == ' ' and self.modo_inicio != 3:
            self.mover(idx, 'X')
            if not self.verificar_estado():
                self.window.after(400, self.turno_ia)

    def turno_ia(self):
        if ' ' in self.tablero and not self.obtener_ganador(self.tablero):
            idx = self.inteligencia_artificial()
            self.mover(idx, 'O')
            self.verificar_estado()

    def mover(self, idx, jugador):
        self.tablero[idx] = jugador
        color = "#1B396B" if jugador == 'X' else "#cc0000"
        self.botones[idx].config(text=jugador, fg=color, state="disabled", disabledforeground=color)

    def inteligencia_artificial(self):
        """Lógica de IA según dificultad seleccionada"""
        vacias = [i for i, x in enumerate(self.tablero) if x == ' ']
        if self.dificultad == 1: return random.choice(vacias)
        if self.dificultad == 2: return self.ia_basica('O')
        return self.minimax(self.tablero, 'O')[1]

    def ia_basica(self, jugador):
        """Busca ganar o bloquear en el siguiente movimiento"""
        vacias = [i for i, x in enumerate(self.tablero) if x == ' ']
        oponente = 'X' if jugador == 'O' else 'O'
        # 1. Intentar ganar
        for i in vacias:
            copia = list(self.tablero); copia[i] = jugador
            if self.obtener_ganador(copia): return i
        # 2. Bloquear oponente
        for i in vacias:
            copia = list(self.tablero); copia[i] = oponente
            if self.obtener_ganador(copia): return i
        return random.choice(vacias)

    def minimax(self, b, jugador):
        """Algoritmo Minimax para IA imbatible"""
        ganador = self.obtener_ganador(b)
        if ganador == 'O': return 1, None
        if ganador == 'X': return -1, None
        if ' ' not in b: return 0, None
        
        vacias = [i for i, x in enumerate(b) if x == ' ']
        movs = []
        for i in vacias:
            b[i] = jugador
            puntos, _ = self.minimax(b, 'X' if jugador == 'O' else 'O')
            b[i] = ' '
            movs.append((puntos, i))
        
        return max(movs) if jugador == 'O' else min(movs)

    def verificar_estado(self):
        ganador = self.obtener_ganador(self.tablero)
        if ganador:
            if ganador == 'X': self.ganados += 1
            else: self.perdidos += 1
            self.terminar_ronda(f"GANADOR: {ganador}")
            return True
        if ' ' not in self.tablero:
            self.empates += 1
            self.terminar_ronda("EMPATE")
            return True
        return False

    def obtener_ganador(self, b):
        lineas = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for l in lineas:
            if b[l[0]] == b[l[1]] == b[l[2]] != ' ': return b[l[0]]
        return None

    def terminar_ronda(self, msg):
        for btn in self.botones: btn.config(state="disabled")
        self.actualizar_texto_marcador(msg)
        self.btn_abandonar.config(text="Siguiente Partida", command=self.nueva_partida, bg="#28a745")

    def reset_completo(self):
        self.ganados = 0; self.perdidos = 0; self.empates = 0; self.juegos_totales = 0
        self.seleccionar_quien_inicia()

    def finalizar_serie(self):
        res = "SERIE EMPATADA"
        if self.ganados > self.perdidos: res = "¡GANASTE LA SERIE!"
        elif self.perdidos > self.ganados: res = "LA IA GANÓ LA SERIE"
        messagebox.showinfo("Fin de la Serie", f"{res}\n\nMarcador: {self.ganados}-{self.perdidos}")
        self.cerrar_juego()

    def actualizar_texto_marcador(self, titulo):
        self.lbl_ronda.config(text=titulo)
        self.lbl_score.config(text=f"Ganados: {self.ganados}  |  Empates: {self.empates}  |  Perdidos: {self.perdidos}")

    def cerrar_juego(self):
        self.window.destroy()
        self.al_cerrar_callback()
        
        