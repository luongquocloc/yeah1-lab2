#!/usr/bin/python

import sqlite3

def main():
    conn = sqlite3.connect('DB.db')
    ####Create table Detail
    conn.execute('''
        CREATE TABLE detail(
            id  INTEGER PRIMARY KEY AUTOINCREMENT,            
            name    TEXT,
            url    TEXT    NOT NULL,
            type    TEXT,
            likes    TEXT,
            love    TEXT,
            haha    TEXT,
            angry    TEXT,
            sad    TEXT,
            wow    TEXT,
            total_react    TEXT,
            created_date    TEXT
        );
    ''')

    print("create table cate & detail successfully")
    conn.close()

main()

