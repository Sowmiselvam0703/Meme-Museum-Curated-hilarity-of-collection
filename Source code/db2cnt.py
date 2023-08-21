from flask import *
import ibm_db
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bfd76926;PWD=LlT33W9dy1RVnlXG" ,'' ,'')
print(conn)
app=Flask(__name__)
@app.route('/')
def home():
    return render_template("Mainpage.html")
@app.route('/login')
def login():
    return render_template("Signin.html")
@app.route('/register')
def register():
    return render_template("Reg.html")
@app.route('/register1',methods = ['POST'])
def register1():
    x = [x for x in request.form.values()]
    print(x)
    NAME = x[0]
    EMAIL = x[1]
    PASSWORD = x[2]
   
    sql="SELECT * FROM REGISTER WHERE EMAIL =?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,EMAIL)
    ibm_db.execute(stmt)    
    account=ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        return render_template('Signin.html',pred="You are already a member,please login using your credentials")
    else:
        insert_sql="INSERT INTO REGISTER VALUES (?,?,?)"
        prep_stmt = ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt, 1 , NAME)
        ibm_db.bind_param(prep_stmt, 2 , EMAIL)
        ibm_db.bind_param(prep_stmt, 3 , PASSWORD)
        ibm_db.execute(prep_stmt)
        return render_template( 'Signin.html' , pred =  "Registration successful, please login using your details")

@app.route('/login1',methods = ['POST'])
def login1():
    NAME = request.form['NAME']
    EMAIL = request.form['EMAIL']
    sql = "SELECT * FROM REGISTER WHERE NAME =? AND EMAIL=?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,NAME)
    ibm_db.bind_param(stmt,2,EMAIL)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    print(NAME,EMAIL)
    if account:
        return render_template('Signin.html', pred = "Login successful")
    else:
        return render_template('Signin.html',pred = "Login unsuccessful.Incorrect username/password!")
if __name__ == "__main__":
    app.run(debug = True, port = 5000 )