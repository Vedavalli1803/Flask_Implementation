from flask import Flask,request,render_template
import pymysql as pms
from book_recommendation import a
deck = a()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("form_login.html")
conn = pms.connect(host="127.0.0.1", 
                   port=3306,
                   user="root",
                   password="Vedavalli@1234",
                   db="login")
cur = conn.cursor()
@app.route('/signup',methods=['POST','GET'])
def signup():
    return render_template('form_signup.html')

@app.route('/form_signup',methods=['POST','GET'])
def form_signup():
        user=request.form['username']
        pwd=request.form['password']
        cur.execute(f'Select password from login where username = "{user}";')
        data=cur.fetchall()
        if(len(data)==0):
            cur.execute(f'INSERT into login values("{user}","{pwd}");')
            conn.commit()
            return render_template('form_login.html')
        else:
            return render_template('form_login.html',info='Already existing')
@app.route('/form_login',methods=['POST','GET'])
def form_login():
    user=request.form['username']
    pwd=request.form['password']
    print(user,pwd)
    cur.execute(f'Select password from login where username = "{user}";')
    data=cur.fetchall()
    if(len(data)==1 and data[0][0]==pwd):
        return render_template('home.html')
    else:
        return render_template('form_login.html',info='Invalid Credials')

@app.route('/home',methods=['Post','GET'])
def home():
    name=request.form['name']
    x = deck.xoxo(name)
    return render_template('home.html',info=x)
if __name__ == '__main__':
    app.run()