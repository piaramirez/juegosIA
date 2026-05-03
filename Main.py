"""
================================================================
SISTEMA DE MENÚ PRINCIPAL - PROYECTOS DE INTELIGENCIA ARTIFICIAL
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
Este módulo implementa el menú principal que integra los tres
proyectos obligatorios requeridos:
P01 - Juego del Gato
P02 - Juego del Quince (Puzzle 15)
P03 - Juego de NIM (Simulador VIM)
================================================================
"""

import tkinter as tk
from gato import GatoJuego
from puzzle15 import Puzzle15
# Asumiendo que vim_logic.py contiene la lógica del Juego de NIM (P03)
from vim_logic import VimSim

# Constantes de colores institucionales de la UNAM
COLOR_UNAM_AZUL = "#1B396B"  # Azul UNAM
COLOR_UNAM_ORO = "#D4AF37"   # Oro UNAM

class MenuPrincipal:
    """
    Clase principal que gestiona el menú de la aplicación.
    Permite navegar entre los diferentes proyectos de IA (P01, P02, P03).
    """
    
    def __init__(self, root):
        """
        Constructor de la clase MenuPrincipal.
        Inicializa la ventana principal y muestra el menú.
        
        Args:
            root: Ventana principal de tkinter donde se mostrará el menú
        """
        self.root = root
        self.root.title("Sistemas de IA - UNAM FES Aragón")
        self.root.geometry("400x600") # Aumentado ligeramente para acomodar textos
        self.root.configure(bg=COLOR_UNAM_AZUL)
        self.render_menu()

    def render_menu(self):
        """
        Renderiza el menú principal en la pantalla.
        Muestra los títulos institucionales y los botones de navegación.
        Limpiará cualquier widget existente antes de renderizar.
        """
        # Elimina todos los widgets actuales para refrescar la pantalla (limpiar trazas de submenús)
        for w in self.root.winfo_children():
            w.destroy()
        
        # Título institucional UNAM
        tk.Label(self.root, text="UNAM", fg=COLOR_UNAM_ORO, bg=COLOR_UNAM_AZUL, 
                font=("Arial", 36, "bold")).pack(pady=(30, 10))
        
        # Subtítulo de facultad - CORREGIDO A FES ARAGÓN
        tk.Label(self.root, text="FES Aragón", fg="white", bg=COLOR_UNAM_AZUL, 
                font=("Arial", 16, "bold")).pack()
        
        # Título de la materia
        tk.Label(self.root, text="Sistemas de IA", font=("Arial", 20, "bold"), 
                fg="white", bg=COLOR_UNAM_AZUL).pack(pady=20)
        
        # Estilo común para todos los botones del menú (P01, P02, P03)
        btn_style = {
            "font": ("Arial", 12, "bold"),
            "bg": COLOR_UNAM_ORO,
            "fg": COLOR_UNAM_AZUL,
            "width": 30, # Ligeramente más ancho
            "height": 2,
            "bd": 3,
            "relief": "raised",
            "cursor": "hand2" # Cambia el cursor al pasar sobre el botón
        }
        
        # Botones de navegación a cada proyecto con nomenclatura oficial
        tk.Button(self.root, text="P01 - Juego del Gato", command=self.elegir_dificultad_gato, 
                 **btn_style).pack(pady=10)
        
        tk.Button(self.root, text="P02 - Juego del Quince", command=self.lanzar_15, 
                 **btn_style).pack(pady=10)
        
        # Se asume que VIM implementa la lógica de NIM requerida
        tk.Button(self.root, text="P03 - Juego de NIM", command=self.lanzar_nim, 
                 **btn_style).pack(pady=10)
        
        # Botón para salir de la aplicación
        tk.Button(self.root, text="Salir del Sistema", command=self.root.quit, 
                 bg="#cc0000", fg="white", font=("Arial", 10, "bold"), 
                 width=20, height=1).pack(pady=40)

    def elegir_dificultad_gato(self):
        """
        Muestra la pantalla de selección de dificultad para el juego del Gato (P01).
        Ofrece tres niveles: Fácil, Medio y Difícil que alteran el algoritmo de IA.
        """
        # Limpia la pantalla actual
        for w in self.root.winfo_children():
            w.destroy()
        
        # Título de la pantalla de dificultad
        tk.Label(self.root, text="Seleccione Dificultad (Gato)", font=("Arial", 16, "bold"), 
                fg="white", bg=COLOR_UNAM_AZUL).pack(pady=30)
        
        # Estilo para los botones de dificultad
        btn_style_diff = {
            "bg": COLOR_UNAM_ORO,
            "fg": COLOR_UNAM_AZUL,
            "width": 20,
            "height": 2,
            "font": ("Arial", 12, "bold"),
            "bd": 2,
            "relief": "groove"
        }
        
        # Botones para cada nivel de dificultad invocando la IA correspondiente
        tk.Button(self.root, text="Fácil (Aleatorio)", command=lambda: self.lanzar_gato(1), 
                 **btn_style_diff).pack(pady=10)
        tk.Button(self.root, text="Medio (Bloqueo)", command=lambda: self.lanzar_gato(2), 
                 **btn_style_diff).pack(pady=10)
        tk.Button(self.root, text="Difícil (Minimax)", command=lambda: self.lanzar_gato(3), 
                 **btn_style_diff).pack(pady=10)
        
        # Botón para regresar al menú principal
        tk.Button(self.root, text="Volver al Menú", command=self.render_menu, 
                 bg="#555", fg="white", font=("Arial", 10, "bold"), 
                 width=15).pack(pady=40)

    def lanzar_gato(self, nivel):
        """
        Lanza la interfaz del juego del Gato (P01) con la dificultad seleccionada.
        
        Args:
            nivel (int): Nivel de dificultad (1=Fácil, 2=Medio, 3=Difícil)
        """
        self.root.withdraw()  # Oculta temporalmente la ventana del menú principal
        # Se instancia la clase importada pasando el callback de retorno
        GatoJuego(self.root, nivel, self.regresar_al_menu)

    def lanzar_15(self):
        """
        Lanza la interfaz del juego del Quince (P02 - Puzzle 15).
        Oculta el menú y cede el control a la clase Puzzle15.
        """
        self.root.withdraw() 
        Puzzle15(self.root, self.regresar_al_menu)

    def lanzar_nim(self):
        """
        Lanza la interfaz del Juego de NIM (P03).
        Utiliza la lógica implementada en VimSim.
        Oculta el menú y cede el control.
        """
        self.root.withdraw()
        # Se asume que VimSim es la implementación de NIM
        VimSim(self.root, self.regresar_al_menu)

    def regresar_al_menu(self):
        """
        Función de callback destinada a ser usada por los subprogramas (P01, P02, P03).
        Cierra la ventana del juego actual, muestra la del menú principal y la re-renderiza.
        """
        self.root.deiconify()  # Muestra nuevamente la ventana del menú
        self.render_menu()     # Fuerza el redibujado del menú principal

# ================================================================
# Punto de entrada principal de la aplicación
# ================================================================
if __name__ == "__main__":
    # 1. Crear la instancia raíz de Tkinter (la ventana base)
    root = tk.Tk() 
    
    # 2. Instanciar nuestra clase MenuPrincipal, pasando la raíz
    # Esto ejecuta el constructor __init__ y render_menu()
    app = MenuPrincipal(root) 
    
    # 3. Iniciar el bucle de eventos infinito (mainloop). 
    # Mantiene la ventana abierta y escuchando clics/teclas.
    root.mainloop()