import sqlite3
import tkinter as tk
from tkinter import Entry, ttk
from tkinter import messagebox
from tkinter import Frame
from tkinter import *
import tkinter.simpledialog as tsd


def esegui_query(query, filtri=None):
    conn = sqlite3.connect("ChatStorage.sqlite")
    cursor = conn.cursor()

    if filtri:
        risultati = cursor.execute(query, filtri).fetchall()
    else:
        risultati = cursor.execute(query).fetchall()

    cursor.close()
    conn.close()

    return risultati


def esegui_query_senza_filtro(query):
    risultati = esegui_query(query)
    messagebox.showinfo("Risultati Query", str(risultati))


def apri_finestra_2filtri(query):
    finestra_2filtri = tk.Toplevel(root)
    finestra_2filtri.title("Inserimento Filtri")

    # Creazione delle etichette e degli entry per i filtri
    label_filtro1 = tk.Label(finestra_2filtri, text="Contatto:")
    label_filtro1.grid(row=0, column=0, padx=10, pady=5)
    entry_filtro1 = tk.Entry(finestra_2filtri)
    entry_filtro1.grid(row=0, column=1, padx=10, pady=5)

    label_filtro2 = tk.Label(finestra_2filtri, text="Testo:")
    label_filtro2.grid(row=1, column=0, padx=10, pady=5)
    entry_filtro2 = tk.Entry(finestra_2filtri)
    entry_filtro2.grid(row=1, column=1, padx=10, pady=5)

    # Funzione per eseguire la query con i filtri inseriti
    def esegui_query_con_2filtro():
        filtro1 = entry_filtro1.get()
        filtro2 = entry_filtro2.get()

        risultati = esegui_query(query, (filtro1, filtro2))
        messagebox.showinfo("Risultati Query", str(risultati))

        finestra_2filtri.destroy()

    # Creazione del pulsante per eseguire la query
    pulsante_esegui = tk.Button(finestra_2filtri, text="Esegui", command=esegui_query_con_2filtro)
    pulsante_esegui.grid(row=2, column=0, columnspan=2, padx=10, pady=5)


# Creazione della finestra principale
root = tk.Tk()
root.geometry("1000x700")
root.resizable(False, False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.title("WhatsApp Analyzer")

root.configure(bg='#C6E4D9')
message = tk.Label(root, text="WHATSAPP ANALYZER", background='#C6E4D9', fg="white", bg="#116062", width=55,
                   height=10, font=('times', 27, ' bold '))
message.place(x=-90, y=120)

# Creazione del menu
menu = tk.Menu(root)
root.config(menu=menu)

# Creazione del menu "Query"
menu_query = tk.Menu(menu)
menu.add_cascade(label="Query", menu=menu_query)



# Aggiunta delle opzioni al menu "Query"
menu_query.add_command(label="Mostra contatti", command=lambda: esegui_query_senza_filtro(
    "SELECT ZPARTNERNAME from ZWACHATSESSION where ZSESSIONTYPE==0 order by ZPARTNERNAME"))

menu_query.add_command(label="Mostra gruppi", command=lambda: esegui_query_senza_filtro(
    "select ZPARTNERNAME from ZWACHATSESSION where ZSESSIONTYPE==1 order by ZPARTNERNAME"))


menu_query.add_command(label="Cercare una parola all'interno della chat con uno specifico contatto", command=lambda: apri_finestra_2filtri(
    "SELECT friend_name, message_text, message_date, message_type, is_from_me from friend_messages where " \
            "friend_name  == ? AND message_text LIKE ? "))

menu_query.add_command(label="Cercare una parola tra i messaggi in uscita all'interno della chat di un gruppo specifico", command=lambda: apri_finestra_2filtri(
    "select message_date,message_type, message_text from group_messages where group_name == ? AND is_from_me " \
            "== 1 AND message_text LIKE ? "))


menu_query.add_command(label="Cercare una parola tra i messaggi in entrata all'interno della chat di un gruppo specifico", command=lambda: apri_finestra_2filtri(
    "select message_date,message_type, message_text, friend_name, friend_id from group_messages where " \
            "group_name == ? AND is_from_me == 0 AND message_text LIKE ?"))

# Avvio del ciclo principale Tkinter
root.mainloop()

# def esegui_query(query, filtri=None):
#     conn = sqlite3.connect("ChatStorage.sqlite")
#     cursor = conn.cursor()
#
#     if filtri:
#         risultati = cursor.execute(query, filtri).fetchall()
#     else:
#         risultati = cursor.execute(query).fetchall()
#
#     cursor.close()
#     conn.close()
#
#     return risultati
#
#
# def apri_finestra_filtri(query):
#     finestra_filtri = tk.Toplevel(root)
#     finestra_filtri.title("Inserimento Filtri")
#
#     # Creazione delle etichette e degli entry per i filtri
#     filtri = []
#     for i, filtro in enumerate(query["filtri"]):
#         label_filtro = tk.Label(finestra_filtri, text=filtro + ":")
#         label_filtro.grid(row=i, column=0, padx=10, pady=5)
#         entry_filtro = tk.Entry(finestra_filtri)
#         entry_filtro.grid(row=i, column=1, padx=10, pady=5)
#         filtri.append(entry_filtro)
#
#     # Funzione per eseguire la query con i filtri inseriti
#     def esegui_query_con_filtri():
#         valori_filtri = [filtro.get() for filtro in filtri]
#         risultati = esegui_query(query["sql"], valori_filtri)
#         messagebox.showinfo("Risultati Query", str(risultati))
#
#     # Esegui la query automaticamente con filtri
#     esegui_query_con_filtri()
#
#     # Chiudi la finestra dei filtri
#     finestra_filtri.destroy()
#
#
# def apri_finestra_query(query):
#     risultati = esegui_query(query["sql"])
#     messagebox.showinfo("Risultati Query", str(risultati))
#
#
# # Creazione della finestra principale
# root = tk.Tk()
# root.title("Applicazione Tkinter")
#
# # Definizione delle query con filtri e senza filtri
# query_con_filtri = [
#     {
#         "label": "Query 1",
#         "sql": "SELECT day, avg(number_of_messages) over (order by day asc rows 30 preceding) as ma_nom from (SELECT " \
#                "date(message_date) as day, count(*) as number_of_messages from friend_messages where friend_name == ? " \
#                "group by day, friend_name)",
#         "filtri": ["Valore Colonna 1"]
#     },
#     {
#         "label": "Query 2",
#         "sql": "SELECT friend_name, message_text, message_date, message_type, is_from_me from friend_messages where " \
#                "friend_name  == ? AND message_text LIKE ?",
#         "filtri": ["Valore Colonna 2", "Valore Colonna 3"]
#     }
# ]
#
# query_senza_filtri = [
#     {
#         "label": "Query 3",
#         "sql": "SELECT ZPARTNERNAME from ZWACHATSESSION where ZSESSIONTYPE==0 order by ZPARTNERNAME"
#     },
#     {
#         "label": "Query 4",
#         "sql": "select ZPARTNERNAME from ZWACHATSESSION where ZSESSIONTYPE==1 order by ZPARTNERNAME"
#     }
# ]
#
# # Creazione del menu con le query
# menu = tk.Menu(root)
# root.config(menu=menu)
#
# menu_query = tk.Menu(menu)
# menu.add_cascade(label="Query con Filtri", menu=menu_query)
#
# for query in query_con_filtri:
#     menu_query.add_command(label=query["label"], command=lambda q=query: apri_finestra_filtri(q))
#
# menu_query_senza_filtri = tk.Menu(menu)
# menu.add_cascade(label="Query senza Filtri", menu=menu_query_senza_filtri)
#
# root.mainloop()
