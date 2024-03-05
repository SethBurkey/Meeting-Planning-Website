import sqlite3

connection = sqlite3.connect('flightDB.db')
cursor = connection.cursor()

#Define database schema
#cursor.execute('DROP TABLE IF EXISTS flights')
cursor.execute('''CREATE TABLE IF NOT EXISTS flights
                (id INTEGER PRIMARY KEY,  
                 origin_location TEXT,
                 dest_location TEXT, 
                 price TEXT,
                 departure_time TEXT)''') 
# arrival_time DATETIME)''')

#Test data
#cursor.execute("DELETE FROM flights")

#cursor.execute("INSERT INTO flights (origin_location, dest_location, price, departure_time) VALUES (?, ?, ?, ?)", ('OHARE', 'JFK', 43.43, '2024-03-03 08:00:00'))
#cursor.execute("INSERT INTO flights (origin_location, dest_location, price, departure_time) VALUES (?, ?, ?, ?)", ('x', 'y', 'z', '2024-03-03 10:00'))


# Commit the transaction
connection.commit()

# Fetch and print the data from the table
cursor.execute("SELECT * FROM flights")
print(cursor.fetchall())

# Close the connection
connection.close()
