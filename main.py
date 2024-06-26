from flask import Flask, render_template, redirect, abort, request

from data.dish_parser import search_dishes, translate
from forms.dish import SearchDishForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import form
from data.parse_products import search_product, dish_hendler

from data import db_session
from data.dishes import Dishes
from data.users import User
from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(application)
res = []


def main():
    db_session.global_init("db/blogs.db")
    application.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@application.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(Dishes).order_by(-Dishes.id).filter(Dishes.is_private != True)
    if current_user.is_authenticated:
        news = db_sess.query(Dishes).order_by(-Dishes.id).filter(
            (Dishes.user == current_user) | (Dishes.is_private != True))
    else:
        news = db_sess.query(Dishes).order_by(-Dishes.id).filter(Dishes.is_private != True)
    return render_template("index.html", news=news)


@application.route("/search_dish/", methods=['GET', 'POST'])
def search_dish():
    form = SearchDishForm()
    global res
    res = []
    if form.validate_on_submit():
        request = form.title.data
        mass = form.mass.data
        res.append(search_dishes(request, mass))
        if None in res:
            res.append("Error")
        return render_template('search_dish.html', title='Найти блюдо',
                               form=form, dishes=res, name=form.title.data)
    return render_template('search_dish.html', title='Найти блюдо',
                           form=form, dishes=res)


@application.route("/publish_dish/", methods=['GET', 'POST'])
def publish_dish():
    global res
    c_dish = res[0]["items"][0]
    db_sess = db_session.create_session()
    dish = Dishes()
    dish.title = translate(c_dish["name"], "ru")
    dish.calories = c_dish["calories"]
    dish.size = c_dish["serving_size_g"]
    dish.protein = c_dish["protein_g"]
    dish.sodium = c_dish["sodium_mg"]
    dish.potassium = c_dish["potassium_mg"]
    dish.cholesterol = c_dish["cholesterol_mg"]
    dish.carbohydrates_total = c_dish["carbohydrates_total_g"]
    dish.fiber = c_dish["fiber_g"]
    dish.sugar = c_dish["sugar_g"]
    current_user.news.append(dish)
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect('/')


@application.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@application.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Dishes()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@application.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Dishes).filter(Dishes.id == id,
                                          Dishes.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Dishes).filter(Dishes.id == id,
                                          Dishes.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@application.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Dishes).filter(Dishes.id == id,
                                      Dishes.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@application.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        c_user = db_sess.query(User).filter(User.id == id
                                            ).first()
        return render_template("profile.html", about=c_user.about)


products = []
send_products = []


@application.route('/create_dish', methods=["GET", "POST"])
def create_dish():
    global products
    if request.method == "POST":
        products.append((request.form.get('input_product'), request.form.get('input_mass')))
        return render_template('list_create_dish.html', products=products, form=form)
    else:
        products = []
        return render_template('create_dish.html', form=form)


@application.route('/dish_saved', methods=['POST'])
def dish_saved():
    try:
        global products
        list_products = search_product(products)
        answer = dish_hendler(list_products)
        products = []
        return render_template('dish_saved.html', form=form, answer=answer)
    except TypeError:
        return render_template('error_input_product.html', form=form)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
