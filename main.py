import tkinter as tk
from database import Database
from gui import GestoreSpeseGUI
import sys
import os

def resource_path(relative_path):
    """Ottiene il percorso assoluto per le risorse"""
    try:
        # PyInstaller crea una cartella temp e memorizza il percorso in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    # Ottimizza l'avvio di matplotlib
    import matplotlib
    matplotlib.use('TkAgg')
    
    # Crea la finestra principale
    root = tk.Tk()
    
    # Imposta la priorità del processo
    try:
        import psutil
        p = psutil.Process()
        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except:
        pass
    
    # Inizializza il database
    db = Database()
    
    # Crea l'interfaccia grafica
    app = GestoreSpeseGUI(root, db)
    
    # Configura il ridimensionamento della finestra
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    # Avvia l'applicazione
    root.mainloop()

if __name__ == "__main__":
    main() 