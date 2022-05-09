from  .import bp as main
from flask import render_template
@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html.j2")
