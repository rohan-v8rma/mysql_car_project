import mysql.connector
import settings

def get_db_connection():
    db_connection = mysql.connector.connect(host = settings.db_host, user = settings.db_user\
, password = settings.db_password, database = settings.db_name, auth_plugin = settings.auth_plugin)
    cursor = db_connection.cursor()
    return [db_connection, cursor]

def get_car_types():
    db_connection, cursor = get_db_connection()
    cursor.execute('Select distinct body_type from ALL_CARS')
    type_list = []
    for record in cursor.fetchall():
        type_list.append(record[0])
    return type_list

def car_reorder(t):
    db_connection, cursor = get_db_connection()
    cursor.execute('UPDATE ALL_CARS SET Units = 3 where name = \'' + t[1] + '\'')
    db_connection.commit()
    db_connection.close()

def display_models(condition):
    db_connection, cursor = get_db_connection()
    cursor.execute('select * from ALL_CARS', condition)
    max_l1 = 0
    max_l2 = 0
    max_l3 = 0
    max_l4 = 0
    max_l5 = 0
    for model in cursor:
        name_l = len(model[1])
        serial_l = len(str(model[0]))
        bodytype_l = len(str(model[2]))
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
        if bodytype_l > max_l5:
            max_l5 = bodytype_l
    n = 3
    cursor.execute('select * from ALL_CARS', condition)
    for model in cursor:
        print(str(model[0]).rjust(max_l2) +  ' ' * n + model[1].ljust(max_l1) + ' ' * n + model[2].ljust(max_l5) + ' ' * n + str(model[3]).rjust(max_l3) + ' ' * n + str(model[4]).rjust(max_l4) )
    db_connection.close()

def get_price_range():
    max_price = 0
    db_connection, cursor = get_db_connection()
    cursor.execute('select min(price) from ALL_CARS')
    min_price = cursor.fetchall()[0][0]
    cursor.execute('select max(price) from ALL_CARS')
    max_price = cursor.fetchall()[0][0]
    return [min_price, max_price]
 
def buying_a_car(serial_number):
    db_connection, cursor = get_db_connection()
    cursor.execute('select * from ALL_CARS where serial_number = ' + str(serial_number))
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
        decrease_stock(serial_number, 1)
    elif option == 2:
        print('Thanks for visiting us. We hope to do business with you in the near future.')

def increase_stock(serial_number, increment):
    db_connection, cursor = get_db_connection() 
    cursor.execute('update ALL_CARS SET Units = Units + ' + str(increment) + ' where Serial_number = ' + str(serial_number) + ';')
    db_connection.commit()
    db_connection.close()

def is_serial_number_valid(serial_number):
    db_connection, cursor = get_db_connection() 
    cursor.execute('select * from ALL_CARS;')
    serial_list = []
    l = cursor.fetchall()
    for content in l:
        serial_list.append(content[0])
    if serial_number in serial_list:
        return  True
    else:
        return False

def price_change(serial_number, new_price):
    db_connection, cursor = get_db_connection() 
    cursor.execute('update ALL_CARS set Price = ' + str(new_price) + ' where Serial_number = ' + str(serial_number) + ';')
    db_connection.commit()
    db_connection.close()

def decrease_stock(serial_number, decrement):
    db_connection, cursor = get_db_connection() 
    cursor.execute('update ALL_CARS SET Units = Units - ' + str(decrement) + ' where Serial_number = ' + str(serial_number) + ';')
    db_connection.commit()
    db_connection.close()

def add_vehicle(name, body_type, price):
    db_connection, cursor = get_db_connection() 
    cursor.execute('select * from ALL_CARS;')
    l = cursor.fetchall()

    serial = l[-1][0]
    cursor.execute('insert into ' + table_name + ' values(' + str(serial + 1) + ', ' + '\'' + name + '\'' + ', ' + '\'' + body_type + '\'' + ', ' + str(price) + ', ' + '2);')
    db_connection.commit()
    db_connection.close()
    return serial

def remove_vehicle(serial_number):
    db_connection, cursor = get_db_connection() 
    cursor.execute('delete from ALL_CARS where Serial_number = ' + str(serial_number) + ';')
    db_connection.commit()
    db_connection.close()

def check_serial_number(serial_number):
    if is_serial_number_valid(serial_number) == True:
        return serial_number
    else:
        new_serial_number = eval(input('Enter a valid serial number for ' + selected_car_type + ' --> '))
        updated_serial_number = check_serial_number(new_serial_number)
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
        if option == 1:
            option = 0      
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
            display_models(' where price < ' + str(budget + 1))
            print('')
            input_from_user_1 = int(input('Please enter the Index of the model you want.\nEnter >>> '))
            print('')
            serial_number = check_serial_number(input_from_user_1)
            buying_a_car(serial_number)
        elif option == 2:
            break

    elif option == 2:
        print('\n')
        display_models()
        print('\n\nThese are the models in stock.')
        option = int(input('''What would you like to do?\n\n
1. Decrease units of a vehicle
2. Add units of a vehicle
3. Change price of any vehicle
4. Add a new vehicle
5. Remove a vehicle
6. Quit
Enter >>> '''))
        if option == 1:
            print('\n')
            input_from_user_1 = int(input('Which model stock do you want to reduce?\nEnter >>> '))
            input_from_user_2 = int(input('How many units do you want to reduce?\nEnter >>> '))
            serial_number = check_serial_number(input_from_user_1)
            decrease_stock(serial_number, input_from_user_2)
            print('Your changes have been made.')

        if option == 2:
            print('\n')
            input_from_user_1 = int(input('Which model stock do you want to increase?\nEnter >>> '))
            input_from_user_2 = int(input('How many units do you want to add?\nEnter >>> '))
            serial_number = check_serial_number(input_from_user_1)
            decrease_stock(serial_number, input_from_user_2)
            print('Your changes have been made.')
            
        if option == 3:
            print('\n')
            input_from_user_1 = int(input('Which model price do you want to change?\nEnter >>> '))
            input_from_user_2 = int(input('Please enter the new price.\nEnter >>> '))
            serial_number = check_serial_number(input_from_user_1)
            price_change(serial_number, input_from_user_2)
            print('Your changes have been made.')

        if option == 4:
            print('\n')
            name = str(input('Please enter the car name. \n Enter >>> '))
            l1 = name.split()
            for word in l1:
                word.capitalize()
            name = ' '.join(l1)
            price = 0
            while price <= 0 or price >= 1000000000:
                price = int(input('Please enter price of the vehicle less than 100 Crores. \nEnter >>> '))
            car_types = get_car_types()
            for index, type in enumerate(car_types()):
                print(str(index + 1) + '. ' + type)
            type_input = -1
            while type_input not in range(1, 4):
                type_input = int(input('Please choose the type of the car you are adding. \nEnter >>> '))
            vehicle = [name, type_input, price]
            add_vehicle(vehicle[0], vehicle[1], vehicle[2])
            print('New vehicle has been added. Order for addition of units has been sent to the supplier which we will recieve in a few days.')
            vehicle = [''] + vehicle
            car_reorder(vehicle)

        if option == 5:
            print('\n')
            input_serial_number = int(input('Enter serial number of vehicle to be removed >>> '))
            serial_number = check_serial_number(input_serial_number)
            remove_vehicle(serial_number)
            print('Changes Saved.')

        if option == 6:
            break
    
    elif option == 3:
        break

print('Program ended.')
