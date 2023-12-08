import mysql.connector

connection = mysql.connector.connect(host="localhost",user="root",password="12345678",database="telegram_users")

def checkUserExists(userId):    
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (userId,))
        user_exists = cursor.fetchone() is not None
        cursor.close()
        return user_exists
    except Exception as e:
        print(e)
        
def createUser(user_id,name,phone_number,role,username,password):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (user_id, name, phone_number, role, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (user_id, name, phone_number, role, username, password))
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False
def loginUser(username,password):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        return user is not None
    except Exception as e:
        print(e)
        return False

def updateUserData(user_id,name,phone_number,role,username,password):
    try:
        cursor = connection.cursor()
        update_query = (
                    "UPDATE users SET name = %s, phone_number = %s, role = %s, "
                    "username = %s, password = %s WHERE user_id = %s"
                )
        cursor.execute(update_query, (name, phone_number, role, username, password, user_id))
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False
def getAllDrivers():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE role = 'driver'"
        cursor.execute(query)
        drivers = cursor.fetchall()
        cursor.close()
        return drivers
    except Exception as e:
        print(e)
        return []
    
def bookRide(user_id, start_latitude, start_longitude, destination_latitude,destination_longitude):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO ride (user_id, start_latitude, start_longitude, destination_latitude, destination_longitude) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (user_id, start_latitude, start_longitude, destination_latitude, destination_longitude))
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        ride_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        return ride_id
    except Exception as e:
        print(e)
        return None
    

def getBookedRide(id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM ride WHERE id = %s"
        cursor.execute(query, (id,))
        booked_ride = cursor.fetchone()
        cursor.close()
        return booked_ride
    except Exception as e:
        print(e)
        return None

def getUser(user_id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user
    except Exception as e:
        print(e)
        return None
    
def getUserbyName(name):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE name = %s"
        cursor.execute(query, (name,))
        user = cursor.fetchone()
        cursor.close()
        return user
    except Exception as e:
        print(e)
        return None