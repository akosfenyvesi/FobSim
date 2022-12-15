import json
import re

from flask import Flask, redirect, url_for, render_template, request, send_file, flash
from markupsafe import Markup
import main
from io import StringIO
import sys
import os


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


def read_files(files):
    contents = []
    for file in files:
        with open(f"temporary/{file}", "r", encoding="utf-8") as fp:
            json_data = fp.read()
            json_data = Markup(re.sub(
                r'(\"(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\\"])*\"(\s*:\s*)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)',
                lambda match: '<span class="{}">{}</span>'.format(
                    "number" if match.group(0).isdigit() else "string", match.group(0)
                ),
                json_data
            ))
            contents.append(json_data)
    return contents


@app.route("/simulation", methods=["POST", "GET"])
def simulation():
    if request.method == "POST":
        data = request.form
        print(data)
        tmp = sys.stdout
        output_results = StringIO()
        sys.stdout = output_results
        main.run_simulations()
        sys.stdout = tmp
        files = os.listdir("temporary")
        contents = read_files(files)
        print(contents)
        return render_template("results.html", results=output_results.getvalue(), len=len(files), files=files,
                               contents=contents)
    return render_template("settings.html")


# @app.route("/test")
# def test():
#     return render_template("graph_modal.html")


@app.route("/results")
def results():
    return render_template("results.html")


@app.route("/previous-simulations")
def previous_simulations():
    return render_template("previoussettings.html")


@app.route("/documentation")
def docs():
    return render_template("documentation.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)
