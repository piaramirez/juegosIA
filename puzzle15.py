"""
================================================================
P02 - JUEGO DE SUMA 15 (ESTRATEGIA NUMÉRICA)
================================================================
Fecha: 03 de Mayo de 2026
Escuela: Universidad Nacional Autónoma de México (UNAM) FES Aragón
Grupo: 2907
Materia: Inteligencia Artificial
Docente: MARTIN ROMERO UGALDE
Integrantes del equipo (Orden alfabético por apellido):
            1. Flores Felix, Omar Victor
            2. Ramírez Alcántara, Pedro Antonio
================================================================
"""

import tkinter as tk
from tkinter import messagebox
import random
from itertools import combinations

class Puzzle15:
    def __init__(self, parent, al_cerrar):
        self.window = tk.Toplevel(parent)
        self.window.title("P02: Suma 15 IA - UNAM FES Aragón")
        self.window.geometry("450x780")
        self.window.configure(bg="#1B396B")
        
        self.al_cerrar_callback = al_cerrar
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar)
        
        self.ganados = 0
        self.perdidos = 0
        self.empates = 0
        self.juegos_totales = 0
        self.dificultad = 1
        self.modo_inicio = None 
        
        self.setup_ui_base()
        self.seleccionar_dificultad() # Empezamos por el nivel

    def setup_ui_base(self):
        self.score_frame = tk.Frame(self.window, bg="#1B396B")
        self.score_frame.pack(pady=15)
        
        self.lbl_info = tk.Label(self.score_frame, text="CONFIGURACIÓN", font=("Arial", 14, "bold"), fg="#D4AF37", bg="#1B396B")
        self.lbl_info.pack()
        
        self.lbl_score = tk.Label(self.score_frame, text="Esperando configuración...", font=("Arial", 11), fg="white", bg="#1B396B")
        self.lbl_score.pack(pady=5)
        
        self.main_container = tk.Frame(self.window, bg="#1B396B")
        self.main_container.pack(pady=10, expand=True, fill="both")

    def seleccionar_dificultad(self):
        for w in self.main_container.winfo_children(): w.destroy()
        self.lbl_info.config(text="SELECCIONE DIFICULTAD")
        
        btn_style = {"font": ("Arial", 12, "bold"), "bg": "#D4AF37", "fg": "#1B396B", "width": 20, "pady": 10}
        
        tk.Button(self.main_container, text="Fácil (Aleatorio)", command=lambda: self.set_dificultad(1), **btn_style).pack(pady=10)
        tk.Button(self.main_container, text="Medio (Bloqueo)", command=lambda: self.set_dificultad(2), **btn_style).pack(pady=10)
        tk.Button(self.main_container, text="Difícil (Estratégico)", command=lambda: self.set_dificultad(3), **btn_style).pack(pady=10)

    def set_dificultad(self, dif):
        self.dificultad = dif
        self.seleccionar_quien_inicia()

    def seleccionar_quien_inicia(self):
        for w in self.main_container.winfo_children(): w.destroy()
        self.lbl_info.config(text=f"NIVEL {self.dificultad}: ¿QUIÉN INICIA?")
        
        btn_style = {"font": ("Arial", 12, "bold"), "bg": "#D4AF37", "fg": "#1B396B", "width": 20, "pady": 10}
        
        tk.Button(self.main_container, text="Yo inicio", command=lambda: self.preparar_partida(1), **btn_style).pack(pady=10)
        tk.Button(self.main_container, text="IA inicia", command=lambda: self.preparar_partida(2), **btn_style).pack(pady=10)
        tk.Button(self.main_container, text="IA vs IA", command=lambda: self.preparar_partida(3), **btn_style).pack(pady=10)

    def preparar_partida(self, modo):
        self.modo_inicio = modo
        for w in self.main_container.winfo_children(): w.destroy()
        
        # Tablero de números
        self.grid_frame = tk.Frame(self.main_container, bg="#1B396B")
        self.grid_frame.pack(pady=10)
        
        self.botones = {}
        for i in range(1, 10):
            btn = tk.Button(self.grid_frame, text=str(i), font=("Arial", 20, "bold"), 
                            width=6, height=2, bg="#D4AF37", fg="#1B396B",
                            command=lambda n=i: self.jugada_usuario(n))
            btn.grid(row=(i-1)//3, column=(i-1)%3, padx=5, pady=5)
            self.botones[i] = btn
            
        self.sumas_frame = tk.Frame(self.main_container, bg="#1B396B", bd=2, relief="groove")
        self.sumas_frame.pack(pady=20, fill="x", padx=40)
        
        self.lbl_tus_num = tk.Label(self.sumas_frame, text="Tus números: []", font=("Arial", 10), fg="white", bg="#1B396B")
        self.lbl_tus_num.pack(pady=2)
        self.lbl_ia_num = tk.Label(self.sumas_frame, text="IA números: []", font=("Arial", 10), fg="#D4AF37", bg="#1B396B")
        self.lbl_ia_num.pack(pady=2)

        self.btn_control = tk.Button(self.window, text="Abandonar", bg="#cc0000", fg="white", 
                                      font=("Arial", 10, "bold"), width=20, command=self.cerrar)
        self.btn_control.pack(pady=20)
        
        self.nueva_partida()

    def nueva_partida(self):
        if self.juegos_totales >= 5:
            self.finalizar_serie()
            return
            
        self.juegos_totales += 1
        self.numeros_disponibles = list(range(1, 10))
        self.numeros_jugador = []
        self.numeros_ia = []
        self.actualizar_marcador(f"PARTIDA {self.juegos_totales} DE 5")
        
        for btn in self.botones.values():
            btn.config(text=btn.cget("text"), state="normal", bg="#D4AF37", fg="#1B396B")
        
        self.btn_control.config(text="Abandonar", bg="#cc0000", command=self.cerrar)

        if self.modo_inicio == 2: self.window.after(600, self.jugada_ia)
        elif self.modo_inicio == 3: self.window.after(600, self.duelo_ias)

    def jugada_usuario(self, n):
        if n in self.numeros_disponibles and self.modo_inicio != 3:
            self.seleccionar(n, "Usuario")
            self.lbl_tus_num.config(text=f"Tus números: {self.numeros_jugador}")
            if not self.verificar_partida(self.numeros_jugador, "¡PUNTO PARA TI!"):
                if not self.numeros_disponibles:
                    self.empates += 1
                    self.terminar_ronda("¡EMPATE!")
                else:
                    self.window.after(600, self.jugada_ia)

    def jugada_ia(self):
        if self.numeros_disponibles:
            n = self.inteligencia_ia()
            self.seleccionar(n, "IA")
            self.lbl_ia_num.config(text=f"IA números: {self.numeros_ia}")
            if not self.verificar_partida(self.numeros_ia, "PUNTO PARA IA"):
                if not self.numeros_disponibles:
                    self.empates += 1
                    self.terminar_ronda("¡EMPATE!")

    def inteligencia_ia(self):
        # 1. Ganar
        for n in self.numeros_disponibles:
            if self.puede_sumar_15(self.numeros_ia + [n]): return n
        # 2. Bloquear (Nivel 2 y 3)
        if self.dificultad >= 2:
            for n in self.numeros_disponibles:
                if self.puede_sumar_15(self.numeros_jugador + [n]): return n
        # 3. Estrategia (Nivel 3)
        if self.dificultad == 3:
            if 5 in self.numeros_disponibles: return 5
            for e in [2, 4, 6, 8]:
                if e in self.numeros_disponibles: return e
        return random.choice(self.numeros_disponibles)

    def duelo_ias(self):
        if not self.verificar_ganador_total():
            vacias = len(self.numeros_disponibles)
            jugador = "IA_1" if vacias % 2 != 0 else "IA_2"
            n = self.inteligencia_ia_duelo(jugador)
            self.seleccionar(n, "IA_1" if jugador == "IA_1" else "IA_2")
            self.lbl_tus_num.config(text=f"IA 1: {self.numeros_jugador}")
            self.lbl_ia_num.config(text=f"IA 2: {self.numeros_ia}")
            
            if not self.verificar_partida(self.numeros_jugador if jugador=="IA_1" else self.numeros_ia, f"GANA {jugador}"):
                if self.numeros_disponibles:
                    self.window.after(700, self.duelo_ias)
                else:
                    self.empates += 1
                    self.terminar_ronda("¡EMPATE!")

    def inteligencia_ia_duelo(self, turno):
        mis_num = self.numeros_jugador if turno == "IA_1" else self.numeros_ia
        sus_num = self.numeros_ia if turno == "IA_1" else self.numeros_jugador
        for n in self.numeros_disponibles:
            if self.puede_sumar_15(mis_num + [n]): return n
        for n in self.numeros_disponibles:
            if self.puede_sumar_15(sus_num + [n]): return n
        if 5 in self.numeros_disponibles: return 5
        return random.choice(self.numeros_disponibles)

    def seleccionar(self, n, quien):
        self.numeros_disponibles.remove(n)
        if quien == "Usuario" or quien == "IA_1":
            self.numeros_jugador.append(n)
            self.botones[n].config(state="disabled", bg="#1B396B", disabledforeground="white")
        else:
            self.numeros_ia.append(n)
            self.botones[n].config(state="disabled", bg="#cc0000", disabledforeground="white")

    def puede_sumar_15(self, lista):
        return any(sum(c) == 15 for c in combinations(lista, 3))

    def verificar_ganador_total(self):
        return self.puede_sumar_15(self.numeros_jugador) or self.puede_sumar_15(self.numeros_ia)

    def verificar_partida(self, lista, msj):
        if self.puede_sumar_15(lista):
            if "IA" in msj or "IA_2" in msj: self.perdidos += 1
            else: self.ganados += 1
            self.terminar_ronda(msj)
            return True
        return False

    def terminar_ronda(self, msg):
        for btn in self.botones.values(): btn.config(state="disabled")
        self.actualizar_marcador(msg)
        self.btn_control.config(text="Siguiente Partida", command=self.nueva_partida, bg="#28a745")

    def actualizar_marcador(self, titulo):
        self.lbl_info.config(text=titulo)
        self.lbl_score.config(text=f"Ganados: {self.ganados} | Empates: {self.empates} | Perdidos: {self.perdidos}")

    def finalizar_serie(self):
        res = "¡CAMPEÓN!" if self.ganados > self.perdidos else "IA GANÓ" if self.perdidos > self.ganados else "EMPATE"
        messagebox.showinfo("Fin de Serie", f"{res}\nFinal: {self.ganados}-{self.perdidos}")
        self.cerrar()

    def cerrar(self):
        self.window.destroy()
        self.al_cerrar_callback()