from app.models import Category, Product, User
from app import app, db
import hashlib


def load_categories():
    return Category.query.order_by("id").all()


def load_products(cate_id=None, kw=None, page=1):
    query = Product.query

    if cate_id:
        query = query.filter(Product.category_id == cate_id)

    if kw:
        query = query.filter(Product.name.contains(kw))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)
    return query.all()


def get_product_count():
    return Product.query.count()


def auth_user(username, password):  # filter mechanism is what ?
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    u = User.query.filter(User.username.__eq__(username),
                          User.password.__eq__(password))
    return u.first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_user(name, username, password):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    u = User(name=name, username=username, password=password)
    User()
    db.session.add(u)
    db.session.commit()

