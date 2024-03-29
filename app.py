# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask app
app = Flask(__name__)

#Use flask_pymongo to set up Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


#Route to render index.html template using data from Mongo
@app.route("/")
def home(): 

    # Find data
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrape functions
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__": 
    app.run(debug= True)