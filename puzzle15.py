import tkinter as tk
from tkinter import messagebox
import random
from itertools import combinations

class Puzzle15:
    def __init__(self, parent, al_cerrar):
        self.window = tk.Toplevel(parent)
        self.window.title("Suma 15 IA - UNAM FES")
        self.window.geometry("450x750")
        self.window.configure(bg="#1B396B")
        
        self.al_cerrar_callback = al_cerrar
        
        # Variables de la serie
        self.ganados = 0
        self.perdidos = 0
        self.empates = 0
        self.juegos_totales = 0
        self.dificultad = 1
        
        # Variables de la partida
        self.numeros_disponibles = []
        self.numeros_jugador = []
        self.numeros_ia = []
        self.turno_jugador = True
        
        self.setup_ui_seleccion()

    def setup_ui_seleccion(self):
        for w in self.window.winfo_children(): w.destroy()
        tk.Label(self.window, text="Dificultad Suma 15", font=("Arial", 20, "bold"), 
                 fg="#D4AF37", bg="#1B396B").pack(pady=40)
        
        btn_style = {"font": ("Arial", 12, "bold"), "bg": "#D4AF37", "fg": "white", "width": 18, "height": 2}
        
        tk.Button(self.window, text="Fácil (IA Azar)", command=lambda: self.iniciar_serie(1), **btn_style).pack(pady=10)
        tk.Button(self.window, text="Medio (IA Bloquea)", command=lambda: self.iniciar_serie(2), **btn_style).pack(pady=10)
        tk.Button(self.window, text="Difícil (IA Pro)", command=lambda: self.iniciar_serie(3), **btn_style).pack(pady=10)
        
        tk.Button(self.window, text="Volver", bg="#cc0000", fg="white", command=self.cerrar).pack(pady=30)

    def iniciar_serie(self, dif):
        self.dificultad = dif
        self.ganados = 0
        self.perdidos = 0
        self.empates = 0
        self.juegos_totales = 0
        self.preparar_interfaz_juego()
        self.nueva_partida()

    def preparar_interfaz_juego(self):
        for w in self.window.winfo_children(): w.destroy()
        
        self.lbl_info = tk.Label(self.window, text="", font=("Arial", 14, "bold"), fg="#D4AF37", bg="#1B396B")
        self.lbl_info.pack(pady=10)
        
        self.lbl_score = tk.Label(self.window, text="", font=("Arial", 11), fg="white", bg="#1B396B")
        self.lbl_score.pack()

        # Tablero 3x3
        self.grid_frame = tk.Frame(self.window, bg="#1B396B")
        self.grid_frame.pack(pady=15)
        
        self.botones = {}
        for i in range(1, 10):
            btn = tk.Button(self.grid_frame, text=str(i), font=("Arial", 18, "bold"), 
                            width=6, height=3, bg="#D4AF37", fg="white",
                            command=lambda n=i: self.jugada_usuario(n))
            btn.grid(row=(i-1)//3, column=(i-1)%3, padx=5, pady=5)
            self.botones[i] = btn
            
        # Panel de sumas actuales
        self.sumas_frame = tk.Frame(self.window, bg="#1B396B", bd=1, relief="sunken")
        self.sumas_frame.pack(pady=10, fill="x", padx=40)
        
        self.lbl_tus_num = tk.Label(self.sumas_frame, text="Tus números: []", font=("Arial", 10), fg="white", bg="#1B396B")
        self.lbl_tus_num.pack()
        self.lbl_ia_num = tk.Label(self.sumas_frame, text="IA números: []", font=("Arial", 10), fg="#D4AF37", bg="#1B396B")
        self.lbl_ia_num.pack()

        self.btn_control = tk.Button(self.window, text="Abandonar", bg="#cc0000", fg="white", 
                                      font=("Arial", 10, "bold"), width=20, height=2, command=self.cerrar)
        self.btn_control.pack(pady=20)

    def nueva_partida(self):
        if self.juegos_totales >= 5:
            self.finalizar_serie()
            return
            
        self.juegos_totales += 1
        self.numeros_disponibles = list(range(1, 10))
        self.numeros_jugador = []
        self.numeros_ia = []
        self.turno_jugador = True
        
        self.actualizar_marcador(f"PARTIDA {self.juegos_totales} DE 5")
        for btn in self.botones.values():
            btn.config(state="normal", bg="#D4AF37")
        
        self.lbl_tus_num.config(text="Tus números: []")
        self.lbl_ia_num.config(text="IA números: []")
        self.btn_control.config(text="Abandonar", bg="#cc0000", command=self.cerrar)

    def jugada_usuario(self, n):
        if n in self.numeros_disponibles and self.turno_jugador:
            self.seleccionar(n, "Usuario")
            self.lbl_tus_num.config(text=f"Tus números: {self.numeros_jugador}")
            
            if not self.verificar_partida(self.numeros_jugador, "¡Ganaste!"):
                if not self.numeros_disponibles:
                    self.empates += 1
                    self.terminar_ronda("¡EMPATE!")
                else:
                    self.turno_jugador = False
                    self.window.after(600, self.jugada_ia)

    def jugada_ia(self):
        n = self.inteligencia_ia()
        self.seleccionar(n, "IA")
        self.lbl_ia_num.config(text=f"IA números: {self.numeros_ia}")
        
        if not self.verificar_partida(self.numeros_ia, "La IA ganó"):
            if not self.numeros_disponibles:
                self.empates += 1
                self.terminar_ronda("¡EMPATE!")
            else:
                self.turno_jugador = True

    def inteligencia_ia(self):
        # 1. Ganar
        for n in self.numeros_disponibles:
            if self.puede_sumar_15(self.numeros_ia + [n]): return n
        # 2. Bloquear
        if self.dificultad >= 2:
            for n in self.numeros_disponibles:
                if self.puede_sumar_15(self.numeros_jugador + [n]): return n
        return random.choice(self.numeros_disponibles)

    def seleccionar(self, n, quien):
        self.numeros_disponibles.remove(n)
        if quien == "Usuario":
            self.numeros_jugador.append(n)
            self.botones[n].config(state="disabled", bg="#1B396B")
        else:
            self.numeros_ia.append(n)
            self.botones[n].config(state="disabled", bg="#cc0000")

    def puede_sumar_15(self, lista):
        return any(sum(c) == 15 for c in combinations(lista, 3))

    def verificar_partida(self, lista, msj):
        if self.puede_sumar_15(lista):
            if "IA" in msj or "La IA" in msj: self.perdidos += 1
            else: self.ganados += 1
            self.terminar_ronda(msj)
            return True
        return False

    def terminar_ronda(self, msg):
        for btn in self.botones.values(): btn.config(state="disabled")
        self.actualizar_marcador(msg)
        self.btn_control.config(text="Siguiente Juego", command=self.nueva_partida, bg="#28a745")

    def actualizar_marcador(self, titulo):
        self.lbl_info.config(text=titulo)
        self.lbl_score.config(text=f"G: {self.ganados} | E: {self.empates} | P: {self.perdidos}")

    def finalizar_serie(self):
        res = "¡CAMPEÓN!" if self.ganados > self.perdidos else "IA GANÓ" if self.perdidos > self.ganados else "EMPATE"
        messagebox.showinfo("Fin", f"{res}\nFinal: {self.ganados}-{self.empates}-{self.perdidos}")
        self.cerrar()

    def cerrar(self):
        self.window.destroy()
        self.al_cerrar_callback()