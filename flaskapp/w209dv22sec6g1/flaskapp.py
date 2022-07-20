from flask import Flask, render_template

# Import everyones work!
from blueprints.Margo_Suryanaga import Margo_Suryanaga 
from blueprints.Rishika_Pulvender import Rishika_Pulvender
from blueprints.Cody_Burker import Cody_Burker
from blueprints.John_Mah import John_Mah

app = Flask(__name__)
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
    file="about9.jpg"
    return render_template('flavorprofiles.html', file=file)


@app.route("/nutrition")
def nutrition():
    file="about9.jpg"
    return render_template('nutrition.html', file=file)

@app.route("/ingredients")
def ingredients():
    file="about9.jpg"
    return render_template('ingredients.html', file=file)


if __name__ == "__main__":
    app.run()