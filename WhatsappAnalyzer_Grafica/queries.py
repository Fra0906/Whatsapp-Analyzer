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
            "strftime('%H', message_date) as day_hour, count(*) as number_of_messages from friend_messages where " \
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


def SQL1(conn):
    query = "SELECT ZPARTNERNAME from ZWACHATSESSION where ZSESSIONTYPE==0 order by ZPARTNERNAME"
    results = execute_select_query(conn, query)
    print('')
    print('I nomi dei contatti sono:')
    print('')
    for row in results:
        print(row)


def SQL2(conn):
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

def SQL3(conn):  # NON ESCE LA LISTA DI 5 MA TUTTI
    query = "SELECT friend_name, avg(length(message_text)) as avg_message_length FROM friend_messages WHERE " \
            "message_type == 'text' and is_from_me == 0 group by friend_name order by avg_message_length desc "
    results = execute_select_query(conn, query)
    print('')
    print('I nomi dei contatti che scrivono messaggi più lunghi sono:')
    print('')
    for row in results:
        print(row)


# Definizione delle funzioni di query SELECT con record filtrati
def SQL4(conn):
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


def SQL5(conn):
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


def SQL6(conn):
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


def SQL7(conn):
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


def SQL8(conn):
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


def SQL9(conn):
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


def SQL10(conn):
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


def SQL11(conn):
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


def SQL12(conn):
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