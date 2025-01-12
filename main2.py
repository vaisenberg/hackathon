from currency_converter_class import ILSConverter  
from Fetch_portfolio import fetch_currency_portfolio  
import psycopg2
from psycopg2 import sql
from config import DATABASE
from registration import connect_db
from datetime import datetime
from USDToILSConverter import USDToILSConverter
from EUROToILSConverter import EURConverter
from FrankToILSConverter import CHFConverter


def check_customer_exists(client_id):
    """
    Check if a customer exists in the SQL database by their unique ID and allow the user to update their balance.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    # Query to check if the customer exists
    cursor.execute("SELECT c.first_name, c.last_name, w.amount FROM clients c JOIN wallet w ON c.id = w.client_id WHERE id = %s", (client_id,))
    customer = cursor.fetchone()
    
    if customer:
        print(f"Client with ID {client_id} exists.")
        print(f"Name: {customer[1]}")  
        print(f"Current Balance: {customer[2]}")
        # print(f"Current Balance: {customer[3]:.2f} ILS") 
        
        try:
            new_balance = float(input("Enter the new balance in Shekels (ILS): "))
                
            # Update balance in the database
            cursor.execute("UPDATE wallet SET amount = %s WHERE client_id = %s", (new_balance, client_id))
            conn.commit()
            print(f"Balance for customer ID {client_id} updated to {new_balance:.2f} ILS.")
                
            # If the new balance is greater than 500, offer conversion
            if new_balance > 500:
                offer_conversion(new_balance, client_id)

            if new_balance < 0:
                resolve_negative_shekel_balance(client_id)
                
        except ValueError:
            print("Invalid input. Please enter a valid number for the balance.")
            
    else:
        print(f"No customer found with ID {client_id}.")
    
    conn.close()


def offer_conversion(amount, client_id):
    """
    If balance exceeds 500 ILS, offer the user to perform currency conversion
    and update the database with the converted amount.
    """
    print(f"Your balance is {amount:.2f} ILS.")
    convert_option = input("Would you like to convert this balance to USD, EUR, or CHF? (yes/no): ").strip().lower()
    if convert_option == 'yes':
        # Initialize the ILSConverter
        ils_converter = ILSConverter()
        # Fetch exchange rates before performing any conversion
        if ils_converter.fetch_exchange_rates():
            target_currency = input("Enter the target currency (USD, EUR, CHF): ").strip().lower()
            # Validate the currency input
            if target_currency in ["usd", "eur", "chf"]:
                converted_amount = ils_converter.convert_to(amount, target_currency.upper())
                if converted_amount is not None:
                    print(f"{amount:.2f} ILS is equivalent to {converted_amount:.2f} {target_currency.upper()}.")
                    # Update the database with the converted amount
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        # Update or insert the balance in the appropriate currency table
                        cursor.execute(
                            sql.SQL("""
                            INSERT INTO {table_name} (client_id, amount)
                            VALUES (%s, %s)
                            ON CONFLICT (client_id)
                            DO UPDATE SET amount = EXCLUDED.amount;
                            """).format(table_name=sql.Identifier(target_currency)),
                            (client_id, converted_amount)
                        )
                        # Reduce ILS balance after conversion in the wallet table
                        new_ils_balance = 0  # Set remaining ILS to 0 after full conversion
                        cursor.execute(
                            """
                            UPDATE wallet
                            SET amount = %s
                            WHERE client_id = %s;
                            """,
                            (new_ils_balance, client_id)
                        )
                        conn.commit()
                        print(f"Database updated: {converted_amount:.2f} {target_currency.upper()} added to {target_currency} table.")
                        print(f"ILS balance for client ID {client_id} updated to {new_ils_balance:.2f}.")
                    except Exception as e:
                        print(f"Error updating the database: {e}")
                        conn.rollback()
                    finally:
                        conn.close()
            else:
                print("Invalid currency. Please choose USD, EUR, or CHF.")
        else:
            print("Failed to fetch exchange rates. Conversion cannot be performed.")
    else:
        print("You chose not to perform any conversion.")

def resolve_negative_shekel_balance(client_id):
    """
    Resolve negative Shekel balance by converting available EUR, USD, and CHF balances to ILS.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Fetch current Shekel (ILS) balance
        cursor.execute("SELECT amount FROM wallet WHERE client_id = %s;", (client_id,))
        shekel_balance = cursor.fetchone()
        if not shekel_balance:
            print(f"No Shekel balance found for client ID {client_id}.")
            return
        shekel_balance = shekel_balance[0]
        # If balance is non-negative, no action needed
        if shekel_balance >= 0:
            print(f"Client ID {client_id} does not have a negative Shekel balance.")
            return
        # Fetch EUR, USD, and CHF balances
        cursor.execute("SELECT amount FROM eur WHERE client_id = %s;", (client_id,))
        eur_balance = cursor.fetchone()
        cursor.execute("SELECT amount FROM usd WHERE client_id = %s;", (client_id,))
        usd_balance = cursor.fetchone()
        cursor.execute("SELECT amount FROM chf WHERE client_id = %s;", (client_id,))
        chf_balance = cursor.fetchone()
        eur_balance = eur_balance[0] if eur_balance else 0
        usd_balance = usd_balance[0] if usd_balance else 0
        chf_balance = chf_balance[0] if chf_balance else 0
        print(f"EUR Balance: {eur_balance}, USD Balance: {usd_balance}, CHF Balance: {chf_balance}, Negative ILS Balance: {shekel_balance}")
        # Instantiate converters
        eur_converter = EURConverter()
        usd_converter = USDToILSConverter()
        chf_converter = CHFConverter()
        # Fetch exchange rates for conversion
        if not (eur_converter.fetch_exchange_rates() and usd_converter.fetch_exchange_rates() and chf_converter.fetch_exchange_rates()):
            print("Failed to fetch exchange rates. Cannot resolve negative balance.")
            return
        # Convert EUR, USD, and CHF to ILS
        eur_to_ils = eur_converter.convert_to_shekels(eur_balance) if eur_balance > 0 else 0
        usd_to_ils = usd_converter.convert_to_shekels(usd_balance) if usd_balance > 0 else 0
        chf_to_ils = chf_converter.convert_to_shekels(chf_balance) if chf_balance > 0 else 0
        total_converted_ils = eur_to_ils + usd_to_ils + chf_to_ils
        # Check if conversions can resolve the negative balance
        if total_converted_ils + shekel_balance >= 0:
            ils_to_add = -shekel_balance  # Amount needed to zero out the balance
        else:
            ils_to_add = total_converted_ils  # Convert as much as possible
        # Deduct equivalent amounts from EUR, USD, and CHF
        eur_deduct = min(ils_to_add / eur_converter.rates["ILS"], eur_balance)  # Deduct from EUR
        usd_deduct = min((ils_to_add - (eur_deduct * eur_converter.rates["ILS"])) / usd_converter.rates["USD"], usd_balance)  # Deduct from USD
        chf_deduct = min((ils_to_add - (eur_deduct * eur_converter.rates["ILS"]) - (usd_deduct * usd_converter.rates["USD"])) / chf_converter.rates["CHF"], chf_balance)  # Deduct from CHF
        # Update the database
        cursor.execute("UPDATE wallet SET amount = amount + %s WHERE client_id = %s;",
                       (ils_to_add, client_id))
        if eur_deduct > 0:
            cursor.execute("UPDATE eur SET amount = amount - %s WHERE client_id = %s;", (eur_deduct, client_id))
        if usd_deduct > 0:
            cursor.execute("UPDATE usd SET amount = amount - %s WHERE client_id = %s;", (usd_deduct, client_id))
        if chf_deduct > 0:
            cursor.execute("UPDATE chf SET amount = amount - %s WHERE client_id = %s;", (chf_deduct, client_id))
        conn.commit()
        print(f"Negative Shekel balance resolved for client ID {client_id}.")
        print(f"ILS Added: {ils_to_add:.2f}, EUR Deducted: {eur_deduct:.2f}, USD Deducted: {usd_deduct:.2f}, CHF Deducted: {chf_deduct:.2f}")
    except Exception as e:
        conn.rollback()
        print(f"Error resolving negative Shekel balance: {e}")
    finally:
        conn.close()


# Main function to run the program
def main():
    client_id = int(input("Enter the customer ID to check: "))
    check_customer_exists(client_id)

if __name__ == "__main__":
    main()
