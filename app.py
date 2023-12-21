from flask import Flask, render_template, request, redirect,jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

engine = create_engine("mysql+mysqlconnector://singly:123@localhost/flask")
import routes



if __name__ == '__main__':
    app.run()


@app.route('/rng')
def rng():
    return render_template("rng.html")