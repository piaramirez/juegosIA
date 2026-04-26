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
        
        # Variables de la serie y configuración
        self.ganados = 0
        self.perdidos = 0
        self.juegos_totales = 0
        self.dificultad = 1
        
        # Valores que el usuario podrá cambiar
        self.v_inicial = 100
        self.v_objetivo = 0
        self.r_min = 1
        self.r_max = 7
        self.valor_actual = 100
        
        self.setup_ui_niveles()

    def setup_ui_niveles(self):
        """Paso 1: Selección de Dificultad"""
        for w in self.window.winfo_children(): w.destroy()
        
        tk.Label(self.window, text="NIVEL DE IA", font=("Arial", 20, "bold"), 
                 fg="#D4AF37", bg="#1B396B").pack(pady=50)

        btn_style = {"font": ("Arial", 12, "bold"), "bg": "#D4AF37", "fg": "white", "width": 22, "height": 2}
        
        tk.Button(self.window, text="Fácil (Azar)", command=lambda: self.ir_a_config(1), **btn_style).pack(pady=10)
        tk.Button(self.window, text="Medio (Estratégico)", command=lambda: self.ir_a_config(2), **btn_style).pack(pady=10)
        tk.Button(self.window, text="Difícil (Invencible)", command=lambda: self.ir_a_config(3), **btn_style).pack(pady=10)
        
        tk.Button(self.window, text="Cerrar", bg="#cc0000", fg="white", command=self.cerrar).pack(pady=40)

    def ir_a_config(self, nivel):
        self.dificultad = nivel
        self.setup_ui_configuracion()

    def setup_ui_configuracion(self):
        """Paso 2: Ingreso de cualquier valor (Total, Objetivo, Restas)"""
        for w in self.window.winfo_children(): w.destroy()
        
        tk.Label(self.window, text="CONFIGURAR VALORES", font=("Arial", 18, "bold"), 
                 fg="#D4AF37", bg="#1B396B").pack(pady=20)

        f_inputs = tk.Frame(self.window, bg="#1B396B")
        f_inputs.pack(pady=10)

        def crear_campo(txt, default):
            tk.Label(f_inputs, text=txt, fg="white", bg="#1B396B", font=("Arial", 10)).pack()
            e = tk.Entry(f_inputs, justify="center", font=("Arial", 12), width=25)
            e.insert(0, default)
            e.pack(pady=8)
            return e

        # Aquí el usuario puede meter CUALQUIER valor
        self.ent_inicial = crear_campo("Valor Inicial (Total a restar):", str(self.v_inicial))
        self.ent_objetivo = crear_campo("Valor Objetivo (Llegar a):", str(self.v_objetivo))
        self.ent_min = crear_campo("Resta Mínima:", str(self.r_min))
        self.ent_max = crear_campo("Resta Máxima:", str(self.r_max))

        tk.Button(self.window, text="INICIAR SERIE DE 5", font=("Arial", 13, "bold"), 
                  bg="#28a745", fg="white", width=25, height=2, command=self.validar_y_empezar).pack(pady=30)
        
        tk.Button(self.window, text="Volver a Niveles", bg="#D4AF37", fg="white", command=self.setup_ui_niveles).pack()

    def validar_y_empezar(self):
        try:
            self.v_inicial = int(self.ent_inicial.get())
            self.v_objetivo = int(self.ent_objetivo.get())
            self.r_min = int(self.ent_min.get())
            self.r_max = int(self.ent_max.get())
            
            if self.r_min >= self.r_max or (self.v_inicial <= self.v_objetivo):
                messagebox.showerror("Error", "Valores inválidos. El inicio debe ser mayor al objetivo y min < max.")
                return
            
            self.ganados = self.perdidos = self.juegos_totales = 0
            self.preparar_interfaz_juego()
            self.nueva_partida()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa solo números enteros.")

    def preparar_interfaz_juego(self):
        for w in self.window.winfo_children(): w.destroy()
        
        # Encabezado con marcador
        self.lbl_info = tk.Label(self.window, text="", font=("Arial", 14, "bold"), fg="#D4AF37", bg="#1B396B")
        self.lbl_info.pack(pady=10)
        self.lbl_score = tk.Label(self.window, text="", font=("Arial", 11), fg="white", bg="#1B396B")
        self.lbl_score.pack()

        # Número actual gigante
        self.lbl_valor = tk.Label(self.window, text=str(self.v_inicial), font=("Arial", 65, "bold"), fg="white", bg="#1B396B")
        self.lbl_valor.pack(pady=10)

        # Historial de operaciones (para que el profe vea las restas)
        tk.Label(self.window, text="Registro de jugadas:", fg="white", bg="#1B396B", font=("Arial", 9)).pack()
        self.txt_historial = tk.Text(self.window, height=10, width=48, font=("Courier", 10), bg="#0D1B2E", fg="#00FF00")
        self.txt_historial.pack(pady=10)
        
        # Botones de resta dinámicos
        self.btn_frame = tk.Frame(self.window, bg="#1B396B")
        self.btn_frame.pack(pady=10)
        self.botones = []
        
        # Se muestran botones representativos si el rango es enorme
        rango = list(range(self.r_min, self.r_max + 1))
        paso = max(1, len(rango) // 7)
        for i in rango[::paso]:
            btn = tk.Button(self.btn_frame, text=f"-{i}", width=6, bg="#D4AF37", font=("Arial", 10, "bold"),
                            command=lambda v=i: self.jugada_usuario(v))
            btn.grid(row=0, column=len(self.botones), padx=4)
            self.botones.append(btn)

        self.btn_control = tk.Button(self.window, text="Abandonar", bg="#cc0000", fg="white", width=20, command=self.setup_ui_niveles)
        self.btn_control.pack(pady=20)

    def nueva_partida(self):
        if self.juegos_totales >= 5:
            self.finalizar_serie()
            return
        self.juegos_totales += 1
        self.valor_actual = self.v_inicial
        self.lbl_valor.config(text=str(self.valor_actual))
        self.txt_historial.delete('1.0', tk.END)
        self.txt_historial.insert(tk.END, f">>> INICIO PARTIDA {self.juegos_totales} de 5\n")
        self.actualizar_marcador(f"PARTIDA {self.juegos_totales} DE 5")
        for b in self.botones: b.config(state="normal")
        self.btn_control.config(text="Abandonar", bg="#cc0000", command=self.setup_ui_niveles)

    def jugada_usuario(self, v):
        self.valor_actual -= v
        self.log(f"[TÚ] Restaste {v}. Quedan: {self.valor_actual}")
        self.lbl_valor.config(text=str(self.valor_actual))
        
        if self.valor_actual <= self.v_objetivo:
            self.perdidos += 1
            self.terminar_ronda("¡Llegaste al objetivo! Punto para la IA.")
        else:
            for b in self.botones: b.config(state="disabled")
            self.window.after(600, self.jugada_ia)

    def jugada_ia(self):
        # Lógica de IA adaptada a cualquier valor
        distancia = self.valor_actual - self.v_objetivo
        
        if self.dificultad == 1:
            r = random.randint(self.r_min, min(self.r_max, distancia))
        else:
            # Estrategia de Nim adaptable
            ciclo = self.r_min + self.r_max
            objetivo_nim = (distancia - self.r_min) % ciclo
            
            if self.r_min <= objetivo_nim <= self.r_max:
                r = objetivo_nim
            else:
                r = self.r_min if self.dificultad == 3 else random.randint(self.r_min, self.r_max)
        
        r = min(r, distancia) # No restar más de lo que queda
        self.valor_actual -= r
        self.log(f"[IA] Restó {r}. Quedan: {self.valor_actual}")
        self.lbl_valor.config(text=str(self.valor_actual))
        
        if self.valor_actual <= self.v_objetivo:
            self.ganados += 1
            self.terminar_ronda("¡La IA llegó al objetivo! Punto para ti.")
        else:
            for b in self.botones: b.config(state="normal")

    def log(self, msj):
        self.txt_historial.insert(tk.END, f"{msj}\n")
        self.txt_historial.see(tk.END)

    def terminar_ronda(self, msg):
        for b in self.botones: b.config(state="disabled")
        self.actualizar_marcador(msg)
        self.btn_control.config(text="Siguiente Juego", bg="#28a745", command=self.nueva_partida)

    def actualizar_marcador(self, titulo):
        self.lbl_info.config(text=titulo)
        self.lbl_score.config(text=f"Tus Puntos: {self.ganados} | Puntos IA: {self.perdidos}")

    def finalizar_serie(self):
        res = "¡CAMPEÓN DE LA SERIE!" if self.ganados > self.perdidos else "LA IA GANÓ LA SERIE" if self.perdidos > self.ganados else "HUBO EMPATE FINAL"
        messagebox.showinfo("Fin de la Serie", f"{res}\nResultado Final: {self.ganados} - {self.perdidos}")
        self.setup_ui_niveles()

    def cerrar(self):
        self.window.destroy()
        self.al_cerrar_callback()