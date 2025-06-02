# Gestore Spese 📊

Un'applicazione desktop moderna e intuitiva per gestire le tue spese e entrate mensili. 💰

## Caratteristiche Principali ✨

### Gestione Transazioni 📝
- Inserimento di spese e entrate con:
  - Data (formato gg-mm-aaaa) 📅
  - Descrizione della spesa o dell'entrata 📋
  - Importo 💵
  - Tipo di transazione (entrata/uscita) ↔️
- Visualizzazione delle transazioni in una tabella ordinata 📊
- Eliminazione delle transazioni non più necessarie 🗑️

### Visualizzazione Dati 📈
- Grafico a barre che mostra:
  - Entrate totali del mese 📈
  - Uscite totali del mese 📉
  - Bilancio mensile 💹
- Tabella dettagliata con tutte le transazioni 📋
- Possibilità di filtrare per mese e anno 🔍

### Navigazione e Filtri 🔄
- Selezione del mese desiderato 📅
- Selezione dell'anno 📆
- Aggiornamento automatico della visualizzazione 🔄
- Supporto per la navigazione tra diversi anni 📚

### Interfaccia Utente 🎨
- Design moderno e intuitivo con tema 'clam' ✨
- Interfaccia pulita e professionale 🎯
- Grafici colorati e leggibili 📊
- Scrollbar per navigare facilmente tra le transazioni 📜
- Supporto per il mouse e la tastiera 🖱️⌨️

### Persistenza Dati 💾
- Salvataggio automatico di tutte le transazioni 💾
- Database SQLite integrato 🗄️
- Mantenimento dei dati tra le sessioni 🔄
- Supporto per più anni di transazioni 📚

## Requisiti di Sistema 💻
- Windows 10 o superiore 🪟
- 4GB di RAM (minimo consigliato) 💾
- 100MB di spazio su disco 💿

## Installazione 🚀
1. Scarica l'eseguibile `Gestore Spese.exe` dalla cartella `dist`
2. Sposta l'eseguibile nella cartella desiderata
3. Fai doppio click per avviare l'applicazione

### Creazione Collegamenti 🔗
- Puoi creare un collegamento all'eseguibile nella cartella principale
- Il collegamento deve puntare a `dist/Gestore Spese.exe`
- Il database verrà sempre creato nella cartella `dist`
- È consigliabile mantenere l'eseguibile originale nella cartella `dist`

## Utilizzo 📱

### Inserimento Transazioni ➕
1. Inserisci la data nel formato gg-mm-aaaa 📅
2. Scrivi una descrizione della transazione 📝
3. Inserisci l'importo 💰
4. Seleziona il tipo (entrata/uscita) ↔️
5. Clicca su "Inserisci" ✅

### Navigazione tra i Mesi 🔄
1. Usa il menu a tendina per selezionare l'anno 📅
2. Seleziona il mese desiderato 📆
3. La visualizzazione si aggiornerà automaticamente 🔄

### Eliminazione Transazioni 🗑️
1. Seleziona la transazione da eliminare nella tabella 📋
2. Clicca su "Elimina Transazione Selezionata" 🗑️
3. Conferma l'eliminazione ✅

### Gestione Database 💾
- Il database viene creato automaticamente nella stessa cartella dell'eseguibile 🗄️
- Puoi fare backup del database copiando il file `transazioni.db` 💾
- Se il database viene eliminato, ne verrà creato uno nuovo vuoto 🔄

## Note Importanti ⚠️
- L'applicazione crea e gestisce automaticamente il database 🗄️
- I dati vengono salvati localmente sul tuo computer 💾
- È consigliabile fare backup regolari del database 📦
- L'applicazione mantiene la cronologia di tutti gli anni 📚


## Autore
👤 **Luigi Carnevale**
- GitHub: [@Luigi-Carnevale](https://github.com/Luigi-Carnevale)

## Licenza
Questo progetto è distribuito con licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

---
⭐️ Se ti piace questo progetto, lascia una stella su GitHub! 