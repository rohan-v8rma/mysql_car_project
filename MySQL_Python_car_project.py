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

def car_sold(t):
    db_connection, cursor = get_db_connection()
    cursor.execute('UPDATE ' + t[2] + ' SET Units = Units - 1 where name = \'' + t[1] + '\'')
    db_connection.commit()
    db_connection.close()

def display_models(t, condition):
    db_connection, cursor = get_db_connection()
    cursor.execute('select * from ' + t, condition)
    models = []
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
        else:
            pass
        if serial_l > max_l2:
            max_l2 = serial_l
        else:
            pass
        if price_l > max_l3:
            max_l3 = price_l
        else:
            pass
        if unit_l > max_l4:
            max_l4 = unit_l
    n = 3
    cursor.execute('select * from ' + t + condition)
    for model in cursor:
        print(str(model[0]).rjust(max_l2) +  ' ' * n + model[1].ljust(max_l1) + ' ' * n + model[2] + ' ' * n + str(model[3]).rjust(max_l3) + ' ' * n + str(model[4]).rjust(max_l4) )
    return [models ,len(str(model[0]).rjust(max_l2) +  ' ' * n + model[1].ljust(max_l1) + ' ' * n + model[2] + ' ' * n + str(model[3]).rjust(max_l3) + ' ' * n + str(model[4]).rjust(max_l4) )]
    db_connection.close()

def car_types():
    db_connection, cursor = get_db_connection()
    cursor.execute('show tables')
    car_type = []
    for x in cursor:
        car_type.append(x[0])
    db_connection.close()
    return car_type

def max_min_checker():
    max = 0
    min = ''
    db_connection, cursor = get_db_connection()
    cursor.execute('''show tables''')
    tables = cursor.fetchall()
    for table in tables:
        name = table[0]
        cursor.execute('select min(price) from ' + name)
        price1 = cursor.fetchall()[0][0]
        if min == '':
            min = price1
        elif price1 < min:
            min = price1
        cursor.execute('select max(price) from ' + name)
        price2 = cursor.fetchall()[0][0]
        if price2 > max:
            max = price2
    return (max, min)
 
def buying_a_car(serial, type):
    db_connection, cursor = get_db_connection()
    cursor.execute('Select * from ' + type + ' where serial_number = ' + str(serial))
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
        car_sold(model_chosen)
    elif option == 2:
        print('Thanks for visiting us. We hope to do business with you in the near future.')
'''Menu for DBMS'''


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
            car_types = car_types()
            if option == 1:
                count = 1
                for t in car_types:
                    print(str(count) + '.', t.capitalize())
                    count += 1
                option = 0
                while option not in range(1, len(car_types) + 1):
                    option = int(input('\nEnter >>> '))
                    print('')
                selected_type = car_types[option - 1]
                models = display_models(selected_type, '')[0]
                option = int(input('\nEnter >>> '))
                print('')
                buying_a_car(option, selected_type)
            elif option == 2:
                max_min = max_min_checker()
                print('Our cars range from ' + str(max_min[1]/10000000) + ' Cr' + ' to ' +  str(max_min[0]/10000000) + ' Cr')
                print('')
                budget = 'r'
                while budget[-1].lower() != 'cr': 
                    budget = input('Please enter your max budget in the specified range in the format <1 Cr>\n\nEnter >>> ')
                    print('')
                    budget = budget.split()
                budget = float(budget[0]) * 10000000
                if budget < max_min[1]:
                    print('Sorry! No cars are available within your budget.')
                    break
                print('')
                for car_type in car_types:
                    print(car_type.upper())
                    print('')
                    models = display_models(car_type, ' where price < ' + str(budget + 1))[0]
                    print('')
                k = []
                while len(k) != 2:
                    k = eval(input('Please enter Serial No and Body type of the car you want to buy in this format <[1, "Saloon"]> \n\nEnter >>> '))
                    print('')
                buying_a_car(k[0], k[1])
            elif option == 3:
                break

    # elif option == 2:
    
    elif option == 3:
        break
print('Program ended.')