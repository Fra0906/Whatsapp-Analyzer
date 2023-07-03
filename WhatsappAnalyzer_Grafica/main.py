import sqlite3
import tkinter as tk
from tkinter import Entry, ttk
from tkinter import messagebox as mess
from tkinter import Frame
from tkinter import *
import tkinter.simpledialog as tsd
#from mainprova2 import *
from queries import *
#import pkg_resources.py2_warn

###################################### QUERY ###########################################à

q_str = {
    "1": "SELECT ZPARTNERNAME from ZWACHATSESSION where ZSESSIONTYPE==0 order by ZPARTNERNAME",
    "2": "select ZPARTNERNAME from ZWACHATSESSION where ZSESSIONTYPE==1 order by ZPARTNERNAME",
    "3": "SELECT friend_name, avg(length(message_text)) as avg_message_length FROM friend_messages WHERE " \
         "message_type == 'text' and is_from_me == 0 group by friend_name order by avg_message_length desc ",
    "4": "SELECT day, avg(number_of_messages) over (order by day asc rows 30 preceding) as ma_nom from (SELECT " \
         "date(message_date) as day, count(*) as number_of_messages from friend_messages where friend_name == ? " \
         "group by day, friend_name)",
    "5": "select strftime('%w', message_date) as weekday_number,(case strftime('%w', message_date) when '0' then " \
         "'Monday' when '1' then 'Tuesday' when '2' then 'Wednesday' when '3' then 'Thursday' when '4' then " \
         "'Friday' when '5' then 'Saturday'  when '6' then 'Sunday' else 'unknown' end ) as weekday_name, " \
         "strftime('%H', message_date) as day_hour, count(*) as number_of_messages from friend_messages where " \
         "friend_name == ? group by weekday_name, day_hour order by weekday_number, day_hour ",
    "6": "select strftime('%w', message_date) as weekday_number,(case strftime('%w', message_date) when '0' then " \
            "'Monday' when '1' then 'Tuesday' when '2' then 'Wednesday' when '3' then 'Thursday' when '4' then " \
            "'Friday' when '5' then 'Saturday'  when '6' then 'Sunday' else 'unknown' end ) as weekday_name, " \
            "strftime('%H', message_date) as day_hour, count(*) as number_of_messages from group_messages where " \
            "group_name == ? group by weekday_name, day_hour order by weekday_number, day_hour ",
    "7": "select friend_name, day, avg(number_of_sent_messages) over ( order by friend_name, day asc rows 30 " \
         "preceding ) as ma_nom from ( select ( case is_from_me when 0 then friend_name else 'Me' end) as " \
         "friend_name,date(message_date) as day,count(*) as number_of_sent_messages from group_messages where " \
         "group_name == ? group by friend_name,day )",
    "8": "SELECT friend_name, message_text, message_date, message_type, is_from_me from friend_messages where " \
         "friend_name  == ? AND message_text LIKE ? ",
    "9": "select message_date,message_type, message_text from group_messages where group_name == ? AND is_from_me " \
         "== 1 AND message_text LIKE ? ",
    "10": "select message_date,message_type, message_text, friend_name, friend_id from group_messages where " \
          "group_name == ? AND is_from_me == 0 AND message_text LIKE ? ",
    "11": "select count(*) as number_of_messages, friend_name, friend_id, group_name, group_id from group_messages " \
          "where group_name == ? AND is_from_me == 0 AND friend_name == ? AND message_text LIKE ? ",
    "12": "select count(*) as number_of_messages, group_name, group_id from group_messages where group_name == ? " \
          "AND is_from_me == 1 AND message_text LIKE ? "
}

q_filters = {
    "1": [],
    "2": [],
    "3": [],
    "4": ["Inserisci il nome del contatto: "],
    "5": ["Inserisci il nome del contatto: "],
    "6": ["Inserisci il nome del gruppo: "],
    "7": ["Inserisci il nome del gruppo: "],
    "8": ["Inserisci il nome del contatto: ",
          "Inserisci il testo da cercare: "],
    "9": ["Inserisci il nome del gruppo: ",
          "Inserisci il testo da cercare: "],
    "10": ["Inserisci il nome del gruppo: ",
           "Inserisci il testo da cercare: "],
    "11": ["Inserisci il nome del gruppo: ",
           "Inserisci il nome del contatto:",
           "Inserisci il testo da cercare: "],
    "12": ["Inserisci il nome del gruppo: ",
           "Inserisci il testo da cercare: "]
}


def SQL1():
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["1"])
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)


    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def SQL2():
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["2"])
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def SQL3():
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["3"])
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def get_data_query4():
    form_input = Toplevel(window)
    form_input.title("Inserimento parametri")
    form_input.geometry("400x150")
    form_input.iconbitmap('logo2.ico')
    form_input.grid_columnconfigure(0, weight=1)
    form_input.grid_columnconfigure(1, weight=1)
    form_input.grid_rowconfigure(0, weight=1)
    form_input.grid_rowconfigure(1, weight=1)
    # frame_input.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    label1 = tk.Label(form_input, text="Inserisci il nome del contatto: ")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry(form_input)
    entry1.grid(row=0, column=1)

    button_submit = Button(form_input, text='Analyze', font=('Arial', 13, 'bold'), width=20, height=1,
                           background='#116062', fg='white', command=lambda: SQL4([entry1.get()]))
    button_submit.place(x=100, y=100)

def SQL4(params):
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["4"], params)
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def get_data_query5():
    form_input = Toplevel(window)
    form_input.title("Inserimento parametri")
    form_input.geometry("400x150")
    form_input.iconbitmap('logo2.ico')
    form_input.grid_columnconfigure(0, weight=1)
    form_input.grid_columnconfigure(1, weight=1)
    form_input.grid_rowconfigure(0, weight=1)
    form_input.grid_rowconfigure(1, weight=1)
    # frame_input.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    label1 = tk.Label(form_input, text="Inserisci il nome del contatto: ")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry(form_input)
    entry1.grid(row=0, column=1)

    button_submit = Button(form_input, text='Analyze', font=('Arial', 13, 'bold'), width=20, height=1,
                           background='#116062', fg='white', command=lambda: SQL5([entry1.get()]))
    button_submit.place(x=100, y=100)

def SQL5(params):
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["5"], params)
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def get_data_query6():
    form_input = Toplevel(window)
    form_input.title("Inserimento parametri")
    form_input.geometry("400x150")
    form_input.iconbitmap('logo2.ico')
    form_input.grid_columnconfigure(0, weight=1)
    form_input.grid_columnconfigure(1, weight=1)
    form_input.grid_rowconfigure(0, weight=1)
    form_input.grid_rowconfigure(1, weight=1)
    # frame_input.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    label1 = tk.Label(form_input, text="Inserisci il nome del gruppo: ")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry(form_input)
    entry1.grid(row=0, column=1)

    button_submit = Button(form_input, text='Analyze', font=('Arial', 13, 'bold'), width=20, height=1,
                           background='#116062', fg='white', command=lambda: SQL6([entry1.get()]))
    button_submit.place(x=100, y=100)

def SQL6(params):
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["6"], params)
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def get_data_query7():
    form_input = Toplevel(window)
    form_input.title("Inserimento parametri")
    form_input.geometry("400x150")
    form_input.iconbitmap('logo2.ico')
    form_input.grid_columnconfigure(0, weight=1)
    form_input.grid_columnconfigure(1, weight=1)
    form_input.grid_rowconfigure(0, weight=1)
    form_input.grid_rowconfigure(1, weight=1)

    # frame_input.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    label1 = tk.Label(form_input, text="Inserisci il nome del gruppo: ")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry(form_input)
    entry1.grid(row=0, column=1)

    button_submit = Button(form_input, text='Analyze', font=('Arial', 13, 'bold'), width=20, height=1,
                           background='#116062', fg='white', command=lambda: SQL7([entry1.get()]))
    button_submit.place(x=100, y=100)

def SQL7(params):
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["7"], params)
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def get_data_query8():
    form_input = Toplevel(window)
    form_input.title("Inserimento parametri")
    form_input.geometry("400x200")
    form_input.iconbitmap('logo2.ico')
    form_input.grid_columnconfigure(0, weight=1)
    form_input.grid_columnconfigure(1, weight=1)
    form_input.grid_rowconfigure(0, weight=1)
    form_input.grid_rowconfigure(1, weight=1)
    form_input.grid_rowconfigure(2, weight=1)
    form_input.grid_rowconfigure(3, weight=1)
    form_input.grid_rowconfigure(4, weight=1)
    # frame_input.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    label1 = tk.Label(form_input, text="Inserisci il nome del contatto: ")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry(form_input)
    entry1.grid(row=0, column=1)

    label2 = tk.Label(form_input, text="Inserisci il testo: ")
    label2.grid(row=1, column=0)

    entry2 = tk.Entry(form_input)
    entry2.grid(row=1, column=1)

    button_submit = Button(form_input, text='Analyze', font=('Arial', 13, 'bold'), width=18, height=1,
                           background='#116062', fg='white',
                           command=lambda: SQL8([entry1.get(), entry2.get()]))
    button_submit.place(x=100, y=130)

def SQL8(params):
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["8"], params)
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def get_data_query9():
    form_input = Toplevel(window)
    form_input.title("Inserimento parametri")
    form_input.geometry("400x200")
    form_input.iconbitmap('logo2.ico')
    form_input.grid_columnconfigure(0, weight=1)
    form_input.grid_columnconfigure(1, weight=1)
    form_input.grid_rowconfigure(0, weight=1)
    form_input.grid_rowconfigure(1, weight=1)
    form_input.grid_rowconfigure(2, weight=1)
    form_input.grid_rowconfigure(3, weight=1)
    form_input.grid_rowconfigure(4, weight=1)
    # frame_input.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    label1 = tk.Label(form_input, text="Inserisci il nome del gruppo: ")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry(form_input)
    entry1.grid(row=0, column=1)

    label2 = tk.Label(form_input, text="Inserisci il testo: ")
    label2.grid(row=1, column=0)

    entry2 = tk.Entry(form_input)
    entry2.grid(row=1, column=1)

    button_submit = Button(form_input, text='Analyze', font=('Arial', 13, 'bold'), width=18, height=1,
                           background='#116062', fg='white',
                           command=lambda: SQL9([entry1.get(), entry2.get()]))
    button_submit.place(x=100, y=130)

def SQL9(params):
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["9"], params)
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def get_data_query10():
    form_input = Toplevel(window)
    form_input.title("Inserimento parametri")
    form_input.geometry("400x200")
    form_input.iconbitmap('logo2.ico')
    form_input.grid_columnconfigure(0, weight=1)
    form_input.grid_columnconfigure(1, weight=1)
    form_input.grid_rowconfigure(0, weight=1)
    form_input.grid_rowconfigure(1, weight=1)
    form_input.grid_rowconfigure(2, weight=1)
    form_input.grid_rowconfigure(3, weight=1)
    form_input.grid_rowconfigure(4, weight=1)
    # frame_input.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    label1 = tk.Label(form_input, text="Inserisci il nome del gruppo: ")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry(form_input)
    entry1.grid(row=0, column=1)

    label2 = tk.Label(form_input, text="Inserisci il testo: ")
    label2.grid(row=1, column=0)

    entry2 = tk.Entry(form_input)
    entry2.grid(row=1, column=1)

    button_submit = Button(form_input, text='Analyze', font=('Arial', 13, 'bold'), width=18, height=1,
                           background='#116062', fg='white',
                           command=lambda: SQL10([entry1.get(), entry2.get()]))
    button_submit.place(x=100, y=130)

def SQL10(params):
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["10"], params)
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def get_data_query11():
    form_input = Toplevel(window)
    form_input.title("Inserimento parametri")
    form_input.geometry("400x200")
    form_input.iconbitmap('logo2.ico')
    form_input.grid_columnconfigure(0, weight=1)
    form_input.grid_columnconfigure(1, weight=1)
    form_input.grid_rowconfigure(0, weight=1)
    form_input.grid_rowconfigure(1, weight=1)
    form_input.grid_rowconfigure(2, weight=1)
    form_input.grid_rowconfigure(3, weight=1)
    form_input.grid_rowconfigure(4, weight=1)
    form_input.grid_rowconfigure(5, weight=1)
    # frame_input.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    label1 = tk.Label(form_input, text="Inserisci il nome del gruppo: ")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry(form_input)
    entry1.grid(row=0, column=1)

    label2 = tk.Label(form_input, text="Inserisci il nome del contatto: ")
    label2.grid(row=1, column=0)

    entry2 = tk.Entry(form_input)
    entry2.grid(row=1, column=1)

    label3 = tk.Label(form_input, text="Inserisci il testo: ")
    label3.grid(row=2, column=0)

    entry3 = tk.Entry(form_input)
    entry3.grid(row=2, column=1)

    button_submit = Button(form_input, text='Analyze', font=('Arial', 13, 'bold'), width=18, height=1,
                           background='#116062', fg='white',
                           command=lambda: SQL11([entry1.get(), entry2.get(), entry3.get()]))
    button_submit.place(x=100, y=140)

def SQL11(params):
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["11"], params)
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()

def get_data_query12():
    form_input = Toplevel(window)
    form_input.title("Inserimento parametri")
    form_input.geometry("400x200")
    form_input.iconbitmap('logo2.ico')
    form_input.grid_columnconfigure(0, weight=1)
    form_input.grid_columnconfigure(1, weight=1)
    form_input.grid_rowconfigure(0, weight=1)
    form_input.grid_rowconfigure(1, weight=1)
    form_input.grid_rowconfigure(2, weight=1)
    form_input.grid_rowconfigure(3, weight=1)
    form_input.grid_rowconfigure(4, weight=1)
    # frame_input.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    label1 = tk.Label(form_input, text="Inserisci il nome del gruppo: ")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry(form_input)
    entry1.grid(row=0, column=1)

    label2 = tk.Label(form_input, text="Inserisci il testo: ")
    label2.grid(row=1, column=0)

    entry2 = tk.Entry(form_input)
    entry2.grid(row=1, column=1)

    button_submit = Button(form_input, text='Analyze', font=('Arial', 13, 'bold'), width=18, height=1,
                           background='#116062', fg='white',
                           command=lambda: SQL12([entry1.get(), entry2.get()]))
    button_submit.place(x=100, y=130)

def SQL12(params):
    conn = sqlite3.connect('ChatStorage.sqlite')
    cursor = conn.cursor()

    cursor.execute(q_str["12"], params)
    results = cursor.fetchall()

    conn.close()

    page3.grid_columnconfigure(0, weight=1)
    page3.grid_rowconfigure(0, weight=1)
    page3.grid_rowconfigure(1, weight=1)

    finestra_risultati = tk.Text(page3)
    finestra_risultati.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    scroll = ttk.Scrollbar(finestra_risultati, orient='vertical', command=finestra_risultati.yview)
    scroll.place(x=960, y=0, height=530)
    finestra_risultati.configure(yscrollcommand=scroll.set)

    page3_button_back = Button(page3, text='Back', font=('Arial', 13, 'bold'), width=35, height=1, background='#116062',
                               fg='white', command=lambda: page2.tkraise())
    page3_button_back.place(x=320, y=650)

    finestra_risultati.delete(1.0, tk.END)
    for r in results:
        finestra_risultati.insert(tk.END, r)
        finestra_risultati.insert(tk.END, "\n")

    page3.tkraise()


###################################### GRAFICA ###########################################à
window = tk.Tk()
window.geometry("1000x700")
window.resizable(False, False)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.title("WhatsApp Analyzer")
window.iconbitmap('logo.ico')


page1 = Frame(window)
page2 = Frame(window)
page3 = Frame(window)

for frame in (page1, page2, page3):
    frame.grid(row=0, column=0, sticky='nsew')

# HOME
page1.configure(bg='#C6E4D9')
message = tk.Label(page1, text="WHATSAPP ANALYZER", background='#C6E4D9', fg="white", bg="#116062", width=55,
                   height=10, font=('times', 27, ' bold '))
message.place(x=-90, y=120)
message2 = tk.Label(page1, text="Author: Francesca Annese", background='#C6E4D9', fg="#116062", font=('times', 11,  ' bold '))
message2.place(x=800, y=0)
page1_button = Button(page1, text='Start', font=('Arial', 13, 'bold'), width=20, height=2, background='#116062',
                      fg='white', command=lambda: page2.tkraise())
page1_button.place(x=380, y=630)
page1.tkraise()

# PAGE2
page2.config(bg='#C6E4D9')
page2_label = Label(page2, text="Selezionare l'operazione da effettuare sul database:", background='#C6E4D9',
                    fg="white", bg="#116062", width=60, height=1, font=('times', 20, ' bold '))
page2_label.place(x=15, y=0)

# Creazione delle variabili per le opzioni di selezione
var = tk.IntVar()
var.set(1)  # Opzione predefinita
radio1 = tk.Button(page2, text="1.      Visualizza i nomi di tutti i contatti", background='#116062', fg='white',
                   font=('Arial', 10, 'bold'), width=100, height=1, command=lambda: SQL1())
radio1.grid(row=1, column=0)
radio1.place(x=80, y=100)
output_text = tk.Text(page3)

radio2 = tk.Button(page2, text="2.      Visualizza i nomi di tutti i gruppi", background='#116062', fg='white',
                   font=('Arial', 10, 'bold'), width=100, height=1, command=lambda: SQL2())
radio2.grid(row=2, column=0)
radio2.place(x=80, y=140)

radio3 = tk.Button(page2, text="3.      Top contatti che scrivono i messaggi più lunghi", background='#116062',
                   fg='white', font=('Arial', 10, 'bold'), width=100, height=1, command=lambda: SQL3())
radio3.grid(row=2, column=0)
radio3.place(x=80, y=180)

radio4 = tk.Button(page2, text="4.      Numero medio di messaggi al giorno scambiati con un contatto nel tempo",
                   background='#116062', fg='white', font=('Arial', 10, 'bold'), width=100, height=1,
                   command=lambda: get_data_query4())
radio4.grid(row=2, column=0)
radio4.place(x=80, y=220)

radio5 = tk.Button(page2,
                   text="5.      Momenti della giornata e della settimana nei quali parlo di più con uno specifico contatto",
                   background='#116062', fg='white', font=('Arial', 10, 'bold'), width=100, height=1,
                   command=lambda: get_data_query5())
radio5.grid(row=2, column=0)
radio5.place(x=80, y=260)

radio6 = tk.Button(page2,
                   text="6.      Momenti della giornata e della settimana nei quali parlo di più con un gruppo specifico",
                   background='#116062', fg='white', font=('Arial', 10, 'bold'), width=100, height=1,
                   command=lambda: get_data_query6())
radio6.grid(row=2, column=0)
radio6.place(x=80, y=300)

radio7 = tk.Button(page2, text="7.      Numero di messaggi inviati da ciascun membro di un gruppo nel tempo",
                   background='#116062', fg='white', font=('Arial', 10, 'bold'), width=100, height=1, command=lambda: get_data_query7())
radio7.grid(row=2, column=0)
radio7.place(x=80, y=340)

radio8 = tk.Button(page2, text="8.      Cercare una parola all'interno della chat con uno specifico contatto",
                   background='#116062', fg='white', font=('Arial', 10, 'bold'), width=100, height=1, command=lambda: get_data_query8())
radio8.grid(row=2, column=0)
radio8.place(x=80, y=380)

radio9 = tk.Button(page2,
                   text="9.      Cercare una parola tra i messaggi in uscita all'interno della chat di un gruppo specifico",
                   background='#116062', fg='white', font=('Arial', 10, 'bold'), width=100, height=1, command=lambda: get_data_query9())
radio9.grid(row=2, column=0)
radio9.place(x=80, y=420)

radio10 = tk.Button(page2,
                    text="10.     Cercare una parola tra i messaggi in entrata all'interno della chat di un gruppo specifico",
                    background='#116062', fg='white', font=('Arial', 10, 'bold'), width=100, height=1, command=lambda: get_data_query10())
radio10.grid(row=2, column=0)
radio10.place(x=80, y=460)

radio11 = tk.Button(page2,
                    text="11.     Contare quante volte una determinata parola è stata scritta da uno specifico utente di uno specifico gruppo",
                    background='#116062', fg='white', font=('Arial', 10, 'bold'), width=100, height=1,
                    command=lambda: get_data_query11())
radio11.grid(row=2, column=0)
radio11.place(x=80, y=500)

radio12 = tk.Button(page2,
                    text="12.     Contare quante volte una determinata parola è stata scritta da me all'interno di uno specifico gruppo",
                    background='#116062', fg='white', font=('Arial', 10, 'bold'), width=100, height=1, command=lambda: get_data_query12())
radio12.grid(row=2, column=0)
radio12.place(x=80, y=540)

quitWindow = tk.Button(page2, text="Esci", command=window.destroy, fg="black", bg="red", width=35, height=1,
                       activebackground="white", font=('times', 11, ' bold '))
quitWindow.place(x=350, y=650)

# PAGE 3
page3.config(bg='#C6E4D9')


window.mainloop()
