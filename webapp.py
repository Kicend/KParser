from flask import Flask, render_template, request
from webbrowser import open
from os import system

app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def root():
    return render_template("index.html")


@app.route("/kparser.html", methods=["GET", "POST"])
def kparser():
    if request.method == "POST":
        queries_number = request.form.get("queries_number")
        search_lang = request.form.get("search_lang")
        query = request.form.get("query")
        system(f"python KParser.py -n {queries_number} -l {search_lang} \"{query}\"")
    return render_template("kparser.html")


if __name__ == "__main__":
    open("http://127.0.0.1:5000")
    app.run()
