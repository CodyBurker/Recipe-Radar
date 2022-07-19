# General imports
from flask import Flask, render_template

# Import everyones work!
from Robert_Turnage import Robert_Turnage
from Margo_Suryanaga import Margo_Suryanaga 
from Rishika_Pulvender import Rishika_Pulvender
from Cody_Burker import Cody_Burker
from John_Mah import John_Mah

app = Flask(__name__)
app.register_blueprint(Robert_Turnage)
app.register_blueprint(Margo_Suryanaga)
app.register_blueprint(Rishika_Pulvender)
app.register_blueprint(Cody_Burker)
app.register_blueprint(John_Mah)

##########################
# Flask routes
##########################
# render index.html home page
@app.route("/")
def index():
    file="about9.jpg"
    return render_template('index.html', file=file)


@app.route("/flavorprofiles")
def flavor():
    return render_template('flavorprofiles.html')


@app.route("/nutrition")
def nutrition():
    return render_template('nutrition.html')


@app.route("/ingredients")
def ingredients():
    return render_template('ingredients.html')
   

if __name__ == "__main__":
    app.run()