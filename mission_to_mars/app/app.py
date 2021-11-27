# import Flask, pymongo, and scrape_mars (your python file)

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Instantiate a Flask app

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_scrape_app"
mongo = PyMongo(app)

# Create a base '/' route that will query your mongodb database and render the `index.html` template

@app.route("/")
def index():
    mars_collection = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_collection)


# Create a '/scrape' route that will create the mars collection, run your scrape() function from scrape_mars, and update the mars collection in the database
# The route should redirect back to the base route '/' with a code 302.

@app.route("/scrape")
def scrape():
    mars1 = scrape_mars.scrape()
    mongo.db.collection.update({}, mars1, upsert=True)
    return redirect ("/", 302)


# Run your app

if __name__ == "__main__":
    app.run(debug=True)