import mysql.connector
import time
p = 'gorgon123' #add your pass
#main input and queries
#continue from option2
def select_table(table_name):
    conn = mysql.connector.connect(user='root', password=p, host='localhost', database='cars', port=3306,
                                   auth_plugin='mysql_native_password')
    mycur = conn.cursor()
    mycur.execute('select * from ' + table_name + ';')
    l = mycur.fetchall()
    str1 = ''
    for i in l:
        print(str(i))
    conn.close()
def show_tables():
    conn = mysql.connector.connect(user='root', password=p, host='localhost', database='cars', port=3306,
                                   auth_plugin='mysql_native_password')
    mycur = conn.cursor()
    mycur.execute('use cars;')
    mycur.execute('show tables;')
    car_type = []
    for type in mycur:
        car_type.append(type[0])

    conn.close()
    count = 1
    for i in car_type:
        z = i.capitalize()
        print(str(count)+ '. ' + z)
        count +=1
def increase_stock(table_name ,serial_number, increment):
    conn = mysql.connector.connect(user='root', password=p, host='localhost', database = 'cars', port=3306, auth_plugin='mysql_native_password')
    mycur = conn.cursor()
    mycur.execute('UPDATE ' + table_name + ' SET Units = Units + ' + str(increment) + ' where Serial_number = ' + str(serial_number) + ';')
    conn.commit()
    conn.close()

def serial_check(table_name, serial):
    conn = mysql.connector.connect(user='root', password=p, host='localhost', database='cars', port=3306,
                                   auth_plugin='mysql_native_password')
    mycur = conn.cursor()
    mycur.execute('select * from ' + table_name + ';')
    serial_list = []
    l = mycur.fetchall()
    for content in l:
        serial_list.append(content[0])

    if serial in serial_list:
        return  True
    else:
        return False



def price_change(table_name, serial, new_price):
    conn = mysql.connector.connect(user='root', password=p, host='localhost', database='cars', port=3306,
                                   auth_plugin='mysql_native_password')
    mycur = conn.cursor()
    mycur.execute('update ' + table_name + ' set Price = ' + str(new_price) + ' where Serial_number = ' + str(serial) + ';')
    conn.commit()
    conn.close()

def decrease_stock(table_name, serial_number, decrement):
    conn = mysql.connector.connect(user='root', password=p, host='localhost', database='cars', port=3306,
                                   auth_plugin='mysql_native_password')
    mycur = conn.cursor()
    mycur.execute('UPDATE ' + table_name + ' SET Units = Units - ' + str(decrement) + ' where Serial_number = ' + str(serial_number) + ';')
    conn.commit()
    conn.close()
def add_vehicle(table_name, name, body_type, price):
    r = ('insert into ' + table_name + ' values(' + str(5) + ', ' + '\'' + name + '\'' + ', ' + '\'' +body_type + '\'' + ', ' + str(price) + ', ' + '0);')
    conn = mysql.connector.connect(user='root', password=p, host='localhost', database='cars', port=3306,
                                   auth_plugin='mysql_native_password')
    mycur = conn.cursor()
    mycur.execute('select * from ' + table_name + ';')
    l = mycur.fetchall()

    serial = l[-1][0]
    mycur.execute('insert into ' + table_name + ' values(' + str(serial + 1) + ', ' + '\'' + name + '\'' + ', ' + '\'' +body_type + '\'' + ', ' + str(price) + ', ' + '0);')
    conn.commit()
    conn.close()
    return serial


def supp_reroll(table_name):

    conn = mysql.connector.connect(user='root', password=p, host='localhost', database='cars', port=3306,
                                   auth_plugin='mysql_native_password')
    mycur = conn.cursor()
    mycur.execute('update ' + table_name + ' set Units = Units + 2 where Units = 0;')
    conn.commit()
    conn.close()

def remove_vehicle(table_name, serial):
    conn = mysql.connector.connect(user='root', password=p, host='localhost', database='cars', port=3306,
                                   auth_plugin='mysql_native_password')
    mycur = conn.cursor()
    mycur.execute('delete from ' + table_name + ' where Serial_number = ' + str(serial) + ';')
    conn.commit()
    conn.close()

#def add_new_type()





while True:
    option = int(input('Are you the Owner or a Supplier?\n\n1. if you are the Owner\n2. if you are a supplier\n\nENTER->>> '))
    if option == 1:
        print('Here is our whole catalogue:\n')
        show_tables()
        option = (input('Which one do you want to change(enter tablename)--> '))
        select_table(option)
        print('Hello Owner. Here is our market.')
        option = int(input('What would you like to do?\n\n1. to decrease units of a vehicle\n2. to change price of any vehicle\n3. to add new car brand\n4. to remove the whole vehicle brand\n5. quit\n\nENTER--> '))

        if option == 1:
            option = eval(input('Enter serial number of vehicle and the decrement in form <[serial, decrement]>--> '))
            while True:
                check = serial_check(inp, option[0])
                if check == True:
                    break
                else:
                    print('Enter a valid serial number!!')
                    option = eval(input('Enter serial number of vehicle and the decrement in form <[serial, decrement]>--> '))
                decrease_stock(inp, option[0], option[1])
                print('Your changes have been made.')

        if option == 2:

            option = eval(input('Enter serial number of vehicle and new price in form <[serial, new_price]>--> '))
            while True:
                valid = serial_check(inp, option[0])
                if valid == True:
                    break
                else:
                    print('Enter an existing serial number!!')
                    option = eval(input('Enter serial number of vehicle and new price in form <[serial, new_price]>--> '))

            price_change(inp, option[0], option[1])
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

            if str(vehicle[2]).isnumeric() == True and vehicle[2]<1000000000:
                add_vehicle(inp, vehicle[0], vehicle[1], vehicle[2])

                print('New car brand has been added. Order for addition of units has been sent to the supplier which we will recieve in a few days.')
                print('Parsing Order.....')
                time.sleep(7)
                supp_reroll(inp)
            else:
                break
        if option == 4:
            ser = int(input('Enter serial number of vehicle to be removed--> '))
            while True:
                check = serial_check(inp, ser)
                if check == True:
                    break
                else:
                    print('Corresponding vehicle not found. pls check your entry')
                    ser = input('Enter serial number of vehicle to be removed in form--> ')



            remove_vehicle(inp, ser)
            supp_reroll(inp)
            print('Changes Saved.')


        if option == 5:
            break


print('\n')
print('HOPE TO SEE YOU AGAIN OWNER.')







