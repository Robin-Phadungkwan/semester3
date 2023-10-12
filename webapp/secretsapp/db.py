from flask import g as app_context_global, flash
import mysql.connector


def db_connection(): #maak een functie die kan worden gebruikt om connectie te maken met de database
    """This function can be called to access the database connection while handling a request"""
    if 'db' not in app_context_global:
        # TODO: store config in config file
        # TODO: do not store secrets on git

        app_context_global.db = mysql.connector.connect( #connect to database
            host="secrets-db",# secrets db gebruiken in docker en extern localhost
            user="secrets",
            password="BestPassword",
            database="secrets"
        )
    return app_context_global.db


def teardown_db(exception):
    db = app_context_global.pop('db', None)

    if db is not None:
        db.close()

# hier maak ik een functie waarmee ik de username en het gehashte wachtwoord in de database kan stoppen.
# als er een username wordt gestuurd die al in de database staat dan wordt er een error message geflasht en wordt het niet in de database gezet.
def insert_user(username, hashpw):
    try:
        db = db_connection()
        cursor = db.cursor()
        sql = "INSERT INTO User (username, password_hash) VALUES (%s, %s)"
        val = (username, hashpw)
        result = cursor.execute(sql, val)
        db.commit()
        print(result)
        print ("Record inserted successfully into users table")
        cursor.close()
        db.commit()
        return True # als het is gelukt return true
    except mysql.connector.Error as err: #als er een username bestaat return none
        if err.errno == 1062:
         # This is the MySQL error code for duplicate entry
            flash("Username already exists", "error") #flash error message
        else: #als er een andere error is return ook none
            # Handle other database errors here
            flash("An error occurred while processing your request", "error")
        return None #als het niet is gelukt return none
    
# hier maak ik een functie waarmee ik de username kan selecteren uit de database
def select_user(username):
    db = db_connection()  # Assuming this function returns a database connection
    cursor = db.cursor()
    sql = "SELECT username FROM User WHERE username = %s"
    val = ( username,)  # Use a tuple with a single element
    cursor.execute(sql, val)
    result = cursor.fetchone()
    cursor.close()
    db.commit()
    return result

#hieronder maak ik een functie waarmee ik de password_hash kan selecteren uit de database met de username als input
def select_password(username):
    db = db_connection()  # Assuming this function returns a database connection
    cursor = db.cursor() #create cursor
    sql = "SELECT password_hash FROM User WHERE username = %s"  #select password_hash from User where username = username
    val = ( username,)  # Use a tuple with a single element
    cursor.execute(sql, val) #execute sql statement or order 66
    result = cursor.fetchone() #fetches the first row of the result
    cursor.close()  #close cursor
    db.commit() #commit changes or do it
    return result

#hieronder maak ik een functie waarmee ik de data dat de gebuiker heeft gebruiker heeft ingevoerd in de database kan stoppen
def insert_secret(name,info,username):
    db = db_connection() #connect to database
    cursor = db.cursor() #create cursor
    sql = "INSERT INTO Secret (name,info,user_name) VALUES (%s, %s, %s)" #insert data into secrets table
    val = (name,info,username) #uses a tuple with the elements name, info, and username
    result = cursor.execute(sql, val) #execute sql statement or order 66
    db.commit() #commit changes or do it
    print(result) #print result
    cursor.close() #close cursor
    db.commit() #commit changes again 


def share_secret(id,username_share):
    db=db_connection()
    cursor=db.cursor()
    sql = "INSERT INTO secret (id,user_name) VALUES (%s, %s)"
    val = (id,username_share)
    result = cursor.execute(sql, val)
    db.commit()
    print(result)
    cursor.close()
    db.commit()

# hiermee kan ik het uit de database halen
def select_secret(username):
    db = db_connection()  #connect to database
    cursor = db.cursor() #create cursor
    sql = "SELECT * FROM Secret WHERE user_name or username_shared = %s" #select all from secrets table where user_name = username
    val = (username,)  # uses a tuple with the element username 
    cursor.execute(sql, val) #execute sql statement or order 66
    result = cursor.fetchall() #fetches the first row of the result
    cursor.close() #close cursor
    return result #return result
# hiermee kan je het geheimen uit de database halen op basis van het id
def delete_secret(id): #execute order 66/ delete secret entry
    db = db_connection() #connect to database
    cursor = db.cursor() #create cursor
    sql = "DELETE FROM Secret WHERE id = %s" #delete from secrets table where id = id
    val = (id,) #uses a tuple with the element id
    cursor.execute(sql, val) #execute sql statement or order 66
    db.commit() #commit changes or do it
    cursor.close() #close cursor