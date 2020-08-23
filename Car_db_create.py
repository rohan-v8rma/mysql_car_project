import mysql.connector

p = 'root'

mydb = mysql.connector.connect(host = 'localhost', user = 'root'\
, password = p, auth_plugin = 'mysql_native_password')
mycursor = mydb.cursor()

mycursor.execute('CREATE DATABASE Cars')
mycursor.execute('USE Cars')
mydb.commit()

mycursor.execute('''CREATE TABLE Saloon(Serial_number int PRIMARY KEY
, Name varchar(30), Body_type varchar(20),  Price int, Units int)''')
mycursor.execute('''
INSERT INTO Saloon
VALUES (1, \'Mercedes Maybach S650\', \'Saloon\', 55000000, 3)''')
mycursor.execute(''' 
INSERT INTO Saloon
VALUES (2, \'BMW M5 Competition\', \'Saloon\', 23000000, 12)''')
mycursor.execute('''
INSERT INTO Saloon
VALUES (3, \'Audi A8 W12 Quattro\', \'Saloon\', 37000000, 5)
''')

mycursor.execute('''CREATE TABLE SUV(Serial_number int PRIMARY KEY
, Name varchar(30), Body_type varchar(20), Price int, Units int)''')
mycursor.execute('''
INSERT INTO SUV
VALUES (1, \'Lamborghini Urus\', \'SUV\', 30000000, 6) 
''')
mycursor.execute('''
INSERT INTO SUV
VALUES (2, \'Rolls Royce Cullinan\', \'SUV\', 70000000, 8) 
''') 
mycursor.execute(''' 
INSERT INTO SUV
VALUES (3, \'Aston Martin DBX\', \'SUV\', 45000000, 3) 
''')

mycursor.execute('''CREATE TABLE Supercar(Serial_number int PRIMARY KEY
, Name varchar(30), Body_type varchar(20), Price int, Units int)''')
mycursor.execute(''' 
INSERT INTO Supercar
VALUES (1, \'Koenigsiegg Regera\', \'Supercar\', 110000000, 4) 
''')
mycursor.execute('''
INSERT INTO Supercar
VALUES (2, \'Lamborghini Essenza\', \'Supercar\', 150000000, 2)  
''')
mycursor.execute(''' 
INSERT INTO Supercar
VALUES (3, \'Porsche 911 GT4 RS\', \'Supercar\', 21000000, 7) 
''')

mydb.commit()
mydb.close()