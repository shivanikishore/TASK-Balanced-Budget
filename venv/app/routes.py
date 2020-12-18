
from app import app,db,charts
from flask import render_template,flash,redirect,url_for,request,jsonify
from app.forms import LoginForm,RegisterForm,DataForm
from flask_login import login_user,logout_user,login_required,current_user
from app.models import User,Data
# from werkzeug.urls import url_parse
import json,datetime
import psycopg2
from flask_googlecharts import LineChart
from flask_googlecharts.utils import prep_data



@app.route('/')
@login_required
def home():
    return render_template('home.html')



@app.route('/login',methods=["POST","GET"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        name=form.username.data
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.get_password(form.password.data):
            flash("Invalid Username and PAssword")
            return redirect('/login')
        login_user(user)
        return redirect(url_for('user',username=name))
    return render_template('login.html',form=form,title="Sign-In")



@app.route('/register',methods=["POST","GET"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data) 
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("U are now registered please login")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)




@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect('/')




@app.route('/user/<username>')
def user(username):
    return render_template('users.html',username=username)
@app.route('/user_l')
def user_l():
    return render_template('user_left.html')
@app.route('/user_r/<username>')
def user_r(username):
    return render_template('user_right.html',username=username)
@app.route('/top')
def top():
    return render_template('base.html')





@app.route('/dashboard')
def dashboard():
    to_balance=0
    data=Data.query.filter_by(users_id=current_user.id)
    total_list=Data.query.with_entities(Data.total).filter(Data.users_id==current_user.id).all()
    for data1 in total_list:
        to_balance+=int(data1.total)
    return render_template('dashboard.html',data=data,total_balance=to_balance)




@app.route('/addnew',methods=["GET","POST"])
def add():
    form=DataForm()
    if form.validate_on_submit():
        user=Data(date=form.date.data,amount_income=form.amount_income.data,amount_spent=form.amount_spent.data)
        income=str(form.amount_income.data)
        spent=str(form.amount_spent.data)
        if int(income)<int(spent):
            flash('Income is less than Ur Expenses')
            return redirect('/addnew')
        total=int(income) - int(spent)
        user.total=total
        currentuser=current_user
        user.users_id=current_user.id
        db.session.add(user)
        db.session.commit()
        flash('succesfully added')
        return redirect('/addnew')
    return render_template('add_new.html',form=form)






@app.route('/graph')
def graph():
    hot_dog_chart = LineChart("hot_dogs", options={"title": "Expenditure","width": 600,"height": 400},data_url=url_for('data'))
    charts.register(hot_dog_chart)
    return render_template('chart2.html')




@app.route('/data')
def data():
    conn = psycopg2.connect(database = 'expenditure', user = 'postgres', password = 'shivi562', host = '127.0.0.1', port = '5432')
    cur = conn.cursor()
    users_id=current_user.id
    cur.execute(""" SELECT * FROM ( SELECT * FROM data where users_id=users_id ORDER BY id DESC LIMIT 5) sub ORDER BY id ASC   """)
    # data=Data.query.filter_by(users_id=current_user.id)
#     SELECT * FROM (
# SELECT * FROM employees 
# ORDER BY employee_id DESC LIMIT 10) sub 
# ORDER BY employee_id ASC;
    # print(data)
    # columns = ("id", 'date', 'amount_income', 'amount_spent')
    # results = []
    # def myconverter(o):
    #     if isinstance(o, datetime.datetime):
    #         return o.__str__()
    # for row in cur.fetchall():
    # results.append(dict(zip("c", list(dict(row)))))
    # for i in range(0,len(results)):
    #     results[i]=dict(zip('c',list(results[i])))
    # with open('data_data.json', 'w') as f:
    #     json.dump(results, f,indent=2,default=myconverter)
    results=cur.fetchall()
    # print(results)
    if len(results)<=4:
        return "1"
    
    d = {"cols": [{"id": "", "label": "Date", "pattern": "", "type": "date"},
                  {"id": "", "label": "expenses", "pattern": "", "type": "number"},
                     {"id":"","label":"income","pattern":"","type":"number"}
                  ],
         "rows": [{"c": [{"v": results[0][1], "f": None}, {"v": results[0][3], "f": None}, {"v": results[0][2], "f": None}]},
                  {"c": [{"v": results[1][1], "f": None}, {"v": results[1][3], "f": None}, {"v": results[1][2], "f": None}]},
                  {"c": [{"v": results[2][1], "f": None}, {"v": results[2][3], "f": None}, {"v": results[2][2], "f": None}]},
                  {"c": [{"v": results[3][1], "f": None}, {"v": results[3][3], "f": None}, {"v": results[3][2], "f": None}]},
                  {"c": [{"v": results[4][1], "f": None}, {"v": results[4][3], "f": None}, {"v": results[4][2], "f": None}]}

        
                  ]}


    return jsonify(prep_data(d))


def prep_data(data):
    # type: (dict) -> dict
    """Takes a dict intended to be converted to JSON for use with Google Charts and transforms date and datetime
    into date string representations as described here:
    https://developers.google.com/chart/interactive/docs/datesandtimes
    TODO:  Implement Timeofday formatting"""

    for row in data['rows']:
        for val in row['c']:
            if isinstance(val['v'], datetime.datetime):
                val['v'] = "Date({}, {}, {})".format(val['v'].year,
                                                     val['v'].month-1,  # JS Dates are 0-based
                                                     val['v'].day,
                                                     val['v'].hour,
                                                     val['v'].minute,
                                                     val['v'].second,
                                                     val['v'].microsecond)

            
                
            elif isinstance(val['v'], datetime.date):
                val['v'] = "Date({}, {}, {})".format(val['v'].year,
                                                     val['v'].month-1,  # JS Dates are 0-based
                                                     val['v'].day)


   
    return data