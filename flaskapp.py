from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbcode import *
app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    results = show_movies()
    return render_template('home.html',results = results)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
