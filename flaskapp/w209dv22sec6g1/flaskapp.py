from flask import Flask, render_template

# Import everyones work!
from blueprints.Robert_Turnage import Robert_Turnage 
from blueprints.Margo_Suryanaga import Margo_Suryanaga
from blueprints.Rishika_Pulvender import Rishika_Pulvender
#from blueprints.Cody_Burker import Cody_Burker
from blueprints.John_Mah import John_Mah

app = Flask(__name__)
app.register_blueprint(Robert_Turnage)
app.register_blueprint(Margo_Suryanaga)
app.register_blueprint(Rishika_Pulvender)
#app.register_blueprint(Cody_Burker)
app.register_blueprint(John_Mah)


##########################
# Flask routes
##########################
# render index.html home page
@app.route("/")
def view_about():
    return render_template("index.html", title="About")

@app.route("/flavorprofiles")
def view_flavor_profiles_page():
    return render_template("flavorprofiles.html", title="Flavor Profiles")

@app.route("/nutrition")
def view_nutrition_page():
    return render_template("nutrition.html", title="Nutrition")

@app.route("/ingredients")
def view_ingredients_page():
    return render_template("ingredients.html", title="Ingredients")

@app.route("/team")
def view_team_page():
    return render_template("team.html", title="Meet the Team")


if __name__ == "__main__":
    app.run()
