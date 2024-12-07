import math
from flask import render_template, request, redirect
from app import dao
from app import app, login
from flask_login import login_user, logout_user, current_user


@app.route("/")
def index():
    cates = dao.load_categories()

    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    page = request.args.get('page', 1)
    prods = dao.load_products(cate_id=cate_id, kw=kw, page=int(page))


    page_size = app.config['PAGE_SIZE']
    page_quantity = math.ceil(dao.get_product_count() / page_size)
    return render_template('index.html',
                           categories=cates,
                           products=prods,
                           p_quan=page_quantity,
                           current_user=current_user)


@app.route('/login', methods=['get', 'post'])  # ? why have methods in decorate
def login_process():
    if request.method.__eq__("POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        u = dao.auth_user(username, password)
        if u:
            login_user(u)
            return redirect('/')

    return render_template('login.html')


@app.route('/register', methods=['get', 'post'])
def register_process():
    err_messenger = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        print(request.form)
        if password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']
            dao.add_user(**data)
            return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_messenger)


@app.route('/logout')
def logout_process():
    logout_user()
    return redirect("/login")


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
