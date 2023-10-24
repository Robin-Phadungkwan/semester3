# Technishe documenetatie over Secret Manager

## werking website

In dit blok ben ik bezig geweest met maken van de app/website genaamd Secret Manager. Hiervoor heb ik gewerkt met Flask,MySQL,HTML,CSS en Python.
Flask kan worden gebruikt om een database met een website te verbinden en om HTML-pagina's te verbinden met elkaar.

Ik gebruik Flask om de website genaamd Secret Manager te maken, dat maak ik voor een schoolproject waarvoor ik een website of app moest maken.

De website is gemaakt om jouw geheimen en wachtwoorden te bewaren, het is vergelijkbaar met keepass.
Hieronder leg ik uit wat elk Python-bestand doet.

### db.py

In db.py wordt er verbinding gemaakt met de database en worden alle functies die in andere python bestanden waarvoor er een database wordt gebruikt gemaakt.

De functies zijn als volgt en hun gebruik:

insert_user wordt gebruikt om een user te registreren.

Hieronder de code hoe ik het heb laten werken:

```python
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
    
```

select_user wordt gebruikt zodat de user in kan loggen.
Hieronder de code hoe het werkt:

```python   
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
```

select_password wordt gebruikt zodat het wachtwoordt uit de database wordt gehaald om het te vergelijken met de plain text wat een gebruiker heeft ingetypt op de login page.
Hieronder de code hoe het werkt:

```python
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
```

insert_secret wordt gebruikt om een geheim in de table secret te stoppen met de username uit de sessie.
Hieronder de code hoe het werkt:

```python
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
```

share_secret wordt gebruikt om een geheim te delen door in de table shared het id van het geheim en de username met wie het geheim wordt gedeeld.
Hieronder de code hoe het werkt:

```python
# hier deel je het geheim met een andere gebruiker
def share_secret(secret_id,username):
    db=db_connection()
    cursor=db.cursor()
    sql = "INSERT INTO Shared (secret_id,user_name_share) VALUES (%s, %s)"
    val = (secret_id, username)
    result = cursor.execute(sql, val)
    db.commit()
    print(result)
    cursor.close()
    db.commit()

```

select_secret wordt gebruikt om de geheimen van de user te laten zien op de user pagina.
Hieronder de code hoe het werkt:

```python
# hiermee haal ik alle data uit de table secret op basis van de username
def select_secret(username):
    db = db_connection()  #connect to database
    cursor = db.cursor() #create cursor
    sql = "SELECT * FROM secrets.Secret WHERE user_name = %s" #select all from secrets table where user_name = username
    val = (username,)  # uses a tuple with the element username 
    cursor.execute(sql, val) #execute sql statement or order 66
    result = cursor.fetchall() #fetches the first row of the result
    cursor.close() #close cursor
    return result #return result
```

select_secret_share werkt net zoals select_secret gebruikt maar dan voor de geheimen die gedeelt zijn met de user door een andere user.
Hieronder de code hoe het werkt:

```python
def select_secret_share(username):
    db = db_connection()  #connect to database
    cursor = db.cursor() #create cursor
    sql = "SELECT id,name,info,user_name FROM secrets.Secret LEFT JOIN secrets.Shared ON Secret.id = Shared.secret_id where user_name_share = %s" #select all from secrets table where user_name = username
    val = (username,)  # uses a tuple with the element username 
    cursor.execute(sql, val) #execute sql statement or order 66
    result = cursor.fetchall() #fetches the first row of the result
    cursor.close() #close cursor
    return result #return result
```

update_secret wordt gebruikt om een geheim up te daten in de database aan de hand van het id van het geheim.
Hieronder de code hoe het werkt:

```python
def update_secret(name,info,id):
    db = db_connection() #connect to database
    cursor = db.cursor() #create cursor
    sql = "UPDATE Secret SET name = %s, info = %s WHERE id = %s" #update info from secrets table where name = name
    val = (name,info,id) #uses a tuple with the elements name, info, and id
    cursor.execute(sql, val) #execute sql statement or order 66
    db.commit() #commit changes or do it
    cursor.close() #close cursor
```

delete_secret_id verwijdert het geheim uit de database aan de hand van het id.
Hieronder de code hoe het werkt:

```python
def delete_secret(id): #execute order 66/ delete secret entry
    db = db_connection() #connect to database
    cursor = db.cursor() #create cursor
    sql = "DELETE FROM Secret WHERE id = %s" #delete from secrets table where id = id
    val = (id,) #uses a tuple with the element id
    cursor.execute(sql, val) #execute sql statement or order 66
    db.commit() #commit changes or do it
    cursor.close() #close cursor
```

select_secret_id selecteerd de id.
Hieronder de code hoe het werkt:

```python
def select_secret_id(id):
    db = db_connection()  #connect to database
    cursor = db.cursor() #create cursor
    sql = "SELECT id FROM Secret WHERE id = %s" #select all from secrets table where user_name = username
    val = (id,) # uses a tuple with the element id
    cursor.execute(sql, val) #execute sql statement or order 66
    result = cursor.fetchall() #fetches the first row of the result
    cursor.close() #close cursor
    return result #return result

```

### home.py

In home.py worden de routes gedefinieerd waardoor flask weet waar hij naar toe moet als een link wordt ingedrukt, voor elke route wordt er een functie gedefineerd.
Bij de routes van login en signup is zowel de GET- als de POST-methode toegevoegd om gebruikersgegevens op te slaan in de database.
De code om dat te doen is als volgt:

```python
@bp.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = select_user(username)
        hashed = select_password(username)
        #hier wordt gekeken of de username en het wachtwoord kloppen aan die in de database, zoja dan moet er hij naar de loggedin pagina.
        #de check_password_hash is een functie die kijkt of het wachtwoord klopt aan de hash en kies de eerste die hij ziet.
        if user and check_password_hash(hashed[0], password):
            session.permanent = True #hier wordt de session permanent gemaakt.
            session["username"] = username #hier wordt de username in de session gezet.
            flash("Login successful", "success")  
            return redirect(url_for('home.loggedin')) #hier wordt je gereturned naar de loggedin pagina.
        else:
            flash("Invalid username or password", "error") #hier wordt een flash op het scherm gezet als de login of password fout is.
    #als de username al in de session zit dan wordt je gereturned naar de loggedin pagina.
    if 'username' in session:
        return redirect(url_for('home.loggedin'))
    return render_template('login.html') 

# hier wordt de data dat is ingevoerd in de database gestopt en het wachtwoord word voordat hij in de database wordt gestopt eerst gehashed.
# als de user al een session heeft dan wordt hij gereturned naar de loggedin pagina.        
@bp.route('/register/',methods=['GET','POST'])
def signup(): 
    #post request om de data aan te maken
    if request.method == 'POST':
        #hier wordt de hash gemaakt van het wachtwoord.
        hashpw = generate_password_hash(request.form['password'], method= 'pbkdf2:sha256',salt_length=12)
        #hier wordt de username en het wachtwoord van de form afgenomen.
        username = request.form['username']
        #hier wordt gekeken of de username en het wachtwoord niet te lang zijn en als hij te lang is dan moet er een flash op het scherm komen.
        if len (username) > 30: #als de lengte van de username langer is dan 256 dan moet er een flash op het scherm komen.
            flash ('Username is too long')
        password = request.form['password'] # hetzelfde als hierboven maar dan voor het wachtwoord.
        if len (password) > 255:
            flash ('Password is too long')
        #hier wordt de data in de database gestopt.
        passed = insert_user(username, hashpw) #hier wordt de data in de database gestopt.
        #als de data al bestaat in de database dan moet er een flash op het scherm komen waarin wordt gezegd dat de username al bestaat(db.py) en wordt je gereturned.
        if passed == None:
            return render_template("sign-up.html")
        else:   #anders mag je naar de login pagina.
            flash ('You are now registered') 
            return redirect (url_for('home.login')) 
    if 'username' in session:
        return redirect(url_for('home.loggedin')) #als de username in de session zit dan wordt je gereturned naar de loggedin pagina.   
    return render_template("sign-up.html") #hier wordt de sign-up pagina gerendered.
```
Ik heb bij sign up gemaakt dat de username en het gehashte wachtwoord in de database wordt gestopt, om het wachtwoordt te hashen wordt er gebruik gemaakt van werkzeug, en dan de functies generate_password_hash. De functie maakt het dat het wachtwoordt met een salt lengte die je zelf kan geven maakt. Daarna wordt in login het wachtwoordt wat is ingetypt door de gebruiker vergeleken met het wachtwoordt wat in de database staat met behulp van de functie check_password_hash, als die gelijk zijn aan elkaar en de user is bekend in de database. Dan mag de gebruiker inloggen en wordt hij doorgestuurd naar zijn user pagina.

#### user pagina 
na het inloggen zie je je persoonlijke pagina met de gegevens die voor jou bedoeld zijn, inclusief je geheimen,gebruikersnaam en de gedeelde geheimen.

De manier waarop de data wordt opgehaald is via een sessie die is aangemaakt terwijl de user wordt ingelogd. De geheimen van de user zelf en de geheiemen die met de user is gedeeld worden opgehaald uit de database op basis van de username.

Hieronder de code hoe het is gedaan in home.py en db.py:

```python
def select_secret(username):
    db = db_connection()  #connect to database
    cursor = db.cursor() #create cursor
    sql = "SELECT * FROM secrets.Secret WHERE user_name = %s" #select all from secrets table where user_name = username
    val = (username,)  # uses a tuple with the element username 
    cursor.execute(sql, val) #execute sql statement or order 66
    result = cursor.fetchall() #fetches the first row of the result
    cursor.close() #close cursor
    return result #return result
```

Hierboven de code van db.py.

```python
@bp.route('/logged-in/', methods=['GET','POST'])
def loggedin():
    if 'username' in session: 
        username = session['username']
        secrets = select_secret(username) 
        shared_secrets = select_secret_share(username)
        if request.method == 'POST': 
            name = request.form['name'] 
            info = request.form['info'] 
            username = session['username'] 
            if len(name)> 30:
                flash("your name for it is too long")
            if len(info)> 255:
                flash("your secret is too long")
            insert_data = insert_secret(name,info,username) 
            flash ('You have added a secret') 
            return redirect (url_for('home.loggedin', flash=flash, username=username, insert_data=insert_data, secrets=secrets,shared_secrets=shared_secrets))
        return render_template("logged-in.html",flash=flash,secrets=secrets,shared_secrets=shared_secrets, username=username)
    else: 
        return redirect(url_for('home.login'))
```

home.py

De userpagina wordt alleen laten zien als de user is ingelogd.

### init.py

In init.py wordt de Flask-app gemaakt met daarin de definities van de routes waar alle routes worden gedefinieerd.
