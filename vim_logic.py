"""
================================================================
P03 - SIMULADOR VIM (JUEGO DE RESTA CONFIGURABLE)
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

class VimSim:
    def __init__(self, parent, al_cerrar):
        self.window = tk.Toplevel(parent)
        self.window.title("VIM IA - UNAM FES")
        self.window.geometry("500x850")
        self.window.configure(bg="#1B396B")
        
        self.al_cerrar_callback = al_cerrar
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar)
        
        self.ganados = 0
        self.perdidos = 0
        self.juegos_totales = 0
        self.dificultad = 1
        self.modo_inicio = None 
        
        # Variables de lógica
        self.valor_actual = 100
        self.v_objetivo = 0
        self.r_min = 1
        self.r_max = 7
        
        self.setup_ui_base()
        self.seleccionar_dificultad()

    def setup_ui_base(self):
        self.container = tk.Frame(self.window, bg="#1B396B")
        self.container.pack(expand=True, fill="both", pady=20)

    def seleccionar_dificultad(self):
        for w in self.container.winfo_children(): w.destroy()
        
        tk.Label(self.container, text="VIM: SELECCIONE NIVEL", font=("Arial", 16, "bold"), 
                 fg="#D4AF37", bg="#1B396B").pack(pady=20)
        
        btn_style = {"font": ("Arial", 12, "bold"), "bg": "#D4AF37", "fg": "#1B396B", "width": 20, "pady": 10}
        
        tk.Button(self.container, text="Fácil (Azar)", command=lambda: self.set_dif(1), **btn_style).pack(pady=10)
        tk.Button(self.container, text="Medio (IA Bloquea)", command=lambda: self.set_dif(2), **btn_style).pack(pady=10)
        tk.Button(self.container, text="Difícil (IA Pro)", command=lambda: self.set_dif(3), **btn_style).pack(pady=10)

    def set_dif(self, d):
        self.dificultad = d
        self.seleccionar_quien_inicia()

    def seleccionar_quien_inicia(self):
        for w in self.container.winfo_children(): w.destroy()
        
        tk.Label(self.container, text="¿QUIÉN INICIA?", font=("Arial", 16, "bold"), 
                 fg="#D4AF37", bg="#1B396B").pack(pady=20)
        
        btn_style = {"font": ("Arial", 12, "bold"), "bg": "#D4AF37", "fg": "#1B396B", "width": 20, "pady": 10}
        
        tk.Button(self.container, text="Yo inicio", command=lambda: self.pantalla_config(1), **btn_style).pack(pady=10)
        tk.Button(self.container, text="Inicia IA", command=lambda: self.pantalla_config(2), **btn_style).pack(pady=10)
        tk.Button(self.container, text="IA vs IA", command=lambda: self.pantalla_config(3), **btn_style).pack(pady=10)

    def pantalla_config(self, modo):
        self.modo_inicio = modo
        for w in self.container.winfo_children(): w.destroy()
        
        tk.Label(self.container, text="CONFIGURAR VALORES", font=("Arial", 20, "bold"), 
                 fg="#D4AF37", bg="#1B396B").pack(pady=20)
        
        lbl_style = {"fg": "white", "bg": "#1B396B", "font": ("Arial", 11)}
        entry_style = {"font": ("Arial", 12), "justify": "center", "width": 30}
        
        # Campos editables
        tk.Label(self.container, text="Valor Inicial (Total a restar):", **lbl_style).pack(pady=(10,0))
        self.ent_inicial = tk.Entry(self.container, **entry_style)
        self.ent_inicial.insert(0, "100")
        self.ent_inicial.pack(pady=5)
        
        tk.Label(self.container, text="Valor Objetivo (Llegar a):", **lbl_style).pack(pady=(10,0))
        self.ent_objetivo = tk.Entry(self.container, **entry_style)
        self.ent_objetivo.insert(0, "0")
        self.ent_objetivo.pack(pady=5)
        
        tk.Label(self.container, text="Resta Mínima:", **lbl_style).pack(pady=(10,0))
        self.ent_min = tk.Entry(self.container, **entry_style)
        self.ent_min.insert(0, "1")
        self.ent_min.pack(pady=5)
        
        tk.Label(self.container, text="Resta Máxima:", **lbl_style).pack(pady=(10,0))
        self.ent_max = tk.Entry(self.container, **entry_style)
        self.ent_max.insert(0, "7")
        self.ent_max.pack(pady=5)
        
        tk.Button(self.container, text="INICIAR SERIE DE 5", bg="#28a745", fg="white",
                  font=("Arial", 14, "bold"), height=2, width=25, 
                  command=self.validar_e_iniciar).pack(pady=40)
        
        tk.Button(self.container, text="Volver a Niveles", bg="#D4AF37", fg="#1B396B",
                  command=self.seleccionar_dificultad).pack()

    def validar_e_iniciar(self):
        try:
            self.v_inicial = int(self.ent_inicial.get())
            self.v_objetivo = int(self.ent_objetivo.get())
            self.r_min = int(self.ent_min.get())
            self.r_max = int(self.ent_max.get())
            
            if self.r_min >= self.r_max or self.v_inicial <= self.v_objetivo:
                raise ValueError
            
            self.comenzar_juego()
        except ValueError:
            messagebox.showerror("Error", "Revisa que los valores sean lógicos (Inic > Obj, Min < Max)")

    def comenzar_juego(self):
        for w in self.container.winfo_children(): w.destroy()
        
        self.valor_actual = self.v_inicial
        
        self.lbl_marcador = tk.Label(self.container, text=f"Ganados: {self.ganados} | Perdidos: {self.perdidos}", 
                                    fg="white", bg="#1B396B", font=("Arial", 12))
        self.lbl_marcador.pack()
        
        self.lbl_num = tk.Label(self.container, text=str(self.valor_actual), 
                               font=("Arial", 80, "bold"), fg="white", bg="#1B396B")
        self.lbl_num.pack(pady=40)
        
        # Generar botones de resta dinámicos según lo que el usuario metió
        self.f_btns = tk.Frame(self.container, bg="#1B396B")
        self.f_btns.pack(pady=20)
        
        self.btns_resta = []
        for i in range(self.r_min, self.r_max + 1):
            b = tk.Button(self.f_btns, text=f"-{i}", width=4, font=("Arial", 12, "bold"),
                          bg="#D4AF37", fg="#1B396B", command=lambda v=i: self.jugada_user(v))
            b.grid(row=0, column=i-self.r_min, padx=2)
            self.btns_resta.append(b)
            
        if self.modo_inicio == 2: self.window.after(800, self.turno_ia)
        elif self.modo_inicio == 3: self.window.after(800, self.duelo_ias)

    def jugada_user(self, v):
        self.valor_actual -= v
        self.actualizar_vista()
        if not self.check_end("¡GANASTE!"):
            self.bloquear_btns(True)
            self.window.after(800, self.turno_ia)

    def turno_ia(self):
        if self.valor_actual <= self.v_objetivo: return
        v = self.calc_ia()
        self.valor_actual -= v
        self.actualizar_vista()
        if not self.check_end("IA GANÓ"):
            self.bloquear_btns(False)

    def calc_ia(self):
        # Estrategia matemática adaptada a los valores del usuario
        # El ciclo ganador es (Max + Min)
        ciclo = self.r_max + self.r_min
        if self.dificultad == 3:
            distancia = self.valor_actual - self.v_objetivo
            res = distancia % ciclo
            if res >= self.r_min and res <= self.r_max: return res
        
        if self.dificultad >= 2:
            if (self.valor_actual - self.v_objetivo) <= self.r_max:
                return (self.valor_actual - self.v_objetivo)
                
        return random.randint(self.r_min, min(self.r_max, self.valor_actual - self.v_objetivo))

    def duelo_ias(self):
        if self.valor_actual > self.v_objetivo:
            v = self.calc_ia()
            self.valor_actual -= v
            self.actualizar_vista()
            if self.valor_actual <= self.v_objetivo:
                self.perdidos += 1
                self.finalizar_ronda("IA GANÓ SIMULACIÓN")
            else:
                self.window.after(800, self.duelo_ias)

    def actualizar_vista(self):
        if self.valor_actual < self.v_objetivo: self.valor_actual = self.v_objetivo
        self.lbl_num.config(text=str(self.valor_actual))

    def check_end(self, m):
        if self.valor_actual <= self.v_objetivo:
            if "IA" in m: self.perdidos += 1
            else: self.ganados += 1
            self.finalizar_ronda(m)
            return True
        return False

    def bloquear_btns(self, b):
        estado = "disabled" if b else "normal"
        for btn in self.btns_resta: btn.config(state=estado)

    def finalizar_ronda(self, m):
        self.juegos_totales += 1
        messagebox.showinfo("Ronda", m)
        if self.juegos_totales < 5:
            self.comenzar_juego()
        else:
            final = "¡CAMPEÓN!" if self.ganados > self.perdidos else "IA GANÓ"
            messagebox.showinfo("Fin", f"{final}\n{self.ganados} - {self.perdidos}")
            self.cerrar()

    def cerrar(self):
        self.window.destroy()
        self.al_cerrar_callback()