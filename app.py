from flask import Flask, render_template, flash, request, url_for, redirect, make_response
from flask_mysqldb import MySQL
import secrets
import string
import time
import hashlib
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_bytes(16)

# Configuration For MySql Database
db = yaml.load(open('db.yaml'), Loader=yaml.Loader)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


#Valid Location checker
def check_valid_location(lat, long):
    """Checks if the Location is from srilanka"""
    if float(long) > 79.5 and float(long) < 82:
        if float(lat) > 5.8 and float(lat) < 9.9:
            return True
        return False
    return False

# create a unique filename for each report pic
def generate_unique_filename():
    timestamp = str(int(time.time()))  # Get current timestamp as a string
    random_string = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
    unique_filename = f"{timestamp}_{random_string}"
    return unique_filename


# file upload control
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])
def allowed_file(filename): # this function checks if file is allowed to be uploaded
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create Tables if doesnt Exist
def create_table_if_not_exists():
    try:
        cur = mysql.connection.cursor()
        print("Database Connection Successful!!!!")

        cur.execute('''
            CREATE TABLE IF NOT EXISTS userinfo (
                    user_id INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(30) UNIQUE KEY,
                    password VARCHAR(250),
                    useris VARCHAR(10),
                    vehicle_reg_no VARCHAR(20) UNIQUE KEY,
                    vehicle_type VARCHAR(20),
                    f_name VARCHAR(50),
                    l_name VARCHAR(50),
                    full_name VARCHAR(100)
                );
            
            CREATE TABLE IF NOT EXISTS reports (
                    reportid INT PRIMARY KEY AUTO_INCREMENT,
                    vehicle_reg_no VARCHAR(30),
                    vehicle_type VARCHAR(20),
                    FOREIGN KEY(vehicle_reg_no) REFERENCES userinfo(vehicle_reg_no),
                    report_title VARCHAR(200),
                    city VARCHAR(100),
                    longitude VARCHAR(100),
                    latitude VARCHAR(100),
                    report_pic VARCHAR(500)
            );
            ''')
        cur.close()
        mysql.connection.commit()
        print("Created userinfo and reports Table")

    except Exception as e:
        print("Failed To Connect With Database or Table Creation", e)


# Funtion to get Repeated User Data
def get_user_data(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM userinfo WHERE username = %s", (str(id),))
    user_data = cursor.fetchone()
    cursor.close()
    return user_data 


# Home Page After Login
@app.route("/home")
def home():
    if request.cookies.get('username'):
        user_data = get_user_data(request.cookies.get('username'))

        read_only_user_data = [user_data[1], user_data[3], user_data[4], user_data[5], user_data[7]]  # username, useris, vehicleid, vehicletype, fullname
    else:
        flash("Login First !")
        return redirect('/')

    if request.cookies.get('username') == user_data[1]: #Selecting the username from db data and verifing with cookie username again
        if read_only_user_data[1] == "Police" or read_only_user_data[1] == "RDA-Staff":
            try:
                cursor = mysql.connection.cursor()

                # Chart Data 
                # Pie Chart Accidents Caused by Different Types of Vehicles
                query1 = """SELECT COUNT(vehicle_type) as Accidents, vehicle_type from reports group by vehicle_type"""
                cursor.execute(query1)
                accidents = cursor.fetchall()
                accident_dict = {}
                for accident in accidents:
                    accident_dict[accident[1]] = accident[0]

                # Histogram Chart Accdients per City
                query2 = """SELECT COUNT(city) as Accidents, city from reports group by city"""
                cursor.execute(query2)
                cities = cursor.fetchall()
                city_dict = {}
                for city_accident in cities:
                    city_dict[city_accident[1]] = city_accident[0]

                cursor.execute("SELECT * FROM reports;")
                all_reports = cursor.fetchall()
                cursor.close()
                return render_template('home.html', data=read_only_user_data, all_reports=all_reports, accident_dict=accident_dict, city_dict=city_dict)
            
            except Exception as e:
                print("Error : ", e) # Most Likely Database Error. I have Redirected to Logout Bcz too many flash message will keep looping if not logged out rare case never happens
                flash("Error in Processing ! Contact Support !")
                return redirect('/logout')
        
        else:
            return render_template('home.html', data=read_only_user_data)
    else:
        flash("Invalid Login/Login First/Wrong Credentials !")
        return redirect('/logout')


@app.route("/", methods=['POST', 'GET'])
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.cookies.get('username'):
        return redirect('/home')
    
    if request.method == 'POST':
        id = request.form['userid']
        password = request.form['password']
        encripted_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        # Verify if User-in-database
        cur = mysql.connection.cursor()
        query = "SELECT * FROM userinfo WHERE username = %s AND password = %s"
        cur.execute(query, (id, encripted_password))
        user_data = cur.fetchone()
        cur.close()

        if bool(user_data): #User Verified
            # Adding Cookie and Logging In
            resp = make_response(redirect("/home"))
            resp.set_cookie('username', id)
            return resp
        else:
            flash('Account Not Found... Check Credentials !')
            return redirect(url_for('login'))

    return render_template("login.html")


# Logout /Deleting Cookie
@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('username', expires=0)
    return resp

# User Sign Up
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.cookies.get('username'):
        return redirect('/home')
    
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        vehicle_reg_no = request.form['vehicle_reg_no']
        vehicle_type = request.form['vehicle']
        id = request.form['username']
        password = request.form['password']
        encripted_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        # Check if Username or vehicle_reg_no already Registered
        cursor = mysql.connection.cursor()
        check1 = cursor.execute("""SELECT * FROM userinfo WHERE username = %s""", (str(id),))
        check2 = cursor.execute("""SELECT * FROM userinfo WHERE vehicle_reg_no = %s""", (str(vehicle_reg_no),))
        
        if check1 == 0 and check2 == 0:   # if username and vehicle_reg_no plate not registered 
            try:
                query = """
                            INSERT INTO userinfo (username, password, useris, vehicle_reg_no, vehicle_type, f_name, l_name, full_name) VALUES
                            (%s, %s, 'Resident', %s, %s, %s, %s, CONCAT(f_name, " ", l_name));
                        """
                cursor.execute(query, (id, encripted_password, vehicle_reg_no, vehicle_type, fname, lname))
                mysql.connection.commit()
                cursor.close()
                flash("Account Created ! Login Now !")
                return redirect('/')
            
            except Exception as e:
                print("Error when Data Inserting !", e)
                flash("Error Registering !!")
                return redirect('/signup')

        else: # Username exists or vehicle registered
            flash("Username Exists Or Vehicle Registered Already !! Recheck !")
            return redirect('/signup')

    return render_template("signup.html")


# Registration of authority-RDASTAFF,POLICE
@app.route("/authority-registration", methods=['POST', 'GET'])
def authority_reg():
    if len(get_user_data(request.cookies.get('username'))) > 0 and get_user_data(request.cookies.get('username'))[3] == "Admin":
        # Adding Authority User to Database
        username = request.form['username']
        password = request.form['password']
        encripted_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        fname = request.form['fname']
        lname = request.form['lname']
        useris = request.form.get('cecky')

        try:
            cursor = mysql.connection.cursor()
            # Check if username Exists
            alreadyexist = cursor.execute("""
                SELECT * FROM userinfo WHERE username = %s
            """, (str(username),))
            
            if alreadyexist == 0: # It Doesnt Exist
                query = """
                            INSERT INTO userinfo (username, password, useris, vehicle_reg_no, f_name, l_name, full_name) VALUES
                            (%s, %s, %s, NULL, %s, %s, CONCAT(f_name, " ", l_name));
                        """
                cursor.execute(query, (username, encripted_password, useris, fname, lname))
                mysql.connection.commit()
                cursor.close()

                flash("Account Created Successfully !")
            else: # It Exists
                cursor.close()
                flash("Username Exists Please Choose Another !")

        except Exception as e:
            print("Error : ", e)

        return redirect('/home')
    else:
        return redirect('/')


# Report Sending + Saving 
@app.route("/send-report", methods=['POST', 'GET'])
def process_report():
    if len(get_user_data(request.cookies.get('username'))) > 0 and get_user_data(request.cookies.get('username'))[3] == "Resident":
        user_data = get_user_data(request.cookies.get('username'))

        # Adding Report to Database
        report_title = request.form['report_title']
        request.form.get('cecky')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        city = request.form['city']
        file = request.files['file']

        if check_valid_location(latitude, longitude):
            if allowed_file(file.filename): #checks if file is an image
                filename = f"{generate_unique_filename()}.{file.filename.rsplit('.', 1)[1].lower()}"
                # now we add the report and save the picture in ./static/reportimages
                cur = mysql.connection.cursor()
                query = """
                        INSERT INTO reports (vehicle_reg_no, vehicle_type, report_title, longitude, latitude, city, report_pic) VALUES
                        (%s, %s, %s, %s, %s, %s, %s);
                        """
                try:
                    cur.execute(query, (user_data[4], user_data[5], report_title, longitude, latitude, city, filename))
                    mysql.connection.commit()
                    cur.close()

                    # Now save the file to static folder
                    file.save(f"static/reportimages/{filename}")
                    flash("Report Sent ! ")
                    return redirect('/')

                except Exception as e:
                    cur.close()
                    print("Error While Uploading Report : ", e)
                    flash("Error in Report Processing !")
                    return redirect('/')
            else:
                flash("Upload jpg, png, jpeg only !")
                return redirect('/')
        else:
            flash("Please Select a Location Inside Srilanka !")
            return redirect('/')
    else:
        flash("Invalid !")
        return redirect('/')
            

if __name__ == "__main__":
    with app.app_context():
        create_table_if_not_exists()

    app.run(host="0.0.0.0", debug=True)
