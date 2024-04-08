from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, func
import random
import pandas as pd
import os
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, Length  # pip install email-validator
# from flask_bootstrap import Bootstrap5  # pip install bootstrap-flask

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')
test =  os.environ.get('FLASK_KEY')
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
    id: Mapped[str] = mapped_column(String(250), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

# Create table Survey
class Survey(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String, ForeignKey('product.name'),nullable=False)
    user_id: Mapped[str] = mapped_column(String(6), ForeignKey('product.id'), nullable=False)
    interested_lanched: Mapped[int] = mapped_column(Integer, nullable=False)
    path_to_market: Mapped[int] = mapped_column(Integer, nullable=False)
    pull_sales: Mapped[int] = mapped_column(Integer, nullable=False)
    comments: Mapped[str] = mapped_column(String, nullable=False)

#Create table user
class UserCompletedSurvey(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(6), nullable=False)
    product_id: Mapped[str] = mapped_column(String(250), ForeignKey('product.id'), nullable=False)


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()

def generate_unique_user_id():
    while True:
        user_id = ''.join(random.choices(['0','1','2','3','4','5','6','7','8','9'], k=6))
        if user_id not in session.values():  # kiểm tra xem mã ID đã tồn tại trong session hay chưa
            return user_id

# Main ------------------------------------------------------
@app.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        user_id = generate_unique_user_id()
        session['user_id'] = user_id

    user_completed_survey = db.session.execute(db.select(UserCompletedSurvey).where(UserCompletedSurvey.user_id == user_id)).scalars()

    user_completed_survey = [survey.product_id for survey in user_completed_survey]
    surveyed_product = len(user_completed_survey)
    result = db.session.execute(db.select(Product))

    if len(result.all()) == 0:
        new_product_a = Product(id="product_a", name="Product A", description="Description for Product A")
        new_product_b = Product(id="product_b", name="Product B", description="Description for Product B")
        new_product_c = Product(id="product_c", name="Product C", description="Description for Product C")
        new_product_d = Product(id="product_d", name="Product D", description="Description for Product D")
        new_product_e = Product(id="product_e", name="Product E", description="Description for Product E")
        new_product_f = Product(id="product_f", name="Product F", description="Description for Product F")
        new_product_g = Product(id="product_g", name="Product G", description="Description for Product G")
        new_product_h = Product(id="product_h", name="Product H", description="Description for Product H")
        new_product_i = Product(id="product_i", name="Product I", description="Description for Product I")
        new_product_j = Product(id="product_j", name="Product J", description="Description for Product J")
        new_product_k = Product(id="product_k", name="Product K", description="Description for Product K")
        new_product_l = Product(id="product_l", name="Product L", description="Description for Product L")
        new_product_m = Product(id="product_m", name="Product M", description="Description for Product M")
        new_product_o = Product(id="product_o", name="Product O", description="Description for Product O")
        new_product_p = Product(id="product_p", name="Product P", description="Description for Product P")
        new_product_q = Product(id="product_q", name="Product Q", description="Description for Product Q")
        new_product_z = Product(id="product_z", name="Product Z", description="Description for Product Z")

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

    return render_template('index.html', products=all_products, user_id=user_id, completed_surveys=user_completed_survey, surveyed=surveyed_product)

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
        new_completed_survey = UserCompletedSurvey(user_id=user_id, product_id=survey_id)
        db.session.add(new_completed_survey)
        db.session.commit()

        interested_lanch = int(request.form['launched'])
        path_to_mar = int(request.form['pathmarket'])
        pull_sale = int(request.form['pullsales'])
        comment = request.form['comment']
        new_survey = Survey(product_name=survey.name, user_id=user_id, interested_lanched=interested_lanch, path_to_market=path_to_mar, pull_sales=pull_sale, comments=comment)
        db.session.add(new_survey)
        db.session.commit()

        return redirect(url_for('thank_you'))
    
    return render_template('survey.html', survey=survey, user_id=user_id, surveyed=surveyed_product)

# ------------------------------------------------------
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

# Admin web ------------------------------------------
@app.route('/admin')
def admin():
    surveys = db.session.execute(db.select(Survey)).scalars()

    if len(surveys.all()) > 0:
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
        df_measure_survey = df_measure_survey.to_dict(orient='records')
    else:
        df_measure_survey = pd.DataFrame()

    total_surveys = df_measure_survey.shape[0]

    user_surveys = db.session.execute(db.select(UserCompletedSurvey)).scalars()
    total_user = len(user_surveys.all())

    # print(df_measure_survey)
    return render_template('index_admin.html', measure_survey = df_measure_survey, total_surveys=total_surveys, total_user=total_user)


# Product Table ------------------------------------------
@app.route('/admin/product')
def product_table():
    product_all = db.session.execute(db.select(Product)).scalars()
    
    return render_template('product_admin.html', products = product_all)

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

# Main python ------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=False, port=5001)
