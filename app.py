from scraper import scraper
import mariadb
import sys


def app():
    df = scraper()
    try:
        connection = mariadb.connect(user='root', password='$PASSWORD', host='$HOST', port=3306, database='$DATABASE')
    except mariadb.Error as ex:
        print(f"An error occurred while connecting to MariaDB: {ex}")
        sys.exit(1)
    cursor = connection.cursor()
    cursor.execute('drop table if exists times')
    cursor.execute('create table times(id int not null auto_increment, nick varchar(100), date varchar(15), '
                   'time varchar(15), primary key(id))')
    for index, row in df.iterrows():
        cursor.execute("insert into times(nick, date, time) values(?, ?, ?)", (row['nick'], row['date'], row['time']))
    connection.commit()
    print(df)
