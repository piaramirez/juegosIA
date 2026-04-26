"""
================================================================
SISTEMA DE MENÚ PRINCIPAL - PROYECTOS DE INTELIGENCIA ARTIFICIAL
================================================================
Fecha: 27 de Abril de 2026
Escuela: Universidad Nacional Autónoma de México (UNAM) Facultad de Estudios Superior Aragón
Grupo: 2907 
Materia: Inteligencia Artificial
Docente: MARTIN ROMERO UGALDE
Estudiante: Pedro Antonio Ramírez Alcántara
            Victor Omar
================================================================
Este módulo implementa el menú principal que integra tres proyectos:
- Juego del Gato 
- Puzzle 15
- Simulador de movimientos VIM
================================================================
"""

import tkinter as tk
from gato import GatoJuego
from puzzle15 import Puzzle15
from vim_logic import VimSim

# Constantes de colores institucionales de la UNAM
COLOR_UNAM_AZUL = "#1B396B"  # Azul UNAM
COLOR_UNAM_ORO = "#D4AF37"   # Oro UNAM

class MenuPrincipal:
    """
    Clase principal que gestiona el menú de la aplicación.
    Permite navegar entre los diferentes proyectos de IA.
    """
    
    def __init__(self, root):
        """
        Constructor de la clase MenuPrincipal.
        Inicializa la ventana principal y muestra el menú.
        
        Args:
            root: Ventana principal de tkinter donde se mostrará el menú
        """
        self.root = root
        self.root.title("Sistemas de IA - UNAM FES")
        self.root.geometry("400x550")
        self.root.configure(bg=COLOR_UNAM_AZUL)
        self.render_menu()

    def render_menu(self):
        """
        Renderiza el menú principal en la pantalla.
        Muestra los títulos institucionales y los botones de navegación.
        Limpia cualquier widget existente antes de renderizar.
        """
        # Elimina todos los widgets actuales para refrescar la pantalla
        for w in self.root.winfo_children():
            w.destroy()
        
        # Título institucional UNAM
        tk.Label(self.root, text="UNAM", fg=COLOR_UNAM_ORO, bg=COLOR_UNAM_AZUL, 
                font=("Arial", 36, "bold")).pack(pady=30)
        
        # Subtítulo de facultad
        tk.Label(self.root, text="FES Acatlán", fg="white", bg=COLOR_UNAM_AZUL, 
                font=("Arial", 14)).pack()
        
        # Título de la materia
        tk.Label(self.root, text="Sistemas de IA", font=("Arial", 20, "bold"), 
                fg="white", bg=COLOR_UNAM_AZUL).pack(pady=20)
        
        # Estilo común para todos los botones del menú
        btn_style = {
            "font": ("Arial", 12, "bold"),
            "bg": COLOR_UNAM_ORO,
            "fg": COLOR_UNAM_AZUL,
            "width": 25,
            "height": 2,
            "bd": 2,
            "relief": "raised"
        }
        
        # Botones de navegación a cada proyecto
        tk.Button(self.root, text="Gato", command=self.elegir_dificultad_gato, 
                 **btn_style).pack(pady=10)
        tk.Button(self.root, text="Puzzle 15", command=self.lanzar_15, 
                 **btn_style).pack(pady=10)
        tk.Button(self.root, text="VIM Movement", command=self.lanzar_vim, 
                 **btn_style).pack(pady=10)
        
        # Botón para salir de la aplicación
        tk.Button(self.root, text="Salir", command=self.root.quit, 
                 bg="#cc0000", fg="white", font=("Arial", 10, "bold"), 
                 width=15).pack(pady=30)

    def elegir_dificultad_gato(self):
        """
        Muestra la pantalla de selección de dificultad para el juego del Gato.
        Ofrece tres niveles: Fácil, Medio y Difícil.
        """
        # Limpia la pantalla actual
        for w in self.root.winfo_children():
            w.destroy()
        
        # Título de la pantalla de dificultad
        tk.Label(self.root, text="Dificultad", font=("Arial", 18, "bold"), 
                fg="white", bg=COLOR_UNAM_AZUL).pack(pady=30)
        
        # Estilo para los botones de dificultad
        btn_style = {
            "bg": COLOR_UNAM_ORO,
            "fg": COLOR_UNAM_AZUL,
            "width": 20,
            "height": 2,
            "font": ("Arial", 12, "bold")
        }
        
        # Botones para cada nivel de dificultad
        tk.Button(self.root, text="Fácil", command=lambda: self.lanzar_gato(1), 
                 **btn_style).pack(pady=10)
        tk.Button(self.root, text="Medio", command=lambda: self.lanzar_gato(2), 
                 **btn_style).pack(pady=10)
        tk.Button(self.root, text="Difícil", command=lambda: self.lanzar_gato(3), 
                 **btn_style).pack(pady=10)
        
        # Botón para regresar al menú principal
        tk.Button(self.root, text="Volver", command=self.render_menu, 
                 bg="#555", fg="white", font=("Arial", 10, "bold"), 
                 width=15).pack(pady=30)

    def lanzar_gato(self, nivel):
        """
        Lanza el juego del Gato con la dificultad seleccionada.
        
        Args:
            nivel (int): Nivel de dificultad (1=Fácil, 2=Medio, 3=Difícil)
        """
        self.root.withdraw()  # Oculta la ventana del menú
        GatoJuego(self.root, nivel, self.regresar_al_menu)

    def lanzar_15(self):
        """
        Lanza el juego del Puzzle 15 (8-Puzzle).
        """
        self.root.withdraw()  # Oculta la ventana del menú
        Puzzle15(self.root, self.regresar_al_menu)

    def lanzar_vim(self):
        """
        Lanza el simulador de movimientos VIM.
        """
        self.root.withdraw()  # Oculta la ventana del menú
        VimSim(self.root, self.regresar_al_menu)

    def regresar_al_menu(self):
        """
        Función callback que regresa al menú principal.
        Se ejecuta cuando un juego termina y el usuario quiere volver.
        """
        self.root.deiconify()  # Muestra nuevamente la ventana del menú
        self.render_menu()     # Renderiza el menú principal

# Punto de entrada principal de la aplicación
if __name__ == "__main__":
    root = tk.Tk()                     # Crea la ventana raíz de tkinter
    app = MenuPrincipal(root)          # Inicializa el menú principal
    root.mainloop()                    # Inicia el bucle principal de la interfaz