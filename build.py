import os
import subprocess
import shutil
from datetime import datetime

def esegui_comando(comando):
    """Esegue un comando e restituisce l'output"""
    try:
        risultato = subprocess.run(comando, shell=True, check=True, capture_output=True, text=True)
        return True, risultato.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Errore: {e.stderr}"

def pulisci_cartelle():
    """Pulisce le cartelle di build e dist"""
    cartelle_da_pulire = ['build', 'dist']
    for cartella in cartelle_da_pulire:
        if os.path.exists(cartella):
            shutil.rmtree(cartella)
            print(f"Cartella {cartella} pulita")

def crea_zip():
    """Crea un file zip della cartella dist"""
    data_attuale = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_zip = f"GestoreSpese_{data_attuale}.zip"
    
    if os.path.exists("dist"):
        shutil.make_archive(f"GestoreSpese_{data_attuale}", 'zip', "dist")
        print(f"Creato file {nome_zip}")
        return nome_zip
    return None

def main():
    print("=== Inizio processo di build ===")
    
    # 1. Pulisci le cartelle precedenti
    print("\n1. Pulizia cartelle...")
    pulisci_cartelle()
    
    # 2. Esegui PyInstaller
    print("\n2. Generazione file .exe...")
    successo, output = esegui_comando("pyinstaller GestoreSpese.spec --clean")
    if not successo:
        print("Errore durante la generazione del file .exe")
        print(output)
        return
    
    # 3. Crea il file zip
    print("\n3. Creazione file zip...")
    nome_zip = crea_zip()
    if not nome_zip:
        print("Errore durante la creazione del file zip")
        return
    
    # 4. Commit e push su GitHub
    print("\n4. Caricamento su GitHub...")
    comandi_git = [
        "git add .",
        f'git commit -m "Build automatica: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"',
        "git push"
    ]
    
    for comando in comandi_git:
        successo, output = esegui_comando(comando)
        if not successo:
            print(f"Errore durante l'esecuzione di: {comando}")
            print(output)
            return
    
    print("\n=== Processo completato con successo! ===")
    print(f"File .exe generato in: dist/Gestore Spese.exe")
    print(f"File zip creato: {nome_zip}")

if __name__ == "__main__":
    main() 