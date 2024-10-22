import openai
from openai import OpenAI
import sqlite3

# create your own file and add your own openai api
from api_key import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

client = OpenAI(
    api_key = OPENAI_API_KEY
)

services_data = [
    ('Toronto', '123-456-7890'),
    ('Vancouver', '234-567-8901'),
    ('New York', '111-222-3333'),
    ('Los Angeles', '444-555-6666')
]

def create_db(name='psych_services.db'):
    connection = sqlite3.connect(name)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            location_name TEXT PRIMARY KEY,
            phone_number TEXT
        );
    ''')
    connection.commit()

    return connection, cursor


def insert_data(connection, cursor, data=None):
    if data == None:
        cursor.executemany('''
            INSERT OR IGNORE INTO services (location_name, phone_number) 
            VALUES (?, ?)
        ''', services_data)

    connection.commit()


def query_data(cursor, command = 'SELECT * FROM services'):
    cursor.execute(command)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    return rows

def end_connection(connection, cursor):
    cursor.close()
    connection.close()


## main function
def retrieve_number(prompt):
    # db realted 
    connection, cursor = create_db(name='psych_services.db')
    insert_data(connection, cursor)
    
    system_prompt = "I have a database: services (location_name TEXT PRIMARY KEY, phone_number TEXT). First extract the location name from the user input, then use the location name as key, generate a SQL query to query the phone number from the databse. Only ouput the SQL query without format setting!"

    conversation_history = [
        {"role": "system", "content": system_prompt}
    ]

    conversation_history.append({'role': 'user', 'content': prompt})
        
    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        temperature = 0,
        messages = conversation_history
    )
    
    sql_command = completion.choices[0].message.content
    print(sql_command)

    query_data(cursor, command=sql_command)
    end_connection(connection, cursor)


if __name__ == '__main__':
    connection, cursor = create_db()
    insert_data(connection, cursor)
    query_data(cursor)
    end_connection(connection, cursor)
    # retrieve_number('I live in Toronto.')
