import mysql.connector
import settings

db_connection = mysql.connector.connect(host = settings.db_host, user = settings.db_user\
, password = settings.db_password, auth_plugin = settings.auth_plugin)
cursor = db_connection.cursor()

cursor.execute('CREATE DATABASE ' + settings.db_name)
cursor.execute('USE ' + settings.db_name)
db_connection.commit()

cursor.execute('''CREATE TABLE ALL_CARS(Serial_number int PRIMARY KEY
, Name varchar(30), Body_type varchar(20),  Price int, Units int)''')
cursor.execute('''
INSERT INTO ALL_CARS
VALUES (1, \'Mercedes Maybach S650\', \'Saloon\', 55000000, 3)''')
cursor.execute(''' 
INSERT INTO ALL_CARS
VALUES (2, \'BMW M5 Competition\', \'Saloon\', 23000000, 12)''')
cursor.execute('''
INSERT INTO ALL_CARS
VALUES (3, \'Audi A8 W12 Quattro\', \'Saloon\', 37000000, 5)
''')
cursor.execute('''
INSERT INTO ALL_CARS
VALUES (4, \'Lamborghini Urus\', \'SUV\', 30000000, 6) 
''')
cursor.execute('''
INSERT INTO ALL_CARS
VALUES (5, \'Rolls Royce Cullinan\', \'SUV\', 70000000, 8) 
''') 
cursor.execute(''' 
INSERT INTO ALL_CARS
VALUES (6, \'Aston Martin DBX\', \'SUV\', 45000000, 3) 
''')
cursor.execute(''' 
INSERT INTO ALL_CARS
VALUES (7, \'Koenigsiegg Regera\', \'Supercar\', 110000000, 4) 
''')
cursor.execute('''
INSERT INTO ALL_CARS
VALUES (8, \'Lamborghini Essenza\', \'Supercar\', 150000000, 2)  
''')
cursor.execute(''' 
INSERT INTO ALL_CARS
VALUES (9, \'Porsche 911 GT4 RS\', \'Supercar\', 21000000, 7) 
''')

db_connection.commit()
db_connection.close()
