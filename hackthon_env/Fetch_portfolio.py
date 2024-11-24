def fetch_currency_portfolio(client_id):
    """
    Fetches the currency portfolio for a specific client from USD, EUR, and CHF tables.
    
    :param client_id: The ID of the client.
    :return: A dictionary with currency as keys and their amounts as values.
    """
    conn = connect_db()
    cursor = conn.cursor()
    portfolio = {}

    try:
        # Query USD table
        cursor.execute("SELECT amount FROM usd WHERE client_id = %s;", (client_id,))
        usd_balance = cursor.fetchone()
        portfolio['USD'] = usd_balance[0] if usd_balance else 0.0

        # Query EUR table
        cursor.execute("SELECT amount FROM eur WHERE client_id = %s;", (client_id,))
        eur_balance = cursor.fetchone()
        portfolio['EUR'] = eur_balance[0] if eur_balance else 0.0

        # Query CHF table
        cursor.execute("SELECT amount FROM chf WHERE client_id = %s;", (client_id,))
        chf_balance = cursor.fetchone()
        portfolio['CHF'] = chf_balance[0] if chf_balance else 0.0

    except Exception as e:
        print(f"Error fetching portfolio: {e}")
        portfolio = None

    finally:
        cursor.close()
        conn.close()
    print(portfolio)
    return portfolio
