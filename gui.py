import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime
from utils import valida_data, valida_importo, formatta_importo, get_mese_corrente, get_anno_corrente, get_nome_mese

class GestoreSpeseGUI:
    def __init__(self, root, database):
        self.root = root
        self.db = database
        self.root.title("Gestore Spese")
        self.root.geometry("1200x800")
        
        # Configura la chiusura della finestra
        self.root.protocol("WM_DELETE_WINDOW", self.chiudi_applicazione)
        
        # Stile moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configura i colori e gli stili
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabelframe", background="#f0f0f0")
        self.style.configure("TLabelframe.Label", 
                           font=('Helvetica', 10, 'bold'),
                           background="#f0f0f0",
                           foreground="black")
        self.style.configure("TButton", 
                           font=('Helvetica', 9),
                           padding=6,
                           background="#2196F3",
                           foreground="white")
        self.style.map("TButton",
                      background=[('active', '#1976D2'), ('pressed', '#0D47A1')])
        self.style.configure("TLabel", 
                           font=('Helvetica', 9),
                           background="#f0f0f0",
                           foreground="black",
                           padding=5)
        self.style.configure("TEntry", 
                           font=('Helvetica', 9),
                           padding=5,
                           fieldbackground="white")
        self.style.configure("Treeview",
                           font=('Helvetica', 9),
                           rowheight=25,
                           background="white",
                           fieldbackground="white",
                           foreground="black")
        self.style.configure("Treeview.Heading",
                           font=('Helvetica', 9, 'bold'),
                           background="#e0e0e0",
                           foreground="black")
        
        # Crea un canvas con scrollbar
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        # Configura il canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Posiziona il canvas e la scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Crea un frame per il contenuto
        self.main_frame = ttk.Frame(self.canvas, padding="20")
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw", width=self.root.winfo_width())
        
        # Configura il binding per lo scroll
        self.main_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Aggiungi il binding per la rotella del mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)    # Linux scroll down
        
        # Configura il grid per espandere
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Frame per l'inserimento con stile moderno
        self.inserimento_frame = ttk.LabelFrame(self.main_frame, text="Inserisci Transazione", padding="15")
        self.inserimento_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Configura il grid per l'inserimento
        self.inserimento_frame.grid_columnconfigure(3, weight=1)  # Espande la colonna della descrizione
        
        # Campi di inserimento con layout migliorato
        ttk.Label(self.inserimento_frame, text="Data (gg-mm-aaaa):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.data_var = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y"))
        self.data_entry = ttk.Entry(self.inserimento_frame, textvariable=self.data_var, width=12)
        self.data_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(self.inserimento_frame, text="Descrizione:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.descrizione_var = tk.StringVar()
        self.descrizione_entry = ttk.Entry(self.inserimento_frame, textvariable=self.descrizione_var, width=30)
        self.descrizione_entry.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(self.inserimento_frame, text="Importo (€):").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.importo_var = tk.StringVar()
        self.importo_entry = ttk.Entry(self.inserimento_frame, textvariable=self.importo_var, width=10)
        self.importo_entry.grid(row=0, column=5, padx=5)
        
        ttk.Label(self.inserimento_frame, text="Tipo:").grid(row=0, column=6, sticky=tk.W, padx=5)
        self.tipo_var = tk.StringVar(value="entrata")
        self.tipo_combo = ttk.Combobox(self.inserimento_frame, textvariable=self.tipo_var, 
                                      values=["entrata", "uscita"], state="readonly", width=10)
        self.tipo_combo.grid(row=0, column=7, padx=5)
        
        ttk.Button(self.inserimento_frame, text="Inserisci", command=self.inserisci_transazione).grid(row=0, column=8, padx=5)
        
        # Frame per la selezione del periodo con stile moderno
        self.periodo_frame = ttk.Frame(self.main_frame)
        self.periodo_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(self.periodo_frame, text="Anno:").pack(side=tk.LEFT, padx=5)
        self.anno_var = tk.StringVar()
        self.anno_combo = ttk.Combobox(self.periodo_frame, textvariable=self.anno_var, width=6, state="readonly")
        self.anno_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.periodo_frame, text="Mese:").pack(side=tk.LEFT, padx=5)
        self.mese_var = tk.StringVar()
        self.mesi = [(str(i), get_nome_mese(i)) for i in range(1, 13)]
        self.mese_combo = ttk.Combobox(self.periodo_frame, textvariable=self.mese_var, 
                                      values=[f"{m[0]} - {m[1]}" for m in self.mesi],
                                      width=15, state="readonly")
        self.mese_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.periodo_frame, text="Aggiorna", command=self.aggiorna_visualizzazione).pack(side=tk.LEFT, padx=5)
        
        # Frame per il grafico con stile moderno
        self.grafico_frame = ttk.LabelFrame(self.main_frame, text="Grafico", padding="15")
        self.grafico_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Frame per la tabella con stile moderno
        self.tabella_frame = ttk.LabelFrame(self.main_frame, text="Transazioni", padding="15")
        self.tabella_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Tabella con stile migliorato
        self.tree = ttk.Treeview(self.tabella_frame, columns=("ID", "Data", "Descrizione", "Importo", "Tipo"), show="headings")
        
        # Configura le intestazioni con la funzionalità di ordinamento
        self.ordine_corrente = {"colonna": None, "inverso": False}
        
        # Configura le intestazioni con ordinamento solo per i campi specificati
        self.tree.heading("ID", text="ID", command=lambda: self.ordina_tabella("ID"))
        self.tree.heading("Data", text="Data", command=lambda: self.ordina_tabella("Data"))
        self.tree.heading("Descrizione", text="Descrizione")  # Senza ordinamento
        self.tree.heading("Importo", text="Importo", command=lambda: self.ordina_tabella("Importo"))
        self.tree.heading("Tipo", text="Tipo", command=lambda: self.ordina_tabella("Tipo"))
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Data", width=100, anchor=tk.CENTER)
        self.tree.column("Descrizione", width=300)
        self.tree.column("Importo", width=100, anchor=tk.E)
        self.tree.column("Tipo", width=100, anchor=tk.CENTER)
        
        # Scrollbar con stile moderno
        scrollbar = ttk.Scrollbar(self.tabella_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame per i pulsanti con stile moderno
        self.pulsanti_frame = ttk.Frame(self.tabella_frame)
        self.pulsanti_frame.pack(fill=tk.X, pady=10)
        
        # Pulsanti con stile migliorato
        ttk.Button(self.pulsanti_frame, text="Elimina Transazione Selezionata", 
                  command=self.elimina_transazione_selezionata).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.pulsanti_frame, text="Aggiorna Visualizzazione", 
                  command=self.aggiorna_visualizzazione).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.pulsanti_frame, text="Chiudi Applicazione", 
                  command=self.chiudi_applicazione).pack(side=tk.RIGHT, padx=5)
        
        # Inizializzazione
        self.inizializza_periodo()
    
    def chiudi_applicazione(self):
        """Chiude l'applicazione in modo sicuro"""
        if messagebox.askyesno("Conferma", "Vuoi davvero chiudere l'applicazione?"):
            plt.close('all')  # Chiude tutti i grafici aperti
            self.root.quit()
            self.root.destroy()
    
    def inizializza_periodo(self):
        """Inizializza i valori dei combobox per anno e mese"""
        try:
            # Aggiorna la lista degli anni
            anni = self.db.get_anni_disponibili()
            if not anni:
                anni = [get_anno_corrente()]
            self.anno_combo['values'] = anni
            
            # Imposta l'anno corrente o il primo anno disponibile
            if str(get_anno_corrente()) in anni:
                self.anno_combo.set(str(get_anno_corrente()))
            else:
                self.anno_combo.set(str(anni[0]))
            
            # Imposta il mese corrente
            mese_corrente = f"{get_mese_corrente()} - {get_nome_mese(get_mese_corrente())}"
            self.mese_combo.set(mese_corrente)
            
            # Aggiungi i binding per l'aggiornamento automatico
            self.anno_combo.bind('<<ComboboxSelected>>', self.on_periodo_change)
            self.mese_combo.bind('<<ComboboxSelected>>', self.on_periodo_change)
            
            # Aggiorna la visualizzazione iniziale
            self.aggiorna_visualizzazione()
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'inizializzazione del periodo: {str(e)}")
    
    def on_periodo_change(self, event=None):
        """Gestisce il cambio di periodo"""
        try:
            anno = self.anno_var.get()
            mese = self.mese_var.get()
            if anno and mese:
                print(f"Cambio periodo: Anno {anno}, Mese {mese}")  # Debug
                self.aggiorna_visualizzazione()
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il cambio di periodo: {str(e)}")
    
    def inserisci_transazione(self):
        """Inserisce una nuova transazione nel database"""
        data = self.data_var.get()
        descrizione = self.descrizione_var.get()
        importo = self.importo_var.get()
        tipo = self.tipo_var.get()
        
        # Validazione
        if not valida_data(data):
            messagebox.showerror("Errore", "Data non valida. Usa il formato gg-mm-aaaa")
            return
        
        if not descrizione:
            messagebox.showerror("Errore", "Inserisci una descrizione")
            return
        
        if not valida_importo(importo):
            messagebox.showerror("Errore", "Importo non valido")
            return
        
        try:
            # Converti l'importo in float
            importo = float(importo.replace(',', '.'))
            
            # Converti la data in oggetto datetime per ottenere anno e mese
            data_obj = datetime.strptime(data, '%d-%m-%Y')
            anno_transazione = data_obj.year
            mese_transazione = data_obj.month
            
            # Inserisci nel database
            self.db.aggiungi_transazione(data, descrizione, importo, tipo)
            
            # Aggiorna la lista degli anni disponibili
            anni = self.db.get_anni_disponibili()
            self.anno_combo['values'] = anni
            
            # Se l'anno della transazione non è nella lista, aggiungilo
            if str(anno_transazione) not in anni:
                self.anno_combo['values'] = list(anni) + [str(anno_transazione)]
            
            # Aggiorna sempre la visualizzazione
            self.aggiorna_visualizzazione()
            
            # Pulisci i campi
            self.descrizione_var.set("")
            self.importo_var.set("")
            
            # Mostra messaggio di conferma
            messagebox.showinfo("Successo", "Transazione inserita con successo!")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'inserimento della transazione: {str(e)}")
    
    def elimina_transazione_selezionata(self):
        """Elimina la transazione selezionata dalla tabella"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attenzione", "Seleziona una transazione da eliminare")
            return
        
        # Chiedi conferma
        if not messagebox.askyesno("Conferma", "Sei sicuro di voler eliminare questa transazione?"):
            return
        
        # Recupera l'ID della transazione
        item = self.tree.item(selected_item[0])
        id_transazione = item['values'][0]
        
        # Elimina dal database
        if self.db.elimina_transazione(id_transazione):
            # Aggiorna la visualizzazione
            self.aggiorna_visualizzazione()
            messagebox.showinfo("Successo", "Transazione eliminata con successo!")
        else:
            messagebox.showerror("Errore", "Errore durante l'eliminazione della transazione")
    
    def aggiorna_visualizzazione(self):
        """Aggiorna il grafico e la tabella con i dati del periodo selezionato"""
        try:
            # Ottieni l'anno selezionato
            anno_selezionato = self.anno_var.get()
            if not anno_selezionato:
                print("Nessun anno selezionato")  # Debug
                return
            
            # Ottieni il mese selezionato
            mese_selezionato = self.mese_var.get()
            if not mese_selezionato:
                print("Nessun mese selezionato")  # Debug
                return
            
            anno = int(anno_selezionato)
            mese = int(mese_selezionato.split(" - ")[0])
            
            print(f"Visualizzazione periodo: {get_nome_mese(mese)} {anno}")  # Debug
            
            # Recupera le transazioni
            transazioni = self.db.get_transazioni_mese(anno, mese)
            print(f"Transazioni trovate: {len(transazioni)}")  # Debug
            
            # Aggiorna la tabella
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for trans in transazioni:
                self.tree.insert("", "end", values=(
                    trans[0],  # id
                    trans[1],  # data
                    trans[2],  # descrizione
                    formatta_importo(trans[3]),  # importo
                    trans[4]   # tipo
                ))
            
            # Aggiorna il grafico
            self.aggiorna_grafico(transazioni)
            
            # Aggiorna il titolo della finestra con il periodo corrente
            self.root.title(f"Gestore Spese - {get_nome_mese(mese)} {anno}")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiornamento della visualizzazione: {str(e)}")
            print(f"Errore dettagliato: {str(e)}")  # Debug
            # Per debug, mostra tutte le transazioni nel database
            print("Transazioni nel database:")
            for trans in self.db.get_tutte_transazioni():
                print(trans)
    
    def create_gradient(self):
        """Crea uno sfondo sfumato blu-viola"""
        # Ottieni le dimensioni della finestra
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Colori per il gradiente (più vivaci)
        color1 = "#0D47A1"  # Blu più intenso
        color2 = "#7B1FA2"  # Viola più intenso
        
        # Crea il gradiente con più passaggi per un effetto più sfumato
        steps = 100  # Aumenta il numero di passaggi per un effetto più fluido
        
        # Pulisci il canvas
        self.canvas.delete("all")
        
        # Crea il gradiente orizzontale
        for i in range(steps):
            # Calcola il colore per questo passaggio
            r1, g1, b1 = self.root.winfo_rgb(color1)
            r2, g2, b2 = self.root.winfo_rgb(color2)
            
            # Calcola il colore intermedio
            r = r1 + (r2 - r1) * i // steps
            g = g1 + (g2 - g1) * i // steps
            b = b1 + (b2 - b1) * i // steps
            
            # Converti in formato esadecimale
            color = f'#{r//256:02x}{g//256:02x}{b//256:02x}'
            
            # Calcola la larghezza per questo passaggio
            x1 = i * width // steps
            x2 = (i + 1) * width // steps
            
            # Crea un rettangolo sfumato
            self.canvas.create_rectangle(x1, 0, x2, height, fill=color, outline=color)
        
        # Aggiorna il canvas quando la finestra viene ridimensionata
        self.root.bind('<Configure>', self._on_resize)
    
    def _on_resize(self, event):
        """Aggiorna il gradiente quando la finestra viene ridimensionata"""
        # Aggiorna le dimensioni del canvas
        self.canvas.config(width=event.width, height=event.height)
        # Ricrea il gradiente
        self.create_gradient()
    
    def _on_mousewheel(self, event):
        """Gestisce lo scroll con la rotella del mouse"""
        if event.num == 5 or event.delta < 0:  # scroll down
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:  # scroll up
            self.canvas.yview_scroll(-1, "units")
    
    def aggiorna_grafico(self, transazioni):
        """Aggiorna il grafico con le transazioni fornite"""
        # Pulisci il frame del grafico
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()
        
        if not transazioni:
            ttk.Label(self.grafico_frame, text="Nessuna transazione disponibile").pack()
            return
        
        # Prepara i dati
        df = pd.DataFrame(transazioni, columns=['id', 'data', 'descrizione', 'importo', 'tipo', 'anno', 'mese'])
        entrate = df[df['tipo'] == 'entrata']['importo'].sum()
        uscite = df[df['tipo'] == 'uscita']['importo'].sum()
        
        # Crea il grafico con stile moderno
        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize=(6, 3))  # Grafico più piccolo
        
        # Colori moderni
        colors = ['#4CAF50', '#F44336']  # Verde per entrate, rosso per uscite
        
        # Crea le barre
        bars = ax.bar(['Entrate', 'Uscite'], [entrate, uscite], color=colors)
        
        # Aggiungi i valori sopra le barre
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'€{height:,.2f}',
                   ha='center', va='bottom',
                   color='black',
                   fontsize=9)
        
        # Personalizza il grafico
        ax.set_title(f"Bilancio {get_nome_mese(int(self.mese_var.get().split(' - ')[0]))} {self.anno_var.get()}",
                    fontsize=10, pad=15, color='black')
        ax.set_ylabel("Euro", fontsize=9, color='black')
        
        # Rimuovi i bordi
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Colora gli assi
        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
        
        # Colora i tick
        ax.tick_params(colors='black')
        
        # Aggiungi il grafico all'interfaccia
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _on_frame_configure(self, event=None):
        """Aggiorna la scrollregion quando il frame viene ridimensionato"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Aggiorna la larghezza del frame interno quando il canvas viene ridimensionato"""
        # Aggiorna la larghezza del frame interno per adattarla al canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width - 20)  # Sottrai il padding
    
    def _on_resize(self, event):
        """Aggiorna il gradiente quando la finestra viene ridimensionata"""
        # Aggiorna le dimensioni del canvas
        self.canvas.config(width=event.width, height=event.height)
        # Ricrea il gradiente
        self.create_gradient()
    
    def _on_mousewheel(self, event):
        """Gestisce lo scroll con la rotella del mouse"""
        if event.num == 5 or event.delta < 0:  # scroll down
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:  # scroll up
            self.canvas.yview_scroll(-1, "units")
    
    def aggiorna_grafico(self, transazioni):
        """Aggiorna il grafico con le transazioni fornite"""
        # Pulisci il frame del grafico
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()
        
        if not transazioni:
            ttk.Label(self.grafico_frame, text="Nessuna transazione disponibile").pack()
            return
        
        # Prepara i dati
        df = pd.DataFrame(transazioni, columns=['id', 'data', 'descrizione', 'importo', 'tipo', 'anno', 'mese'])
        entrate = df[df['tipo'] == 'entrata']['importo'].sum()
        uscite = df[df['tipo'] == 'uscita']['importo'].sum()
        
        # Crea il grafico con stile moderno
        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize=(6, 3))  # Grafico più piccolo
        
        # Colori moderni
        colors = ['#4CAF50', '#F44336']  # Verde per entrate, rosso per uscite
        
        # Crea le barre
        bars = ax.bar(['Entrate', 'Uscite'], [entrate, uscite], color=colors)
        
        # Aggiungi i valori sopra le barre
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'€{height:,.2f}',
                   ha='center', va='bottom',
                   color='black',
                   fontsize=9)
        
        # Personalizza il grafico
        ax.set_title(f"Bilancio {get_nome_mese(int(self.mese_var.get().split(' - ')[0]))} {self.anno_var.get()}",
                    fontsize=10, pad=15, color='black')
        ax.set_ylabel("Euro", fontsize=9, color='black')
        
        # Rimuovi i bordi
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Colora gli assi
        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
        
        # Colora i tick
        ax.tick_params(colors='black')
        
        # Aggiungi il grafico all'interfaccia
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def ordina_tabella(self, colonna):
        """Ordina la tabella in base alla colonna selezionata"""
        # Ottieni tutti gli elementi
        items = []
        for item in self.tree.get_children(''):
            valore = self.tree.set(item, colonna)
            # Converti il valore in base al tipo di colonna
            if colonna == "ID":
                valore = int(valore)
            elif colonna == "Importo":
                # Rimuovi il simbolo € e converti in float
                valore = float(valore.replace('€', '').replace('.', '').replace(',', '.').strip())
            elif colonna == "Data":
                # Converti la data in oggetto datetime per un ordinamento corretto
                valore = datetime.strptime(valore, '%d-%m-%Y')
            items.append((valore, item))
        
        # Determina se invertire l'ordine
        if self.ordine_corrente["colonna"] == colonna:
            self.ordine_corrente["inverso"] = not self.ordine_corrente["inverso"]
        else:
            self.ordine_corrente["inverso"] = False
            self.ordine_corrente["colonna"] = colonna
        
        # Ordina gli elementi
        items.sort(reverse=self.ordine_corrente["inverso"])
        
        # Riorganizza gli elementi nell'ordine corretto
        for index, (_, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        # Aggiorna le intestazioni per mostrare l'ordine corrente
        for col in self.tree["columns"]:
            if col == colonna:
                self.tree.heading(col, text=f"{col} {'↓' if self.ordine_corrente['inverso'] else '↑'}")
            else:
                self.tree.heading(col, text=col) 