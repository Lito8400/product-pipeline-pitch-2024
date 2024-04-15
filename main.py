from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, func
from werkzeug.security import generate_password_hash, check_password_hash
# from openai import OpenAI

import random
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')

class User(UserMixin):
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
    def get_id(self):
        return self.username

app.config['USER'] = User('admin', os.environ.get('ADMIN_PASSWORD'))
# app.config['USER'] = User(os.environ.get('USER_NAME'), os.environ.get('PASSWORD'))

login_manager = LoginManager()
login_manager.init_app(app)

# Thiết lập g.user trước mỗi request
@app.before_request
def before_request():
    g.user = app.config['USER']

@login_manager.user_loader
def load_user(user_id):
    return g.user

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///serveys.db")

# Create the extension
db = SQLAlchemy(model_class=Base)
# initialise the app with the extension
db.init_app(app)

# Create table product
class Product(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

# Create table Survey
class Survey(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String,nullable=False)
    user_id: Mapped[str] = mapped_column(String(6), nullable=False)
    interested_lanched: Mapped[int] = mapped_column(Integer, nullable=False)
    path_to_market: Mapped[int] = mapped_column(Integer, nullable=False)
    pull_sales: Mapped[int] = mapped_column(Integer, nullable=False)
    comments: Mapped[str] = mapped_column(String, nullable=True)

#Create table user
class UserCompletedSurvey(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(6), nullable=False)
    product_id: Mapped[str] = mapped_column(String(250), nullable=False)
    product_Name: Mapped[str] = mapped_column(String(250), nullable=False)


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()

def generate_unique_user_id():
    while True:
        user_id = ''.join(random.choices(['0','1','2','3','4','5','6','7','8','9'], k=6))
        if user_id not in session.values(): 
            return user_id

# Main -----------------------------------------------------
@app.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        user_id = generate_unique_user_id()
        session['user_id'] = user_id

    user_completed_survey = db.session.execute(db.select(UserCompletedSurvey).where(UserCompletedSurvey.user_id == user_id)).scalars()

    user_completed_survey = [int(survey.product_id) for survey in user_completed_survey]
    surveyed_product = len(user_completed_survey)
    result = db.session.execute(db.select(Product))

    if len(result.all()) == 0:
        new_product_a = Product( name="Product A", description="Description for Product A")
        new_product_b = Product( name="Product B", description="Description for Product B")
        new_product_c = Product( name="Product C", description="Description for Product C")
        new_product_d = Product( name="Product D", description="Description for Product D")
        new_product_e = Product( name="Product E", description="Description for Product E")
        new_product_f = Product( name="Product F", description="Description for Product F")
        new_product_g = Product( name="Product G", description="Description for Product G")
        new_product_h = Product( name="Product H", description="Description for Product H")
        new_product_i = Product( name="Product I", description="Description for Product I")
        new_product_j = Product( name="Product J", description="Description for Product J")
        new_product_k = Product( name="Product K", description="Description for Product K")
        new_product_l = Product( name="Product L", description="Description for Product L")
        new_product_m = Product( name="Product M", description="Description for Product M")
        new_product_o = Product( name="Product O", description="Description for Product O")
        new_product_p = Product( name="Product P", description="Description for Product P")
        new_product_q = Product( name="Product Q", description="Description for Product Q")
        new_product_z = Product( name="Product Z", description="Description for Product Z")

        db.session.add(new_product_a)
        db.session.add(new_product_b)
        db.session.add(new_product_c)
        db.session.add(new_product_d)
        db.session.add(new_product_e)
        db.session.add(new_product_f)
        db.session.add(new_product_g)
        db.session.add(new_product_h)
        db.session.add(new_product_i)
        db.session.add(new_product_j)
        db.session.add(new_product_k)
        db.session.add(new_product_l)
        db.session.add(new_product_m)
        db.session.add(new_product_o)
        db.session.add(new_product_p)
        db.session.add(new_product_q)
        db.session.add(new_product_z)
        db.session.commit()

    result = db.session.execute(db.select(Product))
    all_products = result.scalars()

    return render_template('index.html', products=all_products, user_id=user_id, completed_surveys=user_completed_survey, surveyed=surveyed_product, logged_in=current_user.is_authenticated)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query').lower()
    filtered_products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()

    return render_template('search_results.html', products=filtered_products, query=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        input_user = request.form.get('inputUser')
        input_password = request.form.get('inputPassword')
        user = g.user

        # User name or password incorrect.
        if user.username != input_user:
            flash("That user name incorrect, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password_hash, input_password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('admin'))

    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    return render_template("login_admin.html", logged_in=current_user.is_authenticated)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Survey ------------------------------------------------------
@app.route('/survey/<survey_id>', methods=['GET', 'POST'])
def survey(survey_id):
    user_id = session.get('user_id')
    survey = db.session.execute(db.select(Product).where(Product.id == survey_id)).scalar()
    # survey = surveys.get(survey_id)
    if not survey:
        return redirect(url_for('index'))
    
    user_completed_survey = db.session.execute(db.select(UserCompletedSurvey).where(UserCompletedSurvey.user_id == user_id)).scalars()

    user_completed_survey = [survey.product_id for survey in user_completed_survey]
    surveyed_product = len(user_completed_survey)

    if request.method == 'POST':
        comment_ai = None
        new_completed_survey = UserCompletedSurvey(user_id=user_id, product_Name=survey.name, product_id=survey_id)
        db.session.add(new_completed_survey)
        db.session.commit()

        interested_lanch = int(request.form['launched'])
        path_to_mar = int(request.form['pathmarket'])
        pull_sale = int(request.form['pullsales'])
        comment = request.form['comment']
        new_survey = Survey(product_name=survey.name, user_id=user_id, interested_lanched=interested_lanch, path_to_market=path_to_mar, pull_sales=pull_sale, comments=comment)
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

        return redirect(url_for('thank_you'))
    
    return render_template('survey.html', survey=survey, user_id=user_id, surveyed=surveyed_product)

# ------------------------------------------------------
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

def measure_survey():
    surveys = db.session.execute(db.select(Survey)).scalars()
    check_count = len(surveys.all())
    surveys = db.session.execute(db.select(Survey)).scalars()
    if check_count > 0:
        df = pd.DataFrame([{
            'product_name': survey.product_name,
            'interested_lanched': survey.interested_lanched,
            'path_to_market': survey.path_to_market,
            'pull_sales': survey.pull_sales
        } for survey in surveys])
        
        df_measure_survey = df.groupby('product_name').agg(
            Rating =('product_name', 'size'),
            Participation=('product_name', 'size'),
            Average_interested_lanched=('interested_lanched', 'mean'),
            Average_path_to_market=('path_to_market', 'mean'),
            Average_pull_sales=('pull_sales', 'mean'),
        ).reset_index()

        df_measure_survey['Rating'] = df_measure_survey[['Average_interested_lanched', 'Average_path_to_market', 'Average_pull_sales']].mean(axis=1)
        df_measure_survey['Rating'] = df_measure_survey['Rating'].round(2)
        df_measure_survey = df_measure_survey.sort_values(by='Rating', ascending=False)
        return df_measure_survey.to_dict(orient='records')
    else:
        return pd.DataFrame()

# Admin web ------------------------------------------
@app.route('/admin')
def admin():
    
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    df_measure_survey = measure_survey()
    total_surveys = len(df_measure_survey)

    user_surveys = db.session.execute(db.select(UserCompletedSurvey)).scalars()
    df = pd.DataFrame([{
            'user_id': survey.user_id,
        } for survey in user_surveys])
    grouped_df = df.groupby('user_id').size().reset_index(name='num_surveys')
    total_user = grouped_df['user_id'].nunique()

    # print(df_measure_survey)
    return render_template('index_admin.html', measure_survey = df_measure_survey, total_surveys=total_surveys, total_user=total_user)


# Product Table ------------------------------------------
@app.route('/admin/product')
def product_table():
    product_all = db.session.execute(db.select(Product)).scalars()
    
    return render_template('product_admin.html', products = product_all)

# Add Product------------------------------------------
@app.route('/admin/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_product = Product(name=name, description=description)
        db.session.add(new_product)
        db.session.commit()

    return redirect(url_for('product_table'))

@app.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = db.session.execute(db.select(Product).where(Product.id == product_id)).scalar()
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        db.session.commit()
        
    return redirect(url_for('product_table'))


# survey Table ------------------------------------------
@app.route('/admin/survey')
def survey_table():
    survey_all = db.session.execute(db.select(Survey)).scalars()
    
    return render_template('survey_admin.html', surveys = survey_all)

# survey Table ------------------------------------------
@app.route('/admin/user-completed-survey')
def user_completed_table():
    user_completed_all = db.session.execute(db.select(UserCompletedSurvey)).scalars()
    
    return render_template('user_completed_admin.html', user_completed = user_completed_all)

# Product Bizarre 2024 Rank Chart ------------------------------------------
@app.route('/admin/rank-chart')
def rank_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        # labels = df_measure_survey['product_name'].tolist()
        labels = [product['product_name'] for product in df_measure_survey]
        values = [product['Rating'] for product in df_measure_survey]

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
        values = [product['Participation'] for product in df_measure_survey]

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
        values = [product['Average_interested_lanched'] for product in df_measure_survey]

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
        values = [product['Average_path_to_market'] for product in df_measure_survey]

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
        values = [product['Average_pull_sales'] for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Main python ------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=False, port=5001)
