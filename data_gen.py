import random
from database import MySQL_connection
import random
import string

def generate_password(length=6):
    characters = string.ascii_letters + string.digits 
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


con = MySQL_connection()
connection = con.connection

def populate_data(connection, num_actions):
    cursor = connection.cursor()

    banks = [
        'Attijariwafa Bank',
        'Banque Populaire',
        'Bank of Africa',
        'Société générale Maroc',
        'BMCI',
        'Crédit agricole du Maroc',
        'Crédit du Maroc',
        'CIH Bank'
    ]

    clients = [
        ('Alice', 1000 , generate_password()),
        ('Bob', 1500 ,generate_password()),
        ('Charlie', 2000 , generate_password()),
        ('David', 2500, generate_password()),
        ('Eve', 3000 , generate_password())
    ]

    insert_client_query = "INSERT INTO client (nom_client, solde , password) VALUES (%s, %s , %s)"
    cursor.executemany(insert_client_query, clients)
    connection.commit()
    print(f"{cursor.rowcount} records inserted into `client` table.")

    actions = []
    for i in range(1, num_actions + 1):
        bank_name = random.choice(banks)
        nombre = random.randint(1, 500) 
        prix = random.randint(10, 100)    
        actions.append((i, bank_name, nombre, prix))

    insert_action_query = "INSERT INTO action (idaction, societe, nombre, prix) VALUES (%s, %s, %s, %s)"
    cursor.executemany(insert_action_query, actions)
    connection.commit()
    print(f"{cursor.rowcount} records inserted into `action` table.")

    actions_client = [
        (1, random.randint(1, num_actions), random.randint(1, 10)),
        (2, random.randint(1, num_actions), random.randint(1, 10)),
        (3, random.randint(1, num_actions), random.randint(1, 10))
    ]

    insert_actions_client_query = "INSERT INTO actions_client (idclient, idaction, nombre) VALUES (%s, %s, %s)"
    cursor.executemany(insert_actions_client_query, actions_client)
    connection.commit()
    print(f"{cursor.rowcount} records inserted into `actions_client` table.")

    cursor.close()

def main():

    if connection:
        num_actions = 40  
        populate_data(connection, num_actions)
        connection.close()

if __name__ == "__main__":
    main()
