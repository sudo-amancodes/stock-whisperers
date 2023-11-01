from flask import Flask, abort, redirect, render_template, request

app = Flask(__name__)
app.debug = True


@app.get('/')
def index():
    return render_template('index.html')

#Create Comments or add a temporary get/post request. That has a pass statement.
#Example:
#@app.get('/test')
#def testing():
#    pass