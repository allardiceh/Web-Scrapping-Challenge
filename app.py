
import pymongo
import scrape_mars

from flask import Flask, render_template, redirect

#build the mongo database 
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route("/")
def home():
    mars = db.mars_facts.find_one()
    return render_template("index.html", mars = mars)



@app.route('/scrape')
def scrape():
   # db.collection.remove()
    mars=db.mars_facts
    mars_data= scrape_mars.scrape_info()
    mars.update({}, mars_data, upsert=True)
    
    return redirect('/')
    
    
   





if __name__ == "__main__":
    app.run(debug=True)




