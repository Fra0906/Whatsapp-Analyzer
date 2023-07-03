import sqlite3


def connect_to_database(database):
    """
    Crea la connessione al database SQLite specificato.
    Restituisce un oggetto di connessione.
    """
    conn = sqlite3.connect(database)
    print("MySQL Database connection successful")
    return conn


def execute_select_query(conn, query, parameters=None):
    """
    Esegue una query SELECT nel database SQLite specificato.
    Restituisce i risultati della query come una lista di tuple.
    Può accettare parametri opzionali per filtrare i record.
    """
    cursor = conn.cursor()
    if parameters:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


def close_connection(conn):
    """
    Chiude la connessione al database SQLite specificato.
    """
    conn.close()


# Funzione per la scelta dell'opzione dal menù
def menu():
    print('')
    print("Menù:")
    print("1.  Visualizza i nomi di tutti i contatti")
    print("2.  Visualizza i nomi di tutti i gruppi")
    print("3.  Top 5 contatti che scrivono i messaggi più lunghi")
    print("4.  Numero medio di messaggi al giorno scambiati con un contatto nel tempo")
    print("5.  Momenti della giornata e della settimana nei quali parlo di più con uno specifico contatto.")
    print("6.  Momenti della giornata e della settimana nei quali parlo di più con un gruppo specifico.")
    print("7.  Numero di messaggi inviati da ciascun membro di un gruppo nel tempo")
    print("8.  Cercare una parola all'interno della chat con uno specifico contatto")
    print("9.  Cercare una parola tra i messaggi in uscita all'interno della chat di un gruppo specifico")
    print("10. Cercare una parola tra i messaggi in entrata all'interno della chat di un gruppo specifico")
    print("11. Contare quante volte una determinata parola è stata scritta da uno specifico utente di uno specifico "
          "gruppo")
    print("12. Contare quante volte una determinata parola è stata scritta da me all'interno di uno specifico gruppo")
    print("13. Esci")
    choice = input("Seleziona un'opzione: ")
    return choice


# Definizione delle funzioni di query SELECT
def nomiContatti(conn):
    query = "SELECT ZPARTNERNAME from ZWACHATSESSION where ZSESSIONTYPE==0 order by ZPARTNERNAME"
    results = execute_select_query(conn, query)
    print('')
    print('I nomi dei contatti sono:')
    print('')
    for row in results:
        print(row)


def nomiGruppi(conn):
    query = "select ZPARTNERNAME from ZWACHATSESSION where ZSESSIONTYPE==1 order by ZPARTNERNAME"
    results = execute_select_query(conn, query)
    print('')
    print('I nomi dei gruppi sono:')
    print('')
    for row in results:
        print(row)


# def SQL1(conn):
#     query = "SELECT friend_name, count(*) as number_of_messages FROM friend_messages WHERE date(message_date) >= " \
#             "date('now', '-30 days') GROUP BY friend_number ORDER BY number_of_messages desc"
#     results = execute_select_query(conn, query)
#     for row in results:
#         print(row)

def SQL2(conn):  
    query = "SELECT friend_name, avg(length(message_text)) as avg_message_length FROM friend_messages WHERE " \
            "message_type == 'text' and is_from_me == 0 group by friend_name order by avg_message_length desc "
    results = execute_select_query(conn, query)
    print('')
    print('I nomi dei contatti che scrivono messaggi più lunghi sono:')
    print('')
    for row in results:
        print(row)


# Definizione delle funzioni di query SELECT con record filtrati
def SQL3(conn):
    f_n = input("Inserisci il nome del contatto: ")
    query = "SELECT day, avg(number_of_messages) over (order by day asc rows 30 preceding) as ma_nom from (SELECT " \
            "date(message_date) as day, count(*) as number_of_messages from friend_messages where friend_name == ? " \
            "group by day, friend_name)"
    results = execute_select_query(conn, query, (f_n,))
    print('')
    print('Il numero medio di messaggi al giorno scambiato con il contatto', f_n, 'è:')
    print('')
    for row in results:
        print(row)


def SQL4(conn):
    f_n = input("Inserisci il nome del contatto: ")
    query = "select strftime('%w', message_date) as weekday_number,(case strftime('%w', message_date) when '0' then " \
            "'Monday' when '1' then 'Tuesday' when '2' then 'Wednesday' when '3' then 'Thursday' when '4' then " \
            "'Friday' when '5' then 'Saturday'  when '6' then 'Sunday' else 'unknown' end ) as weekday_name, " \
            "strftime('%H', message_date) as day_hour, count(*) as number_of_messages from friend_messages where " \
            "friend_name == ? group by weekday_name, day_hour order by weekday_number, day_hour "
    results = execute_select_query(conn, query, (f_n,))
    print('')
    print('I momenti della giornata e della settimana nei quali parlo di più con il contatto', f_n, 'sono:')
    print('')
    for row in results:
        print(row)


def SQL4variante(conn):
    g_n = input("Inserisci il nome del gruppo: ")
    query = "select strftime('%w', message_date) as weekday_number,(case strftime('%w', message_date) when '0' then " \
            "'Monday' when '1' then 'Tuesday' when '2' then 'Wednesday' when '3' then 'Thursday' when '4' then " \
            "'Friday' when '5' then 'Saturday'  when '6' then 'Sunday' else 'unknown' end ) as weekday_name, " \
            "strftime('%H', message_date) as day_hour, count(*) as number_of_messages from group_messages where " \
            "group_name == ? group by weekday_name, day_hour order by weekday_number, day_hour "
    results = execute_select_query(conn, query, (g_n,))
    print('')
    print('I momenti della giornata e della settimana nei quali parlo di più con il gruppo', g_n, 'sono:')
    print('')
    for row in results:
        print(row)


def SQL5(conn):
    g_n = input("Inserisci il nome del gruppo: ")
    query = "select friend_name, day, avg(number_of_sent_messages) over ( order by friend_name, day asc rows 30 " \
            "preceding ) as ma_nom from ( select ( case is_from_me when 0 then friend_name else 'Me' end) as " \
            "friend_name,date(message_date) as day,count(*) as number_of_sent_messages from group_messages where " \
            "group_name == ? group by friend_name,day )"
    results = execute_select_query(conn, query, (g_n,))
    print('')
    print('I momenti della giornata e della settimana nei quali parlo di più con il gruppo', g_n, 'sono:')
    print('')
    for row in results:
        print(row)


def SQL6(conn):
    f_n = input("Inserisci il nome del contatto: ")
    m_t = input("Inserisci il testo da cercare: ")
    query = "SELECT friend_name, message_text, message_date, message_type, is_from_me from friend_messages where " \
            "friend_name  == ? AND message_text LIKE ? "
    results = execute_select_query(conn, query, (f_n, m_t))
    print('')
    print('Cercare la parola', m_t, 'nella chat con il contatto', f_n, ':')
    print('')
    for row in results:
        print(row)


def SQL7(conn):
    g_n = input("Inserisci il nome del gruppo: ")
    m_t = input("Inserisci il testo da cercare: ")
    query = "select message_date,message_type, message_text from group_messages where group_name == ? AND is_from_me " \
            "== 1 AND message_text LIKE ? "
    results = execute_select_query(conn, query, (g_n, m_t))
    print('')
    print('Cercare la parola', m_t, 'tra i messaggi in uscita all interno della chat del gruppo', g_n, ':')
    print('')
    for row in results:
        print(row)


def SQL8(conn):
    g_n = input("Inserisci il nome del gruppo: ")
    m_t = input("Inserisci il testo da cercare: ")
    query = "select message_date,message_type, message_text, friend_name, friend_id from group_messages where " \
            "group_name == ? AND is_from_me == 0 AND message_text LIKE ? "
    results = execute_select_query(conn, query, (g_n, m_t))
    print('')
    print('Cercare la parola', m_t, 'tra i messaggi in entrata all interno della chat del gruppo', g_n, ':')
    print('')
    for row in results:
        print(row)


def SQL9(conn):
    g_n = input("Inserisci il nome del gruppo: ")
    f_n = input("Inserisci il nome del contatto:")
    m_t = input("Inserisci il testo da cercare: ")
    query = "select count(*) as number_of_messages, friend_name, friend_id, group_name, group_id from group_messages " \
            "where group_name == ? AND is_from_me == 0 AND friend_name == ? AND message_text LIKE ? "
    results = execute_select_query(conn, query, (g_n, f_n, m_t))
    print('')
    print('Contare quante volte la parola', m_t, 'è stata scritta dal contatto', f_n, 'presente nel gruppo', g_n, ':')
    print('')
    for row in results:
        print(row)


def SQL10(conn):
    g_n = input("Inserisci il nome del gruppo: ")
    m_t = input("Inserisci il testo da cercare: ")
    query = "select count(*) as number_of_messages, group_name, group_id from group_messages where group_name == ? " \
            "AND is_from_me == 1 AND message_text LIKE ? "
    results = execute_select_query(conn, query, (g_n, m_t))
    print('')
    print('Contare quante volte la parola', m_t, 'è stata scritta nel gruppo', g_n, ':')
    print('')
    for row in results:
        print(row)


# Esecuzione del menu
def main():
    conn = connect_to_database('ChatStorage.sqlite')

    while True:
        choice = menu()

        if choice == '1':
            nomiContatti(conn)
        elif choice == '2':
            nomiGruppi(conn)
        elif choice == '3':
            SQL2(conn)
        elif choice == '4':
            SQL3(conn)
        elif choice == '5':
            SQL4(conn)
        elif choice == '6':
            SQL4variante(conn)
        elif choice == '7':
            SQL5(conn)
        elif choice == '8':
            SQL6(conn)
        elif choice == '9':
            SQL7(conn)
        elif choice == '10':
            SQL8(conn)
        elif choice == '11':
            SQL9(conn)
        elif choice == '12':
            SQL10(conn)
        elif choice == '13':
            break
        else:
            print("Opzione non valida. Riprova.")

    close_connection(conn)


# Avvio del programma
if __name__ == "__main__":
    main()
