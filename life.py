# Import necessary modules
import csv
import sqlite3
from sqlite3 import IntegrityError

# Connect to a new SQLite database (this will replace the existing one)
conn = sqlite3.connect('life_exp.sqlite')
cursor = conn.cursor()

# (Re)create the tables
cursor.execute('DROP TABLE IF EXISTS entities;')
cursor.execute('DROP TABLE IF EXISTS life_expectancy;')

cursor.execute('''
    CREATE TABLE entities (
        entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        code TEXT
    );
''')

cursor.execute('''
    CREATE TABLE life_expectancy (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_id INTEGER,
        year INTEGER NOT NULL,
        life_expectancy FLOAT NOT NULL,
        FOREIGN KEY(entity_id) REFERENCES entities(entity_id)
    );
''')

conn.commit()

'Re-creation of entities and life_expectancy tables completed.'
# Reopen the CSV file and read it using csv.DictReader for easier column access
file_path = 'life-expectancy.csv'

# Initialize a dictionary to keep track of entity names to their database IDs
entity_id_map = {}

with open(file_path, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        entity_name = row['Entity']
        entity_code = row['Code']
        year = row['Year']
        life_expectancy = row['Period life expectancy at birth - Sex: all - Age: 0']
        
        # Insert entity if not already done
        if entity_name not in entity_id_map:
            try:
                cursor.execute('INSERT INTO entities (name, code) VALUES (?, ?)', (entity_name, entity_code))
                conn.commit()
                # Store the newly inserted entity's ID
                entity_id_map[entity_name] = cursor.lastrowid
            except IntegrityError:
                # This block should not be reached due to the UNIQUE constraint, but it's here as a safeguard
                cursor.execute('SELECT entity_id FROM entities WHERE name = ?', (entity_name,))
                entity_id_map[entity_name] = cursor.fetchone()[0]
        
        # Insert life expectancy data
        cursor.execute('''
            INSERT INTO life_expectancy (entity_id, year, life_expectancy) VALUES (?, ?, ?)
        ''', (entity_id_map[entity_name], year, life_expectancy))

conn.commit()
conn.close()

'Direct CSV reading and data insertion into entities and life_expectancy tables completed.'
