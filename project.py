import mysql.connector
import settings

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
    cursor.execute('show tables')
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
    cursor.execute('select * from ' + car_type + ' where serial_number = ' + str(serial_number))
    model_chosen = cursor.fetchall()[0] 
    print('The ' + model_chosen[1] + ' will cost you ' + str(model_chosen[3] * 1.28) +  ' after taxes')
    option = 0 
    while option not in [1,2]:
        option = int(input('Do you wish to buy this car? \n1. Yes \n2. No \nEnter >>> '))
        print('')
    if option == 1:
        print('Congrulations! You are now the proud owner of a ' + model_chosen[1] + '!')
        if model_chosen[-1] == 0:
            print('Since this car isn\'t currently in stock, we will place an order and deliver this car to you tomorrow.')
            car_reorder(model_chosen)
        decrease_stock(car_type, serial_number, 1)
    elif option == 2:
        print('Thanks for visiting us. We hope to do business with you in the near future.')
    
def display_car_type_list(car_types):
    for index, car_type in enumerate(car_types):
        print(str(index + 1) + '. ' + car_type.capitalize())

def select_car_type(car_types):
    display_car_type_list(car_types)
    option = 0
    while option not in range(1, len(car_types) + 1):
        option = int(input('Enter >>> '))
        print('')
    selected_car_type = car_types[option - 1]
    print('')
    display_models(selected_car_type, '')
    return selected_car_type

def increase_stock(table_name ,serial_number, increment):
    db_connection, cursor = get_db_connection() 
    cursor.execute('update ' + table_name + ' SET Units = Units + ' + str(increment) + ' where Serial_number = ' + str(serial_number) + ';')
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
    cursor.execute('update ' + table_name + ' SET Units = Units - ' + str(decrement) + ' where Serial_number = ' + str(serial_number) + ';')
    db_connection.commit()
    db_connection.close()

def add_vehicle(table_name, name, body_type, price):
    db_connection, cursor = get_db_connection() 
    cursor.execute('select * from ' + table_name + ';')
    l = cursor.fetchall()

    serial = l[-1][0]
    cursor.execute('insert into ' + table_name + ' values(' + str(serial + 1) + ', ' + '\'' + name + '\'' + ', ' + '\'' +body_type + '\'' + ', ' + str(price) + ', ' + '2);')
    db_connection.commit()
    db_connection.close()
    return serial

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

print('Welcome to the finest luxury car dealership in the country.')
while True:
    option = 0
    while option not in [1,2,3]:
        print('\n')
        option = int(input('''
1. If you are a Customer
2. If you are the Dealer/Supplier
3. Exit
Enter >>> '''))
    if option == 1:
        option = 0
        while option not in [1,2]:
            print('')
            option = int(input('''
1. Buy a car or get a quote on the car
2. Exit
Enter >>> '''))
        print('')
        if option == 2:
            break
        elif option == 1:
            option = 0
            while option not in [1,2,3]:
                option = int(input('''
1. Buy according to body type
2. Buy according to budget
3. Exit
Enter >>> '''))
                print('')
            car_types = get_car_types()
            if option == 1:
                print('')
                selected_car_type = select_car_type(car_types)
                
                input_serial_number = int(input('Enter >>> '))
                serial_number = check_serial_number(selected_car_type, input_serial_number)
                print('\n')
                buying_a_car(option, selected_car_type)
            elif option == 2:
                min_price, max_price = get_price_range()
                print('')
                print('Our cars range from ' + str(min_price/10000000) + ' Cr' + ' to ' +  str(max_price/10000000) + ' Cr')
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
                for num, car_type in enumerate(car_types):
                    print(str(num + 1) + '. ' + car_type.upper())
                    print('')
                    display_models(car_type, ' where price < ' + str(budget + 1))
                    print('')
                input_from_user_1 = int(input('Please enter the Serial Number of the body type you want.\nEnter >>> '))
                print('')
                input_from_user_2 = int(input('Please enter the Index of the model you want.\nEnter >>> '))
                print('')
                serial_number = check_serial_number(car_types[input_from_user_1 - 1], input_from_user_2)
                buying_a_car(serial_number, car_types[input_from_user_1 - 1])
            elif option == 3:
                break

    elif option == 2:
        print('\n')
        print('Car types in stock:')
        car_types = get_car_types()
        selected_car_type = select_car_type(car_types)
        print('\n\nThese are the models in stock.')
        option = int(input('''What would you like to do?\n\n
1. Decrease units of a vehicle
2. Change price of any vehicle
3. Add a new vehicle
4. Remove a vehicle
5. Quit
Enter >>> '''))
        if option == 1:
            print('\n')
            input_from_user_1 = int(input('Which model stock do you want to reduce?\nEnter >>> '))
            input_from_user_2 = int(input('How many units do you want to reduce?\nEnter >>> '))
            serial_number = check_serial_number(selected_car_type, input_from_user_1)
            decrease_stock(selected_car_type, serial_number, input_from_user_2)
            print('Your changes have been made.')

        if option == 2:
            print('\n')
            input_from_user_1 = int(input('Which model price do you want to change?\nEnter >>> '))
            input_from_user_2 = int(input('Please enter the new price.\nEnter >>> '))
            serial_number = check_serial_number(selected_car_type, input_from_user_1)
            price_change(selected_car_type, serial_number, input_from_user_2)
            print('Your changes have been made.')

        if option == 3:
            print('\n')
            name = str(input('Please enter the car name. \n Enter >>> '))
            l1 = name.split()
            for word in l1:
                word.capitalize()
            name = ' '.join(l1)
            price = 0
            while price <= 0 or price >= 1000000000:
                price = int(input('Please enter price of the vehicle less than 100 Crores. \nEnter >>> '))
            vehicle = [name, selected_car_type, price]
            add_vehicle(selected_car_type, vehicle[0], vehicle[1], vehicle[2])
            print('New vehicle has been added. Order for addition of units has been sent to the supplier which we will recieve in a few days.')
            vehicle = [''] + vehicle
            car_reorder(vehicle)

        if option == 4:
            print('\n')
            input_serial_number = int(input('Enter serial number of vehicle to be removed >>> '))
            serial_number = check_serial_number(selected_car_type, input_serial_number)
            remove_vehicle(selected_car_type, serial_number)
            print('Changes Saved.')

        if option == 5:
            break
    
    elif option == 3:
        break

print('Program ended.')
