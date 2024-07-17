from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, g, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user, user_loaded_from_request
from flask_socketio import SocketIO
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, joinedload
from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, func, asc
from werkzeug.security import generate_password_hash, check_password_hash
# from openai import OpenAI

import random
import pandas as pd
import os
import io
import re

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_name):
    user_get = db.session.execute(db.select(User).where(User.user_name == user_name)).scalar()
    if not user_get:
        session.pop('_user_id', None)
        session.pop('csrf_token', None)
    return db.get_or_404(User, user_name)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///serveys.db")
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     'pool_size': 50,
#     'pool_recycle': 1800,
#     'pool_timeout': 60,
#     'max_overflow': 100,
# }

# Create the extension
db = SQLAlchemy(model_class=Base)
# initialise the app with the extension
db.init_app(app)

# Create table product
class User(UserMixin, db.Model):
    # id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String, primary_key=True)
    password: Mapped[str] = mapped_column(String, nullable=True)
    surveys = db.relationship('Survey', backref='user', lazy=True, cascade="all, delete-orphan")

    def get_id(self):
        return self.user_name

class Product(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    surveys = db.relationship('Survey', backref='product', lazy=True, cascade="all, delete-orphan")

# Create table Survey
class Survey(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('product.id'), nullable=False)
    user_id: Mapped[str] = mapped_column(String, db.ForeignKey('user.user_name'), nullable=False)
    interested_lanched: Mapped[int] = mapped_column(Integer, nullable=False)
    path_to_market: Mapped[int] = mapped_column(Integer, nullable=False)
    pull_sales: Mapped[int] = mapped_column(Integer, nullable=False)
    comments: Mapped[str] = mapped_column(String, nullable=True)

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()

check_lock_login_user = False

# Main -----------------------------------------------------
@app.route('/')
def index():
    user_acount = db.session.execute(db.select(User)).scalars()
    if len(user_acount.all()) == 0:
        new_user_admin = User(user_name='admin', password=os.environ.get('ADMIN_PASSWORD'))
        db.session.add(new_user_admin)
        db.session.commit()
    
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_user_def'))
        else:
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")

    # user_completed_survey = db.session.execute(db.select(UserCompletedSurvey).where(UserCompletedSurvey.user_id == current_user.user_name)).scalars()
    user_get =  db.session.query(User).options(joinedload(User.surveys)).filter_by(user_name=current_user.user_name).first()
    user_completed_survey = [survey.product_id for survey in user_get.surveys]
    surveyed_count = len(user_completed_survey)
    
    all_products = db.session.execute(db.select(Product)).scalars()
    # all_products = result.scalars()
    product_list = list(all_products)

    product_list.sort(key=extract_number)

    return render_template('index.html', products=product_list, user_id=current_user.user_name, completed_surveys=user_completed_survey, surveyed=surveyed_count)

@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_user_def'))
        else:
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")

    query = request.args.get('query').lower()
    filtered_products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()

    product_list = list(filtered_products)

    product_list.sort(key=extract_number)

    user_get = db.session.query(User).options(joinedload(User.surveys)).filter_by(user_name=current_user.user_name).first()
    user_completed_survey = [survey.product_id for survey in user_get.surveys]
    surveyed_count = len(user_completed_survey)

    return render_template('search_results.html', user_id=current_user.user_name, surveyed=surveyed_count, products=product_list, query=query)

@app.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == "POST":
        input_user = request.form.get('inputUser')
        input_password = request.form.get('inputPassword')
        
        # result = db.session.execute(db.select(User).where(func.lower(User.user_name) == input_user.lower()))
        user = db.session.execute(db.select(User).where(func.lower(User.user_name) == input_user.lower())).scalar()
        # User name or password incorrect.
        if not user:
            flash("That user name incorrect, please try again.")
            return redirect(url_for('login_admin'))
        if user.user_name != 'admin':
            flash("That user name incorrect, please try again.")
            return redirect(url_for('login_admin'))
        elif not check_password_hash(user.password, input_password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login_admin'))
        else:
            login_user(user)
            return redirect(url_for('admin'))

    return render_template("login_admin.html")

@app.route('/login-admin/lock-unlock')
def lock_unlock():
    global check_lock_login_user
    if check_lock_login_user:
        check_lock_login_user = False
    else:
        check_lock_login_user = True
    return redirect(url_for('admin'))

@app.route('/login-user', methods=["GET", "POST"])
def login_user_def():
    try:
        if current_user.is_authenticated:
            if check_lock_login_user:
                if current_user.user_name == 'admin':
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('logout'))
            else:
                return redirect(url_for('index'))
        else:
            if check_lock_login_user:
                return redirect(url_for('login_admin'))
    except:
        return render_template("login_user.html")

    if request.method == "POST":
        l_user = request.form.get('inputUser')
        # result = db.session.execute(db.select(User).where(func.lower(User.user_name) == l_user.lower()))

        user = db.session.execute(db.select(User).where(func.lower(User.user_name) == l_user.lower())).scalar()
        # Email doesn't exist or password incorrect.
        if not user:
            new_user = User(
                user_name=l_user,
            )
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            # return redirect(url_for("index"))
        else:
            if user.user_name.lower() == 'admin':
                flash("That Username only for admin, please go to the admin page to log in if you are an admin.")
                return redirect(url_for('login_user_def'))
            
            login_user(user)

        return redirect(url_for('index'))

    return render_template("login_user.html")

@app.route('/register-user', methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        r_user = request.form.get('inputUser')
        # result = db.session.execute(db.select(User).where(func.lower(User.user_name) == r_user.lower()))
        
        # Note, email in db is unique so will only have one result.
        user = db.session.execute(db.select(User).where(func.lower(User.user_name) == r_user.lower())).scalar()
        if user:
            # User already exists
            flash("That Username already exist, Please register with another name!")
            return redirect(url_for('register_user'))

        if ' ' in r_user:
            flash("There must be no spaces in the username!")
            return redirect(url_for('register_user'))

        new_user = User(
            user_name=r_user,
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("index"))
    
    return render_template("register_user.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Survey ------------------------------------------------------
@app.route('/survey/<survey_id>', methods=['GET', 'POST'])
def survey(survey_id):
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_user_def'))
        else:
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
    
    # user_id = session.get('user_id')
    # survey = db.session.execute(db.select(Product).where(Product.id == survey_id)).scalar()
    survey = db.session.query(Product).filter_by(id=survey_id).first()
    # survey = surveys.get(survey_id)
    if not survey:
        return redirect(url_for('index'))
    
    user_get = db.session.query(User).options(joinedload(User.surveys)).filter_by(user_name=current_user.user_name).first()
    user_completed_survey = [survey.product_id for survey in user_get.surveys]
    surveyed_count = len(user_completed_survey)

    if request.method == 'POST':
        comment_ai = None
        interested_lanch = int(request.form['launched'])
        path_to_mar = int(request.form['pathmarket'])
        pull_sale = int(request.form['pullsales'])
        comment = request.form['comment']

        new_survey = Survey(product_id = survey_id, 
                            user_id = current_user.user_name, 
                            interested_lanched = interested_lanch, 
                            path_to_market = path_to_mar, 
                            pull_sales = pull_sale, 
                            comments = comment)
        db.session.add(new_survey)
        db.session.commit()

        socketio.emit('update_dashboard_charts')
        
        df_measure_survey = measure_survey()
        socketio.emit('update_measure_concepts', df_measure_survey)

        total_surveys = db.session.query(Survey).count()
        total_user = db.session.query(User).count()

        socketio.emit('update_total_user', total_user)
        socketio.emit('update_total_survey', total_surveys)

        return redirect(url_for('index'))
    
    return render_template('survey.html', survey=survey, user_id=current_user.user_name, surveyed=surveyed_count)

# ------------------------------------------------------
@app.route('/thank-you')
def thank_you():
    user_get = db.session.execute(db.select(User).where(User.user_name == current_user.user_name)).scalar()
    user_completed_survey = [survey.product_id for survey in user_get.surveys]
    surveyed_count = len(user_completed_survey)

    return render_template('thank_you.html', user_id=current_user.user_name, surveyed=surveyed_count)

def measure_survey():
    surveys = db.session.execute(db.select(Survey)).scalars()
    check_count = len(surveys.all())
    surveys = db.session.execute(db.select(Survey)).scalars()
    if check_count > 0:
        df = pd.DataFrame([{
            'product_name': survey.product.name,
            'interested_lanched': survey.interested_lanched,
            'path_to_market': survey.path_to_market,
            'pull_sales': survey.pull_sales
        } for survey in surveys])
        
        df_measure_survey = df.groupby('product_name').agg(
            Rating =('product_name', 'size'),
            WRating =('product_name', 'size'),
            Participation=('product_name', 'size'),
            Average_interested_lanched=('interested_lanched', 'mean'),
            Average_path_to_market=('path_to_market', 'mean'),
            Average_pull_sales=('pull_sales', 'mean'),
        ).reset_index()

        df_measure_survey['Rating'] = df_measure_survey[['Average_interested_lanched', 'Average_path_to_market', 'Average_pull_sales']].mean(axis=1)
        df_measure_survey['Rating'] = df_measure_survey['Rating'].round(2)
        df_measure_survey['Average_interested_lanched'] = df_measure_survey['Average_interested_lanched'].round(2)
        df_measure_survey['Average_path_to_market'] = df_measure_survey['Average_path_to_market'].round(2)
        df_measure_survey['Average_pull_sales'] = df_measure_survey['Average_pull_sales'].round(2)

        # Calculate the Weighted Rating column
        mean_rating = df_measure_survey['Rating'].mean()
        base_line = int(df_measure_survey['Participation'].mean())
        df_measure_survey['WRating'] = (df_measure_survey['Participation'] / (df_measure_survey['Participation'] + base_line)) * df_measure_survey['Rating'] + (base_line / (df_measure_survey['Participation'] + base_line)) * mean_rating
        df_measure_survey['WRating'] = df_measure_survey['WRating'].round(2)

        df_measure_survey = df_measure_survey.sort_values(by='Rating', ascending=False)
        return df_measure_survey.to_dict(orient='records')
    else:
        return pd.DataFrame()

# Admin web ------------------------------------------
@app.route('/admin')
def admin():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
    
    total_surveys = db.session.query(Survey).count()
    total_user = db.session.query(User).count()
    
    # print(df_measure_survey)
    return render_template('index_admin.html', total_surveys=total_surveys, total_user=total_user, check_lock = check_lock_login_user)

@app.route('/admin/generate_report')
def generate_report():
    # Query the database
    product_all = db.session.execute(db.select(Product)).scalars()
    survey_all = db.session.execute(db.select(Survey)).scalars()
    user_surveys = db.session.execute(db.select(User)).scalars()
    df_measure_survey = measure_survey()

    # Convert the queries to pandas DataFrames
    measure_df = pd.DataFrame(df_measure_survey)
    measure_df = measure_df.rename(columns={'product_name': 'Concept Name', 
                                            'WRating': 'Weighted Rating', 
                                            'Average_interested_lanched':'Average interested lanched',
                                            'Average_path_to_market': 'Average path to market',
                                            'Average_pull_sales': 'Average pull sales'})

    products_df = pd.DataFrame([{
        'ID': product.id, 
        'Concept Name': product.name, 
        'Description': product.description
    } for product in product_all])

    surveys_df = pd.DataFrame([{
        'ID': survey.id, 
        'Concept Name': survey.product.name, 
        'User Name': survey.user_id, 
        'Interested Lanched': survey.interested_lanched, 
        'Path to Market': survey.path_to_market, 
        'Pull Sales': survey.pull_sales, 
        'Comments': survey.comments
    } for survey in survey_all])

    users_df = pd.DataFrame([{
        'User Name': user.user_name,
        'Surveys': len(user.surveys),
    } for user in user_surveys])
    
    # Create an Excel file in memory with three sheets
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        measure_df.to_excel(writer, index=False, sheet_name='Measure Surveys')
        products_df.to_excel(writer, index=False, sheet_name='Concepts')
        surveys_df.to_excel(writer, index=False, sheet_name='Surveys')
        users_df.to_excel(writer, index=False, sheet_name='User Completed')
    
    output.seek(0)
    
    # Send the file to the client
    return send_file(output, download_name ='Surveys Report.xlsx', as_attachment=True)

def extract_number(product):
    match = re.search(r'\d+', product.name)
    return int(match.group()) if match else 0

@app.route('/admin/measure_concepts')
def measure_concepts_table():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
        
    df_measure_survey = measure_survey()

    total_surveys = db.session.query(Survey).count()
    total_user = db.session.query(User).count()

    return render_template('measure_concepts_admin.html', measure_survey = df_measure_survey, total_surveys=total_surveys, total_user=total_user, check_lock = check_lock_login_user)

# Product Table ------------------------------------------
@app.route('/admin/product')
def product_table():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
        
    product_all = db.session.execute(db.select(Product)).scalars()
    
    product_list = list(product_all)

    product_list.sort(key=extract_number)

    total_surveys = db.session.query(Survey).count()
    total_user = db.session.query(User).count()

    return render_template('product_admin.html', products = product_list, total_surveys=total_surveys, total_user=total_user, check_lock = check_lock_login_user)

# Add Product------------------------------------------
@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin')) 
        else:
            if current_user.user_name != 'admin':
                redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
        
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_product = Product(name=name, description=description)
        db.session.add(new_product)
        db.session.commit()

    return redirect(url_for('product_table'))

@app.route('/admin/edit_product', methods=['GET', 'POST'])
def edit_product():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
        
    if request.method == 'POST':
        product_id = request.form['id']
        product = db.session.execute(db.select(Product).where(Product.id == product_id)).scalar()
        product.name = request.form['name']
        product.description = request.form['description']
        db.session.commit()
        
    return redirect(url_for('product_table'))

@app.route('/admin/delete_product/<int:id>')
def delete_product(id):
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
    
    product = db.session.execute(db.select(Product).where(Product.id == id)).scalar()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product_table'))

@app.route('/admin/delete_all_product')
def delete_all_product():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
    
    product = db.session.execute(db.select(Product)).scalars()
    for survey in product:
        db.session.delete(survey)
    db.session.commit()
    return redirect(url_for('product_table'))

# survey Table ------------------------------------------
@app.route('/admin/survey')
def survey_table():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
    
    survey_all = db.session.execute(db.select(Survey)).scalars()
    
    total_surveys = db.session.query(Survey).count()
    total_user = db.session.query(User).count()

    return render_template('survey_admin.html', surveys = survey_all, total_surveys=total_surveys, total_user=total_user, check_lock = check_lock_login_user)

# survey Table ------------------------------------------
@app.route('/admin/user-completed-survey')
def user_completed_table():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
    
    user_completed_all = db.session.query(User).options(joinedload(User.surveys)).all()
    
    total_surveys = db.session.query(Survey).count()
    total_user = db.session.query(User).count()

    return render_template('user_completed_admin.html', user_completed = user_completed_all,  total_surveys=total_surveys, total_user=total_user, check_lock = check_lock_login_user)

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")
    
    if request.method == "POST":
        l_user = request.form.get('userName')
        user = db.session.execute(db.select(User).where(func.lower(User.user_name) == l_user.lower())).scalar()
        # Email doesn't exist or password incorrect.
        if not user:
            new_user = User(
                user_name=l_user,
            )
            db.session.add(new_user)
            db.session.commit()

    return redirect(url_for('user_completed_table'))

@app.route('/admin/edit_user', methods=['GET', 'POST'])
def edit_user():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")

    if request.method == 'POST':
        user_id = request.form['id']
        
        if user_id == 'admin':
            return redirect(url_for('user_completed_table'))

        new_user_name = request.form['name']

        new_user = db.session.execute(db.select(User).where(User.user_name == new_user_name)).scalar()
        user = db.session.execute(db.select(User).where(User.user_name == user_id)).scalar()

        if new_user:
            survey_ids = [{sur.id for sur in new_user.surveys}]

            for survey in user.surveys:
                if survey.id in survey_ids:
                    db.session.delete(survey)
                else:
                    survey.user_id = new_user_name
            db.session.commit()
            db.session.delete(user)
        else:
            for survey in user.surveys:
                survey.user_id = new_user_name
            db.session.commit()
            user.user_name = new_user_name

        db.session.commit()
        
    return redirect(url_for('user_completed_table'))

@app.route('/admin/delete_user/<username>')
def delete_user(username):
    try:
        if username == 'admin':
            user = db.session.execute(db.select(User).where(User.user_name == username)).scalar()
            for survey in user.surveys:
                db.session.delete(survey)
            db.session.commit()
            return redirect(url_for('user_completed_table'))
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                return redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")

    user = db.session.execute(db.select(User).where(User.user_name == username)).scalar()
    
    for survey in user.surveys:
        db.session.delete(survey)
    
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_completed_table'))

@app.route('/admin/delete_all_users')
def delete_all_users():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login_admin'))
        else:
            if current_user.user_name != 'admin':
                redirect(url_for('index'))
            if check_lock_login_user and current_user.user_name != 'admin':
                return redirect(url_for('logout'))
    except:
        return render_template("login_user.html")

    users = db.session.execute(db.select(User).where(User.user_name != 'admin')).scalars()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_completed_table'))

# Product Bizarre 2024 Rank Chart ------------------------------------------
@app.route('/admin/dashboard-charts')
def dashboard_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        #---------------------------
        df_rank_chart = sorted(df_measure_survey, key=lambda entry: entry['Rating'], reverse=True)
        # labels = df_measure_survey['product_name'].tolist()
        rank_chart_labels = [product['product_name'] for product in df_rank_chart]
        rank_chart_values = [round(product['Rating'], 2)  for product in df_rank_chart]

        #---------------------------
        df_weighted_rank_chart = sorted(df_measure_survey, key=lambda entry: entry['WRating'], reverse=True)
        weighted_rank_chart_labels = [product['product_name'] for product in df_weighted_rank_chart]
        weighted_rank_chart_values = [round(product['WRating'],2) for product in df_weighted_rank_chart]

        #---------------------------
        df_participation_chart = sorted(df_measure_survey, key=lambda entry: entry['Participation'], reverse=True)
        participation_chart_labels = [product['product_name'] for product in df_participation_chart]
        participation_chart_values = [round(product['Participation'],0) for product in df_participation_chart]

        #---------------------------
        df_interested_chart = sorted(df_measure_survey, key=lambda entry: entry['Average_interested_lanched'], reverse=True)
        interested_chart_labels = [product['product_name'] for product in df_interested_chart]
        interested_chart_values = [round(product['Average_interested_lanched'],2) for product in df_interested_chart]
        
        #---------------------------
        df_market_chart = sorted(df_measure_survey, key=lambda entry: entry['Average_path_to_market'], reverse=True)
        market_chart_labels = [product['product_name'] for product in df_market_chart]
        market_chart_values = [round(product['Average_path_to_market'],2) for product in df_market_chart]

        #---------------------------
        df_pull_chart = sorted(df_measure_survey, key=lambda entry: entry['Average_pull_sales'], reverse=True)
        pull_chart_labels = [product['product_name'] for product in df_pull_chart]
        pull_chart_values = [round(product['Average_pull_sales'],2) for product in df_pull_chart]

        data = {'rankchartlabels': rank_chart_labels[:10], 'rankchartvalues': rank_chart_values[:10],
                'weightedrankchartlabels': weighted_rank_chart_labels[:10], 'weightedrankchartvalues': weighted_rank_chart_values[:10],
                'participationchartlabels': participation_chart_labels[:10], 'participationchartvalues': participation_chart_values[:10],
                'interestedchartlabels': interested_chart_labels[:10], 'interestedchartvalues': interested_chart_values[:10],
                'marketchartlabels': market_chart_labels[:10], 'marketchartvalues': market_chart_values[:10],
                'pullchartlabels': pull_chart_labels[:10], 'pullchartvalues': pull_chart_values[:10],
                }
    else:
       data = {'rankchartlabels': [], 'rankchartvalues': [],
                'weightedrankchartlabels': [], 'weightedrankchartvalues': [],
                'participationchartlabels': [], 'participationchartvalues': [],
                'interestedchartlabels': [], 'interestedchartvalues': [],
                'marketchartlabels': [], 'marketchartvalues': [],
                'pullchartlabels': [], 'pullchartvalues': [],
                }
    
    return jsonify(data)

@app.route('/admin/rank-chart')
def rank_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['Rating'], reverse=True)
        # labels = df_measure_survey['product_name'].tolist()
        labels = [product['product_name'] for product in df_measure_survey]
        values = [round(product['Rating'], 2)  for product in df_measure_survey]
    
        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

@app.route('/admin/weighted-rank-chart')
def weighted_rank_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['WRating'], reverse=True)
        # labels = df_measure_survey['product_name'].tolist()
        labels = [product['product_name'] for product in df_measure_survey]
        values = [round(product['WRating'],2) for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Product Bizarre 2024 Participation Chart ------------------------------------------
@app.route('/admin/participation-chart')
def participation_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['Participation'], reverse=True)
        labels = [product['product_name'] for product in df_measure_survey]
        values = [round(product['Participation'],0) for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Product Bizarre 2024 interested lanched Chart ------------------------------------------
@app.route('/admin/interested-lanched-chart')
def interested_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['Average_interested_lanched'], reverse=True)
        labels = [product['product_name'] for product in df_measure_survey]
        values = [round(product['Average_interested_lanched'],2) for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Product Bizarre 2024 path to market Chart ------------------------------------------
@app.route('/admin/path-to-market-chart')
def market_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['Average_path_to_market'], reverse=True)
        labels = [product['product_name'] for product in df_measure_survey]
        values = [round(product['Average_path_to_market'],2) for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Product Bizarre 2024 pull sale Chart ------------------------------------------
@app.route('/admin/pull-sales-chart')
def pull_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['Average_pull_sales'], reverse=True)
        labels = [product['product_name'] for product in df_measure_survey]
        values = [round(product['Average_pull_sales'],2) for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Main python ------------------------------------------------------
if __name__ == '__main__':
    # app.run(debug=False, port=5001)
    socketio.run(app, debug=False, port=5001)
