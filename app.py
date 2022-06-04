import re
from flask import Flask, render_template, url_for, request, session, redirect, jsonify
import bcrypt
from flask_pymongo import PyMongo
from pymongo import ALL
app = Flask(__name__)

app.config['MONGODB_NAME'] = 'resume'
app.config['MONGO_URI'] = 'mongodb+srv://username:<password>@cluster_url/resume?ssl=true&ssl_cert_reqs=CERT_NONE'
app.config['SECRET_KEY'] = b'6hc/_gsh,./;2ZZx3c6_s,1//'

mongo = PyMongo(app)


@app.route('/')
def index():
    if 'username' in session:
        data = mongo.db.data
        resume = data.find_one({'username': session['username']})
        return render_template('index.html', resume=resume)
    return render_template('main.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        curr_user = users.find_one({'username': request.form['username']})
        if curr_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'username': request.form['username'], 'email': request.form['email'], 'password': hashpass})
            session['username'] = request.form['username']
            return render_template('form.html')
        return render_template('index.html')
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        curr_user = users.find_one({'username': request.form['username']})
        if curr_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), curr_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('form'))
            return render_template('login.html')
        return render_template('login.html')
    return render_template('login.html')


@app.route('/form')
def form():
    if 'username' in session:
        return render_template('form.html')
    return redirect(url_for('login'))


@app.route('/requirement', methods=['POST', 'GET'])
def requirement():
    if 'username' in session and request.method == 'POST':
        username = session['username']
        data = mongo.db.data
        data.insert({'username': username, 'name': request.form['name'], 'address': request.form[
                    'address'], 'email': request.form['email'], 'phone': request.form['phone'], 'coll_name': request.form['coll_name'], 'coll_year': request.form['coll_year'], 'inter_name': request.form['inter_name'], 'inter_year': request.form['inter_date'], 'high_name': request.form['high_name'],
            'high_year': request.form['high_year'], 'intern_name1': request.form['intern_name1'], 'posi_name1': request.form['posi_name1'], 'exp1': request.form['exp1'], 'intern_date1': request.form['intern_date1'], 'intern_name2': request.form['intern_name2'], 'posi_name2': request.form['posi_name2'],
            'exp2': request.form['exp2'], 'intern_date2': request.form['intern_date2'], 'proj_name1': request.form['proj_name1'], 'info1': request.form['info1'], 'proj_date1': request.form['proj_date1'], 'proj_name2': request.form['proj_name2'], 'info2': request.form['info2'],
            'proj_date2': request.form['proj_date2'], 'skill1': request.form['skill1'], 'skill2': request.form['skill2'], 'skill3': request.form['skill3'], 'skill4': request.form['skill4'], 'skill5': request.form['skill5'], 'skill6': request.form['skill6'], 'skill7': request.form['skill7'],
            'skill8': request.form['skill8'], 'skill9': request.form['skill9'], 'skill10': request.form['skill10'], 'skill11': request.form['skill11']})
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)
