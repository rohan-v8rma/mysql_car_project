import mysql.connector
import settings
import time

def get_db_connection():
    db_connection = mysql.connector.connect(host = settings.db_host, user = settings.db_user\
, password = settings.db_password, database = settings.db_name, auth_plugin = settings.auth_plugin)
    cursor = db_connection.cursor()
    return [db_connection, cursor]

def car_reorder(t):
    db_connection, cursor = get_db_connection()
    cursor.execute('UPDATE ' + t[2] + ' SET Units = 3 where name = \'' + t[1] + '\'')
    db_connection.commit()
    db_connection.close()

def display_models(table_name, condition):
    db_connection, cursor = get_db_connection()
    cursor.execute('select * from ' + table_name, condition)
    max_l1 = 0
    max_l2 = 0
    max_l3 = 0
    max_l4 = 0 
    for model in cursor:
        name_l = len(model[1])
        serial_l = len(str(model[0]))
        price_l = len(str(model[3]))
        unit_l = len(str(model[4]))
        if name_l > max_l1:
            max_l1 = name_l
        if serial_l > max_l2:
            max_l2 = serial_l
        if price_l > max_l3:
            max_l3 = price_l
        if unit_l > max_l4:
            max_l4 = unit_l
    n = 3
    cursor.execute('select * from ' + table_name, condition)
    for model in cursor:
        print(str(model[0]).rjust(max_l2) +  ' ' * n + model[1].ljust(max_l1) + ' ' * n + model[2] + ' ' * n + str(model[3]).rjust(max_l3) + ' ' * n + str(model[4]).rjust(max_l4) )
    db_connection.close()

def get_car_types():
    db_connection, cursor = get_db_connection()
    cursor.execute('show tables')
    car_types = []
    for x in cursor:
        car_types.append(x[0])
    db_connection.close()
    return car_types

def get_price_range():
    max_price = 0
    db_connection, cursor = get_db_connection()
    cursor.execute('''show tables''')
    tables = cursor.fetchall()
    for index, table in enumerate(tables):
        name = table[0]
        cursor.execute('select min(price) from ' + name)
        selected_min_price = cursor.fetchall()[0][0]
        if index == 0 or selected_min_price < min_price:
            min_price = selected_min_price
        cursor.execute('select max(price) from ' + name)
        selected_max_price = cursor.fetchall()[0][0]
        if selected_max_price > max_price:
            max_price = selected_max_price
    return [min_price, max_price]
 
def buying_a_car(serial_number, car_type):
    db_connection, cursor = get_db_connection()
    cursor.execute('Select * from ' + car_type + ' where serial_number = ' + str(serial_number))
    model_chosen = cursor.fetchall()[0] 
    print('The ' + model_chosen[1] + ' will cost you ' + str(model_chosen[3] * 1.28) +  ' after taxes')
    option = 0 
    while option not in [1,2]:
        option = int(input('Do you wish to buy this car? \n1. Yes \n2. No \n\n Enter >>> '))
        print('')
    if option == 1:
        print('Congrulations! You are now the proud owner of a ' + model_chosen[1] + '!')
        if model_chosen[-1] == 0:
            print('Since this car isn\'t currently in stock, we will place an order and deliver this car to you tomorrow.')
            car_reorder(model_chosen)
        decrease_stock(car_type, serial_number, 1)
    elif option == 2:
        print('Thanks for visiting us. We hope to do business with you in the near future.')
'''Menu for DBMS'''
    
def display_car_type_list(car_types):
    for index, car_type in enumerate(car_types):
        print(str(index + 1) + '. ' + car_type.capitalize())

def select_car_type(car_types):
    display_car_type_list(car_types)
    option = 0
    while option not in range(1, len(car_types) + 1):
        option = int(input('\nEnter >>> '))
        print('')
    selected_car_type = car_types[option - 1]
    display_models(selected_car_type, '')
    return selected_car_type

def increase_stock(table_name ,serial_number, increment):
    db_connection, cursor = get_db_connection() 
    cursor.execute('UPDATE ' + table_name + ' SET Units = Units + ' + str(increment) + ' where Serial_number = ' + str(serial_number) + ';')
    db_connection.commit()
    db_connection.close()

def is_serial_number_valid(table_name, serial_number):
    db_connection, cursor = get_db_connection() 
    cursor.execute('select * from ' + table_name + ';')
    serial_list = []
    l = cursor.fetchall()
    for content in l:
        serial_list.append(content[0])

    if serial_number in serial_list:
        return  True
    else:
        return False

def price_change(table_name, serial_number, new_price):
    db_connection, cursor = get_db_connection() 
    cursor.execute('update ' + table_name + ' set Price = ' + str(new_price) + ' where Serial_number = ' + str(serial_number) + ';')
    db_connection.commit()
    db_connection.close()

def decrease_stock(table_name, serial_number, decrement):
    db_connection, cursor = get_db_connection() 
    cursor.execute('UPDATE ' + table_name + ' SET Units = Units - ' + str(decrement) + ' where Serial_number = ' + str(serial_number) + ';')
    db_connection.commit()
    db_connection.close()

def add_vehicle(table_name, name, body_type, price):
    db_connection, cursor = get_db_connection() 
    cursor.execute('select * from ' + table_name + ';')
    l = cursor.fetchall()

    serial = l[-1][0]
    cursor.execute('insert into ' + table_name + ' values(' + str(serial + 1) + ', ' + '\'' + name + '\'' + ', ' + '\'' +body_type + '\'' + ', ' + str(price) + ', ' + '0);')
    db_connection.commit()
    db_connection.close()
    return serial

def supp_reroll(table_name):
    db_connection, cursor = get_db_connection() 
    cursor.execute('update ' + table_name + ' set Units = Units + 2 where Units = 0;')
    db_connection.commit()
    db_connection.close()

def remove_vehicle(table_name, serial_number):
    db_connection, cursor = get_db_connection() 
    cursor.execute('delete from ' + table_name + ' where Serial_number = ' + str(serial_number) + ';')
    db_connection.commit()
    db_connection.close()

def check_serial_number(selected_car_type, serial_number):
    if is_serial_number_valid(selected_car_type, serial_number) == True:
        return serial_number
    else:
        new_serial_number = eval(input('Enter a valid serial number for ' + selected_car_type + ' --> '))
        updated_serial_number = check_serial_number(selected_car_type, new_serial_number)
        return updated_serial_number

print('Welcome to the finest luxury car dealership in the country. \n')
while True:
    option = 0
    while option not in [1,2,3]:
        option = int(input('1. if you are a Customer \n2. if you are the Dealer/Supplier \n3. to exit \n\nEnter >>> '))
        print('')
    if option == 1:
        option = 0
        while option not in [1,2]:
            option = int(input('1. if you want to buy a car or get a quote on the car \n2. to exit \n\nEnter >>> '))
            print('')
        if option == 2:
            break
        elif option == 1:
            option = 0
            while option not in [1,2,3]:
                option = int(input('1. if you want to buy according to body type \n2. if you want to buy according to budget \n3. to exit \n\nEnter >>> '))
                print('')
            car_types = get_car_types()
            if option == 1:
                selected_car_type = select_car_type(car_types)
                option = int(input('\nEnter >>> '))
                print('')
                buying_a_car(option, selected_car_type)
            elif option == 2:
                min_price, max_price = get_price_range()
                print('Our cars range from ' + str(min_price/10000000) + ' Cr' + ' to ' +  str(max_price/10000000) + ' Cr')
                print('')
                budget = 'r'
                while budget[-1].lower() != 'cr': 
                    budget = input('Please enter your max budget in the specified range in the format <1 Cr>\n\nEnter >>> ')
                    print('')
                    budget = budget.split()
                budget = float(budget[0]) * 10000000
                if budget < min_price:
                    print('Sorry! No cars are available within your budget.')
                    break
                print('')
                for car_type in car_types:
                    print(car_type.upper())
                    print('')
                    display_models(car_type, ' where price < ' + str(budget + 1))
                    print('')
                k = []
                while len(k) != 2:
                    k = eval(input('Please enter Serial No and Body type of the car you want to buy in this format <[1, "Saloon"]> \n\nEnter >>> '))
                    print('')
                buying_a_car(k[0], k[1])
            elif option == 3:
                break

    elif option == 2:
        print('Here is our whole catalogue:\n')
        car_types = get_car_types()
        selected_car_type = select_car_type(car_types)
        print('Hello Owner. Here is our market.')
        option = int(input('What would you like to do?\n\n1. to decrease units of a vehicle\n2. to change price of any vehicle\n3. to add new car brand\n4. to remove the whole vehicle brand\n5. quit\n\nENTER--> '))

        if option == 1:
            input_from_user = eval(input('Enter serial number of vehicle and the decrement in form <[serial, decrement]>--> '))
            serial_number = check_serial_number(selected_car_type, input_from_user[0])
            decrease_stock(selected_car_type, serial_number, input_from_user[1])
            print('Your changes have been made.')

        if option == 2:
            input_from_user = eval(input('Enter serial number of vehicle and new price in form <[serial, new_price]>--> '))
            serial_number = check_serial_number(selected_car_type, input_from_user[0])
            price_change(selected_car_type, serial_number, input_from_user[1])
            print('Your changes have been made.')

        if option == 3:
            vehicle = eval(input('Enter the details of desired car in form <[Name, Body_Type, Price]>--> '))
            while True:
                if str(vehicle[2]).isnumeric() == False:
                    print('Kindly enter a valid price!')
                    m = vehicle
                    vehicle = eval(input('Enter the details of desired car in form <[Name, Body_Type, Price]>-->(or press q to quit)'))

                    if vehicle == 'q':
                        m, vehicle = vehicle, m
                        break
                    else:
                        continue
                elif vehicle[2]>1000000000:
                    print('Price out of budget!!')
                    vehicle = eval(input('Enter the details of desired car in form <[Name, Body_Type, Price]>--> '))
                else:
                    break

            if str(vehicle[2]).isnumeric() == True and vehicle[2] < 1000000000:
                add_vehicle(selected_car_type, vehicle[0], vehicle[1], vehicle[2])

                print('New car brand has been added. Order for addition of units has been sent to the supplier which we will recieve in a few days.')
                print('Parsing Order.....')
                time.sleep(7)
                supp_reroll(selected_car_type)
            else:
                break

        if option == 4:
            input_serial_number = int(input('Enter serial number of vehicle to be removed--> '))
            serial_number = check_serial_number(selected_car_type, input_serial_number)
            remove_vehicle(selected_car_type, serial_number)
            supp_reroll(selected_car_type)
            print('Changes Saved.')

        if option == 5:
            break
    
    elif option == 3:
        break

print('Program ended.')