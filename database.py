import sqlite3
from datetime import datetime
import os
import sys

class Database:
    def __init__(self):
        # Ottieni il percorso della cartella dell'eseguibile
        if getattr(sys, 'frozen', False):
            # Se l'applicazione è eseguita come eseguibile
            application_path = os.path.dirname(sys.executable)
        else:
            # Se l'applicazione è eseguita come script Python
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        self.db_path = os.path.join(application_path, 'transazioni.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Crea le tabelle necessarie se non esistono"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transazioni (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                descrizione TEXT NOT NULL,
                importo REAL NOT NULL,
                tipo TEXT NOT NULL,
                anno INTEGER NOT NULL,
                mese INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
    
    def get_prossimo_id(self):
        """Ottiene il prossimo ID disponibile, riutilizzando gli ID eliminati"""
        # Ottieni l'ID massimo attuale
        self.cursor.execute('SELECT MAX(id) FROM transazioni')
        max_id = self.cursor.fetchone()[0] or 0
        
        # Cerca il primo ID disponibile
        for id in range(1, max_id + 1):
            self.cursor.execute('SELECT id FROM transazioni WHERE id = ?', (id,))
            if not self.cursor.fetchone():
                return id
        
        # Se non ci sono ID disponibili, usa il successivo all'ultimo
        return max_id + 1
    
    def aggiungi_transazione(self, data, descrizione, importo, tipo):
        """Aggiunge una nuova transazione al database"""
        # Converti la data in oggetto datetime
        data_obj = datetime.strptime(data, '%d-%m-%Y')
        
        # Ottieni il prossimo ID disponibile
        id_transazione = self.get_prossimo_id()
        
        self.cursor.execute('''
            INSERT INTO transazioni (id, data, descrizione, importo, tipo, anno, mese)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (id_transazione, data, descrizione, importo, tipo, data_obj.year, data_obj.month))
        self.conn.commit()
    
    def elimina_transazione(self, id_transazione):
        """Elimina una transazione dal database dato il suo ID"""
        try:
            self.cursor.execute('DELETE FROM transazioni WHERE id = ?', (id_transazione,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Errore durante l'eliminazione: {str(e)}")
            return False
    
    def get_transazioni_mese(self, anno, mese):
        """Recupera tutte le transazioni di un mese specifico"""
        try:
            self.cursor.execute('''
                SELECT * FROM transazioni 
                WHERE anno = ? AND mese = ?
                ORDER BY data
            ''', (anno, mese))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Errore durante il recupero delle transazioni: {str(e)}")
            return []
    
    def get_transazioni_anno(self, anno):
        """Recupera tutte le transazioni di un anno specifico"""
        self.cursor.execute('''
            SELECT * FROM transazioni 
            WHERE anno = ?
            ORDER BY mese, data
        ''', (anno,))
        return self.cursor.fetchall()
    
    def get_anni_disponibili(self):
        """Recupera tutti gli anni presenti nel database"""
        self.cursor.execute('SELECT DISTINCT anno FROM transazioni ORDER BY anno')
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_tutte_transazioni(self):
        """Recupera tutte le transazioni dal database per debug"""
        try:
            self.cursor.execute('SELECT * FROM transazioni ORDER BY anno, mese, data')
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Errore durante il recupero di tutte le transazioni: {str(e)}")
            return []
    
    def __del__(self):
        """Chiude la connessione al database quando l'oggetto viene distrutto"""
        self.conn.close() 