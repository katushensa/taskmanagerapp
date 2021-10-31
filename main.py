from flask import Flask, render_template, request, redirect, url_for #render_template - возвращает html страниццу, request - чтобы получать данные
import pymysql, os
from config import host, user, password, db_name
from flask_login import LoginManager, login_user, login_required, logout_user




app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager(app) #экземпляр
########################################################################################################################
try:
    db = pymysql.connect(
             host=host,
             port=3306,
              user=user,
              password=password,
             database=db_name,
             cursorclass=pymysql.cursors.DictCursor ) # параметры для подключения к бд

   # try:
       # with db.cursor() as cursor:

          #  create_table_user_info = "CREATE TABLE `users` (id INT AUTO_INCREMENT,  login VARCHAR(32), email VARCHAR(32), " \
                                    #   " password VARCHAR(40), PRIMARY KEY (id))";
           # cursor.execute(create_table_user_info)
            #print('TABLE created successfully...')

    #finally:
   #     db.close()


    # try:
    #
    #     with db.cursor() as cursor:
    #
    #
    #         create_table_user_info = "CREATE TABLE `tasks` (id INT AUTO_INCREMENT,  id_user INT,  " \
    #                                   " task VARCHAR(100), PRIMARY KEY (id))";
    #         cursor.execute(create_table_user_info)
    #         print('TABLE created successfully...')
    #
    # finally:
    #    db.close()





except Exception as ex:
    print('Connection refused...')
    print(ex)

#######################################################################################################################
class UserLogin():
    def fromDB(self, user_id, db):
        self.__user = getUser(user_id)
        return self
    def create(self, user):
        self.__user = user
        return self
       # print(str(self.__user[0]))

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        #global id
       # print()
        return str(self.__user[0])









def getUser(user_id):
    print(user_id, 'user_id')
    try:
        with db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `users`  WHERE id = {user_id} LIMIT 1;")
            res = cursor.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            return res
            print(res, 'res')
    except Exception as ex:
            print(ex)

    return False


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, db)

@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tm', methods = ['POST', 'GET'])
@login_required
def tm():
    if request.method == 'GET':
        # with db.cursor() as cursor:
        #     cursor.execute(("SELECT `task` FROM `tasks` WHERE id_user =  %s;"), (id[0]['id']))
        #     tasks = cursor.fetchall()
        #     db.commit()
        #     print(tasks)
        #
        return render_template('tm.html')
    elif request.method == 'POST':

        t = request.form['task']
        global db, email1
        with db.cursor() as cursor:
            cursor.execute(("SELECT `id` FROM `users` WHERE email =  %s;"), (email1))
            global id
            id = cursor.fetchall()
            db.commit()
            print(id[0]['id'], 'id')
            # sql = "INSERT INTO `users` (login, email, password) VALUES ()"
            cursor.execute("INSERT INTO `tasks` (id_user, task) VALUES (%s, %s);",
                           (id[0]['id'], t))
            db.commit()
            print('IN TABLE added successfully...')

    print(t)


    return render_template('tm.html')



@app.route('/task_list', methods = ['POST', 'GET'])
@login_required
def task_list():
    global db, email1
    if request.method == 'GET':
        with db.cursor() as cursor:
            cursor.execute(("SELECT `id` FROM `users` WHERE email =  %s;"), (email1))
            id = cursor.fetchall()
            #print(id[0]['id'])
            cursor.execute(("SELECT `task` FROM `tasks` WHERE id_user =  %s;"), (id[0]['id']))
            tasks = cursor.fetchall()
            task_list_user = []
            for i in range(len(tasks)):
                task_list_user.append(tasks[i]['task'])
                #task_list_users = "<br>".join([str(elem) for elem in task_list_user])
            db.commit()
            print(task_list_user)

    elif request.method == 'POST':

        with db.cursor() as cursor:
            cursor.execute(("SELECT `id` FROM `users` WHERE email =  %s;"), (email1))
            id = cursor.fetchall()
            cursor.execute(("DELETE FROM `tasks` WHERE id_user =  %s;"), (id[0]['id']))
            cursor.fetchall()
            db.commit()
        return render_template('index.html')

    return render_template('task_list.html', task_list_user=task_list_user)




@app.route('/registration', methods = ['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        global db
        if request.form['login'] != '':
            login = request.form['login']
        else:
            return "Введите верные данные"

        if request.form['email'] != '':
            email = request.form['email']
        else:
            return "Введите верные данные"

        if request.form['password'] != '':
            password = request.form['password']
        else:
            return "Введите верные данные"



        print(login, email, password)
        with db.cursor() as cursor:
            #sql = "INSERT INTO `users` (login, email, password) VALUES ()"
            cursor.execute("INSERT INTO `users` (login, email, password ) VALUES (%s, %s, %s);", (login, email, password))
            db.commit()
            print('IN TABLE added successfully...')

        return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    global db
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        user = request.form['email1']
        with db.cursor() as cursor:
            global email1
            email1 = request.form['email1']
            password1 = request.form['password1']
            #cursor.execute(("SELECT `password` FROM `users` WHERE email =  %s;"), (email1))
            auto = cursor.execute(("SELECT * FROM `users` WHERE email =  %s;"), (email1))
            #result = cursor.fetchall()
            #print(result)
           # db.commit()
            if auto == 1:
                cursor.execute(("SELECT `password` FROM `users` WHERE email =  %s;"), (email1))
                passw = cursor.fetchall()
                db.commit()
               # print(passw[0]['password'], password1)
                if passw[0]['password'] == password1:
                    userlogin = UserLogin().create(user)
                    login_user(userlogin)
                    return redirect(url_for('index'))
                else:
                    return 'Введен неверный пароль'

            else:
                return 'Имя пользователя не найдено'
    return render_template('login.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    if request.method == 'GET':
        return render_template('logout.html')
    elif request.method == 'POST':
        logout_user()
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/timer_pomodoro',  methods=['POST', 'GET'])
@login_required
def timer_pomodoro():
    if request.method == 'GET':
        return render_template('timer_pomodoro.html')


if __name__ == '__main__':
    app.run(debug=True)
