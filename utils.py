from datetime import datetime

def valida_data(data_str):
    """Verifica se una stringa è una data valida nel formato dd-mm-yyyy"""
    try:
        datetime.strptime(data_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False

def valida_importo(importo_str):
    """Verifica se una stringa è un importo valido"""
    try:
        importo = float(importo_str.replace(',', '.'))
        return importo > 0
    except ValueError:
        return False

def formatta_importo(importo):
    """Formatta un importo con il simbolo dell'euro e due decimali"""
    return f"€ {importo:.2f}"

def get_mese_corrente():
    """Restituisce il mese corrente come numero (1-12)"""
    return datetime.now().month

def get_anno_corrente():
    """Restituisce l'anno corrente"""
    return datetime.now().year

def get_nome_mese(numero_mese):
    """Converte il numero del mese nel suo nome"""
    mesi = {
        1: "Gennaio", 2: "Febbraio", 3: "Marzo", 4: "Aprile",
        5: "Maggio", 6: "Giugno", 7: "Luglio", 8: "Agosto",
        9: "Settembre", 10: "Ottobre", 11: "Novembre", 12: "Dicembre"
    }
    return mesi.get(numero_mese, "") 