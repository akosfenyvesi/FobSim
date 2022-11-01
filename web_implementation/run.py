from flask import Flask, redirect, url_for, render_template, request, send_file, flash
import main
import contextlib

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/simulation", methods=["POST", "GET"])
def simulation():
    if request.method == "POST":
        with open("output.txt", 'w') as f:
            with contextlib.redirect_stdout(f):
                main.run_simulations()
        return redirect(url_for('results'))
    return render_template("settings.html")


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