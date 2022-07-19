from flask import Flask, render_template
app = Flask(__name__)

##########################
# Flask routes
##########################
# render index.html home page
@app.route("/")
def index():
    file="about9.jpg"
    return render_template('index.html', file=file)

# render index.html home page
@app.route("/home")
def home():
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