# from faker import Faker
# import json
from random import randint
# import psycopg2
# from psycopg2 import sql
# from datetime import datetime
# from config import DATABASE
# import requests
# from spendemic import Wallet

# fake = Faker()
# countries = ['Israel','USA','ES','Switzerland']
generated_numbers = set()
def generate_unique_number():
    while True:
        unique_number = randint(10000, 99999)
        if unique_number not in generated_numbers:
            generated_numbers.add(unique_number)
            print(f'Your login: "{unique_number}"') 
            return unique_number

# def generate_phone_number():
#     return f"05{randint(100000000, 999999999)}"  

# def _connect_db():
#     conn = psycopg2.connect(**DATABASE)
#     return conn





# def add_new_user(x):
#     user_data = {}
#     for i in range(0, x):
#         user_data[i] = {}
#         user_data[i]['unique_number'] = generate_unique_number() 
#         user_data[i]['first_name'] = fake.first_name()  
#         user_data[i]['last_name'] = fake.last_name()  
#         user_data[i]['phone'] = generate_phone_number()  
#         user_data[i]['country'] = 'Israel'  

        
#         save_user_to_db(user_data[i])

    # print(user_data)
    
    # # dictionary dumped as json in a json file  
    # with open('users.json', 'w') as fp:  
    #     json.dump(user_data, fp)  

# def save_user_to_db(user):
#     conn = _connect_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO clients (unique_number, first_name, last_name, phone, country) 
#         VALUES (%s, %s, %s, %s, %s) RETURNING id
#     """, (user['unique_number'], user['first_name'], user['last_name'], user['phone'], user['country']))
#     client_id = cursor.fetchone()[0] 

#     while True:
#         try:
#             amount = float(input("How much money you have? "))
#             if amount < 0:
#                 print("Amount cannot be negative. Please try again.")
#             else:
#                 break
#         except ValueError:
#             print("Invalid input. Please enter a valid number.")

#     cursor.execute("""
#         INSERT INTO wallet (client_id, amount) 
#         VALUES (%s, %s)
#     """, (client_id, amount))

#     conn.commit()
#     conn.close()

# add_new_user()