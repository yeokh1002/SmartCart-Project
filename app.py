from flask import Flask, request, render_template
import pandas as pd
import random
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
# load files===========================================================================================================
trending_products = pd.read_csv("models/trending_products.csv")
train_data = pd.read_csv("models/cleaned_data3.csv")
# database configuration---------------------------------------
app.secret_key = "SecretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/ecom"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Content-based recommendation model from previous research
def content_based_recommendations(train_data, item_name, top_n=10):
    if item_name not in train_data['Name'].values:
        print(f"Item '{item_name}' not found in the training data.")
        return pd.DataFrame()
    train_data['Tags'] = train_data['Tags'].fillna('')
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)
    item_index = train_data[train_data['Name'] == item_name].index[0]
    similar_items = list(enumerate(cosine_similarities_content[item_index]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[1:top_n + 1]  # Excludes index 0 (input item)
    recommended_item_indices = [x[0] for x in top_similar_items]
    recommended_items_details = train_data.iloc[recommended_item_indices][
        ['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating', 'Product Price']]
    recommended_items_details = recommended_items_details[
        recommended_items_details['Name'] != item_name]  # Redundant but safe
    recommended_items_details = recommended_items_details.sort_values(by=['Rating', 'ReviewCount'],
                                                                      ascending=[False, False])
    return recommended_items_details



# define model class for signup table
class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define your model class for the 'signup' table
class Signin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

random_image_urls = [
    "static/img/img1.jfif",
    "static/img/img2.jfif",
    "static/img/img3.webp",
    "static/img/img4.jpg",
    "static/img/img5.webp",
    "static/img/img6.jpg",
    "static/img/img7.jpg",
    "static/img/img8.jfif",
]
def truncate(text, length=20):
    if len(text) > length:
        return text[:length] + "..."
    else:
        return text

@app.route("/")
def index():
    # Create a list of random image URLs for each product
    random_product_image_urls = random_image_urls
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html',trending_products=trending_products.head(8),
                           truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price = random.choice(price))

@app.route("/main")
def main():
    return render_template('main.html',
                         content_based_rec=pd.DataFrame(),
                         message="Search for products to get recommendations")
# routes
@app.route("/index")
def indexredirect():
    # Create a list of random image URLs for each product
    random_product_image_urls = random_image_urls
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price=random.choice(price))

@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_signup = Signup(username=username, email=email, password=password)
        db.session.add(new_signup)
        db.session.commit()

        # Create a list of random image URLs for each product
        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
        return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                               random_product_image_urls=random_product_image_urls, random_price=random.choice(price),
                               signup_message='User signed up successfully!'
                               )

# Route for signup page
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['signinUsername']
        password = request.form['signinPassword']
        new_signup = Signin(username=username,password=password)
        db.session.add(new_signup)
        db.session.commit()

        # Create a list of random image URLs for each product
        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
        return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                               random_product_image_urls=random_product_image_urls, random_price=random.choice(price),
                               signup_message='User signed in successfully!'
                               )


@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    content_based_rec = pd.DataFrame()  # Initialize empty DataFrame

    if request.method == 'POST':
        prod = request.form.get('prod')
        nbr = int(request.form.get('nbr'))
        content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)

        debug_info = {
            'is_none': content_based_rec is None,
            'is_empty': content_based_rec.empty,
            'shape': content_based_rec.shape if not content_based_rec.empty else (0, 0),
            'columns': list(content_based_rec.columns) if not content_based_rec.empty else []
        }

        price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
        random_product_image_urls = [random.choice(random_image_urls) for _ in
                                     range(len(content_based_rec) if not content_based_rec.empty else 0)]

        return render_template('main.html',
                               content_based_rec=content_based_rec,
                               truncate=truncate,
                               random_product_image_urls=random_product_image_urls,
                               random_price=random.choice(price),
                               debug_info=debug_info,
                               message="No recommendations available" if content_based_rec.empty else None)

    # Handle GET requests
    return render_template('main.html',
                           content_based_rec=pd.DataFrame(),
                           message="Search for products to get recommendations")
if __name__ == '__main__':
    app.run(debug=True)

