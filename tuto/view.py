from .app import app
import yaml , os.path
from yaml import Loader
from flask import render_template

@app.route("/")
def home():
    return render_template(
            "home.html",
            title ="Hello World!",
            names =["Pierre", "Paul", "Corinne"]
    )

@app.route("/test")
def template2():
    print(os.path.join(os.path.dirname(__file__),"data.yml"))
    return render_template(
            "templates2.html",
            title = "Les 100 meilleurs bouqin de SF",
            data = yaml.load(open(
                        os.path.join(
                        os.path.dirname(__file__),
                        "data.yml"
                        )
                    ), Loader=Loader
                )
            )