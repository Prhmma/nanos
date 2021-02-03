from flask import Flask, render_template, request, flash
import requests
from similarity import similarity


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        try:
            result = {}
            url = request.form["URL"]
            inputPS = request.form["InputPS"]
            web_page = requests.get(url, verify=False)
            if web_page.status_code == 200 and len(inputPS) > 0:
                simimilarity_object = similarity(inputPS, web_page.text)
                simimilarity_object.pre_processing()
                result = simimilarity_object.similarity_detection()
            return render_template("index.html", data=result)
        except Exception as ex:
            flash(ex)
            return render_template("index.html")


if __name__ == "__main__":
    app.run()
