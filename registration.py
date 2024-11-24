from random import randint
import psycopg2
from psycopg2 import sql
from datetime import datetime
from config import DATABASE

def connect_db():
    return psycopg2.connect(**DATABASE)

generated_numbers = set()
def generate_unique_number():
    while True:
        unique_number = randint(10000, 99999)
        if unique_number not in generated_numbers:
            generated_numbers.add(unique_number)
            print(f'Your login: "{unique_number}"') 
            return unique_number
        
class User:
    def __init__(self, unique_number):
        self.unique_number = unique_number
    
    def client_exists(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM clients WHERE unique_number = %s", (self.unique_number,))
        result = cursor.fetchone()
        conn.close()
        if result is None:
            # print(f"Client with unique_number {self.unique_number} does not exist.")
            # print('You can create a new account:')  
            unique_number = generate_unique_number()
            print(f"New client generated with ID: {unique_number}")

            first_name = input('Write your name:') 
            last_name = input('Write your last name:') 
            phone = input('Write your phone:') 
            country = 'Israel'  
            # column 

            self.save_user_to_db(unique_number, first_name, last_name, phone, country)
            return False
        else:
            return True
    
    def save_user_to_db(self, unique_number, first_name, last_name, phone, country):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clients (unique_number, first_name, last_name, phone, country)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, (unique_number, first_name, last_name, phone, country))
        client_id = cursor.fetchone()[0] 
        conn.commit()
        conn.close()

        self.register_big_spent(client_id)

    def register_big_spent(self, client_id):
        print("Please provide details for your big purchase.")
        month = input("Enter the month of your big purchase (MM): ")
        month = f"{month.zfill(2)}-01"

        try:
            month = datetime.strptime(month, "%m-%d").date().replace(year=datetime.today().year)
        except ValueError:
            print("Invalid date format. Please enter the month in MM format.")
            return

        amount = float(input("Enter the total amount of the big purchase in shekels: "))

        self.save_big_spent(client_id, month, amount)

    def save_big_spent(self, client_id, month, amount):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM clients WHERE id = %s", (client_id,))
        result = cursor.fetchone()

        if result is None:
            print(f"Client with id {client_id} does not exist. Cannot register big spent.")
            conn.close()
            return

        cursor.execute("""
            INSERT INTO big_purchases (client_id, month, amount)
            VALUES (%s, %s, %s)
        """, (client_id, month, amount))

        conn.commit()
        conn.close()

        print('Account succesfully registered!')
        print("Big spent successfully registered!")
