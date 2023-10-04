from sqlite3 import connect
from pandas import DataFrame
from Source.CreateDB.example_data import append_example_data

def create_db_sqlite(path):
    """Creates sqlite.db and tables in it"""
    conn = connect(path)
    curr = conn.cursor()
    curr.execute(
        'CREATE TABLE "activities" ('
            '"id" INTEGER PRIMARY KEY, '
            '"name" TEXT, '
            '"bg" TEXT, '
            '"fg" TEXT, '
            '"auto" INTEGER'
        ');'
    )
    curr.execute(
        'CREATE TABLE "data" ('
            '"id" INTEGER PRIMARY KEY, '
            '"date" TEXT, '
            '"start_time" TEXT, '
            '"main_time" INTEGER, '
            '"break_time" INTEGER, '
            '"desc" TEXT, '
            '"activity" INTEGER'
        ');'
    )
    conn.commit()
    
    df = DataFrame({
        'name': ['SOMETHING'],
        'bg': ['#808080'],
        'fg': ['#aaaaaa']
    })
    df.to_sql('activities', conn, if_exists='append', index=False)
    
    ### Only in TimerWithExampleData.exe
    # append_example_data(conn)
    
    conn.close()