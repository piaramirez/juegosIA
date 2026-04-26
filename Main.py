import tkinter as tk
from gato import GatoJuego
from puzzle15 import Puzzle15
from vim_logic import VimSim
import os

COLOR_UNAM_AZUL = "#1B396B"
COLOR_UNAM_ORO = "#D4AF37"

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistemas de IA - UNAM FES")
        self.root.geometry("400x550")
        self.root.configure(bg=COLOR_UNAM_AZUL)
        self.render_menu()

    def render_menu(self):
        for w in self.root.winfo_children(): w.destroy()
        
        
        try:
            ruta = os.path.join(os.path.dirname(__file__), 'logo_unam.png')
            self.logo = tk.PhotoImage(file=ruta)
            tk.Label(self.root, image=self.logo, bg=COLOR_UNAM_AZUL).pack(pady=20)
        except:
            tk.Label(self.root, text="[ LOGO UNAM ]", fg="white", bg=COLOR_UNAM_AZUL, font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Proyectos de IA", font=("Arial", 20, "bold"), fg="white", bg=COLOR_UNAM_AZUL).pack()
        btn_style = {
            "font": ("Arial", 12, "bold"), 
            "bg": COLOR_UNAM_ORO, 
            "fg": "white", 
            "width": 20, 
            "height": 2, 
            "bd": 3, 
            "relief": "raised"
        }
        
        # Botones Principales
        tk.Button(self.root, text="1. Jugar Gato", command=self.elegir_dificultad_gato, **btn_style).pack(pady=12)
        tk.Button(self.root, text="2. Jugar 15 (8-Puzzle)", command=self.lanzar_15, **btn_style).pack(pady=12)
        tk.Button(self.root, text="3. VIM Movement", command=self.lanzar_vim, **btn_style).pack(pady=12)

    # --- Lógica para Gato (con selección de niveles) ---
    def elegir_dificultad_gato(self):
        for w in self.root.winfo_children(): w.destroy()
        tk.Label(self.root, text="Dificultad Gato:", font=("Arial", 16, "bold"), fg="white", bg=COLOR_UNAM_AZUL).pack(pady=30)
        
        btn_dif = {"bg": COLOR_UNAM_ORO, "fg": "white", "width": 15, "font": ("Arial", 11, "bold"), "height": 2}
        
        for n, nombre in [(1, "Fácil"), (2, "Medio"), (3, "Difícil")]:
            tk.Button(self.root, text=nombre, command=lambda n=n: self.lanzar_gato(n), **btn_dif).pack(pady=8)
        
        tk.Button(self.root, text="Volver", bg="#cc0000", fg="white", font=("Arial", 10, "bold"), 
                  command=self.render_menu).pack(pady=30)

    def lanzar_gato(self, nivel):
        self.root.withdraw() 
        GatoJuego(self.root, nivel, self.regresar_al_menu)

    # --- Lógica para Puzzle 15 (La dificultad se elige dentro de su propia clase) ---
    def lanzar_15(self):
        self.root.withdraw()
        Puzzle15(self.root, self.regresar_al_menu)

    # --- Lógica para VIM ---
    def lanzar_vim(self):
        self.root.withdraw()
        VimSim(self.root, self.regresar_al_menu)

    def regresar_al_menu(self):
        self.root.deiconify() # Muestra el menú otra vez
        self.render_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()