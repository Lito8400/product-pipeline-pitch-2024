from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, g, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, func
from werkzeug.security import generate_password_hash, check_password_hash
# from openai import OpenAI

import random
import pandas as pd
import os
import io

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_name):
    return db.get_or_404(User, user_name)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///serveys.db")

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

#Create table user
# class UserCompletedSurvey(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[str] = mapped_column(String, nullable=False)
#     product_id: Mapped[str] = mapped_column(String, nullable=False)
#     product_Name: Mapped[str] = mapped_column(String, nullable=False)

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

    if not current_user.is_authenticated:
        return redirect(url_for('login_user_def'))
    else:
        if check_lock_login_user and current_user.user_name != 'admin':
            return redirect(url_for('logout'))

    # user_completed_survey = db.session.execute(db.select(UserCompletedSurvey).where(UserCompletedSurvey.user_id == current_user.user_name)).scalars()
    user_get = db.session.execute(db.select(User).where(User.user_name == current_user.user_name)).scalar()
    user_completed_survey = [survey.product_id for survey in user_get.surveys]
    surveyed_count = len(user_completed_survey)
    
    # result = db.session.execute(db.select(Product)).all()
    # if len(result) == 0:
    #     new_product_1 = Product( name="Concept 1", description="Concept 1 name")
    #     new_product_2 = Product( name="Concept 2", description="Concept 2 name")
    #     new_product_3 = Product( name="Concept 3", description="Concept 3 name")
    #     new_product_4 = Product( name="Concept 4", description="Concept 4 name")
    #     new_product_5 = Product( name="Concept 5", description="Concept 5 name")
    #     new_product_6 = Product( name="Concept 6", description="Concept 6 name")
    #     new_product_7 = Product( name="Concept 7", description="Concept 7 name")
    #     new_product_8 = Product( name="Concept 8", description="Concept 8 name")
    #     new_product_9 = Product( name="Concept 9", description="Concept 9 name")
    #     new_product_10 = Product( name="Concept 10", description="Concept 10 name")
    #     new_product_11 = Product( name="Concept 11", description="Concept 11 name")
    #     new_product_12 = Product( name="Concept 12", description="Concept 12 name")
    #     new_product_13 = Product( name="Concept 13", description="Concept 13 name")
    #     new_product_14 = Product( name="Concept 14", description="Concept 14 name")
    #     new_product_15 = Product( name="Concept 15", description="Concept 15 name")
    #     new_product_16 = Product( name="Concept 16", description="Concept 16 name")
    #     new_product_17 = Product( name="Concept 17", description="Concept 17 name")
    #     new_product_18 = Product( name="Concept 18", description="Concept 18 name")
    #     new_product_19 = Product( name="Concept 19", description="Concept 19 name")
    #     new_product_20 = Product( name="Concept 20", description="Concept 20 name")

    #     db.session.add(new_product_1)
    #     db.session.add(new_product_2)
    #     db.session.add(new_product_3)
    #     db.session.add(new_product_4)
    #     db.session.add(new_product_5)
    #     db.session.add(new_product_6)
    #     db.session.add(new_product_7)
    #     db.session.add(new_product_8)
    #     db.session.add(new_product_9)
    #     db.session.add(new_product_10)
    #     db.session.add(new_product_11)
    #     db.session.add(new_product_12)
    #     db.session.add(new_product_13)
    #     db.session.add(new_product_14)
    #     db.session.add(new_product_15)
    #     db.session.add(new_product_16)
    #     db.session.add(new_product_17)
    #     db.session.add(new_product_18)
    #     db.session.add(new_product_19)
    #     db.session.add(new_product_20)
    #     db.session.commit()

    all_products = db.session.execute(db.select(Product)).scalars()
    # all_products = result.scalars()

    return render_template('index.html', products=all_products, user_id=current_user.user_name, completed_surveys=user_completed_survey, surveyed=surveyed_count)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not current_user.is_authenticated:
        return redirect(url_for('login_user_def'))
    else:
        if check_lock_login_user and current_user.user_name != 'admin':
            return redirect(url_for('logout'))

    query = request.args.get('query').lower()
    filtered_products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()

    user_get = db.session.execute(db.select(User).where(User.user_name == current_user.user_name)).scalar()
    user_completed_survey = [survey.product_id for survey in user_get.surveys]
    surveyed_count = len(user_completed_survey)

    return render_template('search_results.html', user_id=current_user.user_name, surveyed=surveyed_count, products=filtered_products, query=query)

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
    if check_lock_login_user:
        return redirect(url_for('login_admin'))

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
    if not current_user.is_authenticated:
        return redirect(url_for('login_user_def'))
    else:
        if check_lock_login_user and current_user.user_name != 'admin':
            return redirect(url_for('logout'))
        
    # user_id = session.get('user_id')
    # survey = db.session.execute(db.select(Product).where(Product.id == survey_id)).scalar()
    survey = db.session.execute(db.select(Product).where(Product.id == survey_id)).scalar()
    # survey = surveys.get(survey_id)
    if not survey:
        return redirect(url_for('index'))
    
    user_get = db.session.execute(db.select(User).where(User.user_name == current_user.user_name)).scalar()
    user_completed_survey = [survey.product_id for survey in user_get.surveys]
    surveyed_count = len(user_completed_survey)

    if request.method == 'POST':
        comment_ai = None
        interested_lanch = int(request.form['launched'])
        path_to_mar = int(request.form['pathmarket'])
        pull_sale = int(request.form['pullsales'])
        comment = request.form['comment']

        new_survey = Survey(product_id=survey_id, user_id=current_user.user_name, interested_lanched=interested_lanch, path_to_market=path_to_mar, pull_sales=pull_sale, comments=comment)
        db.session.add(new_survey)
        db.session.commit()

        # if comment == '':
        #     prompt = f"Given the ratings: 'How interested are you in having this product launched?': {interested_lanch}, 'The path to market for this product concept established?': {path_to_mar}, 'Do you feel this product will “pull” sales of other products along?': {pull_sale}, generate a short comment."
        #     response = client.chat.completions.create(
        #         model="gpt-3.5-turbo",
        #         messages=[
        #             {"role": "user", "content": prompt},
        #         ]
        #     )
        #     comment_ai = response.choices[0].text.strip()

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
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))
    
    df_measure_survey = measure_survey()
    total_surveys = len(df_measure_survey)
    total_user = 0
    user_surveys = db.session.execute(db.select(User)).all()
    total_user = len(user_surveys)
   
    # print(df_measure_survey)
    return render_template('index_admin.html', measure_survey = df_measure_survey, total_surveys=total_surveys, total_user=total_user, check_lock = check_lock_login_user)

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
        'Name': product.name, 
        'Description': product.description
    } for product in product_all])

    surveys_df = pd.DataFrame([{
        'ID': survey.id, 
        'Concept Name': survey.product.name, 
        'User ID': survey.user_id, 
        'Interested Lanched': survey.interested_lanched, 
        'Path to Market': survey.path_to_market, 
        'Pull Sales': survey.pull_sales, 
        'Comments': survey.comments
    } for survey in survey_all])

    users_df = pd.DataFrame([{
        'User ID': user.user_name,
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

# Product Table ------------------------------------------
@app.route('/admin/product')
def product_table():
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))
    
    product_all = db.session.execute(db.select(Product)).scalars()
    
    return render_template('product_admin.html', products = product_all)

# Add Product------------------------------------------
@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin')) 
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_product = Product(name=name, description=description)
        db.session.add(new_product)
        db.session.commit()

    return redirect(url_for('product_table'))

@app.route('/admin/edit_product', methods=['GET', 'POST'])
def edit_product():
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))
    
    if request.method == 'POST':
        product_id = request.form['id']
        product = db.session.execute(db.select(Product).where(Product.id == product_id)).scalar()
        product.name = request.form['name']
        product.description = request.form['description']
        db.session.commit()
        
    return redirect(url_for('product_table'))

@app.route('/admin/delete_product/<int:id>')
def delete_product(id):
    product = db.session.execute(db.select(Product).where(Product.id == id)).scalar()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product_table'))

@app.route('/admin/delete_all_product')
def delete_all_product():
    product = db.session.execute(db.select(Product)).scalars()
    for survey in product:
        db.session.delete(survey)
    db.session.commit()
    return redirect(url_for('product_table'))

# survey Table ------------------------------------------
@app.route('/admin/survey')
def survey_table():
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))

    survey_all = db.session.execute(db.select(Survey)).scalars()
    
    return render_template('survey_admin.html', surveys = survey_all)

# survey Table ------------------------------------------
@app.route('/admin/user-completed-survey')
def user_completed_table():
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))

    user_completed_all = db.session.execute(db.select(User)).scalars()
    
    return render_template('user_completed_admin.html', user_completed = user_completed_all)

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin')) 
    
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
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))
    
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
    if username == 'admin':
        return redirect(url_for('user_completed_table'))

    user = db.session.execute(db.select(User).where(User.user_name == username)).scalar()
    for survey in user.surveys:
        db.session.delete(survey)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_completed_table'))

@app.route('/admin/delete_all_users')
def delete_all_users():
    users = db.session.execute(db.select(User).where(User.user_name != 'admin')).scalars()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_completed_table'))

# Product Bizarre 2024 Rank Chart ------------------------------------------
@app.route('/admin/rank-chart')
def rank_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['Rating'], reverse=True)
        # labels = df_measure_survey['product_name'].tolist()
        labels = [product['product_name'] for product in df_measure_survey]
        values = [product['Rating'] for product in df_measure_survey]

        data = {'labels': labels[:25], 'values': values[:25]}
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
        values = [product['WRating'] for product in df_measure_survey]

        data = {'labels': labels[:25], 'values': values[:25]}
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
        values = [product['Participation'] for product in df_measure_survey]

        data = {'labels': labels[:25], 'values': values[:25]}
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
        values = [product['Average_interested_lanched'] for product in df_measure_survey]

        data = {'labels': labels[:25], 'values': values[:25]}
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
        values = [product['Average_path_to_market'] for product in df_measure_survey]

        data = {'labels': labels[:25], 'values': values[:25]}
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
        values = [product['Average_pull_sales'] for product in df_measure_survey]

        data = {'labels': labels[:25], 'values': values[:25]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Main python ------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=False, port=5001)
