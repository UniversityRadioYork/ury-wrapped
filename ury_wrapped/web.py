from flask import Flask, render_template, request
import requests
from io import BytesIO
from werkzeug.exceptions import Unauthorized

from config import cfg
from tasks import TASKS
import db
from imaging import generate_image

app = Flask(__name__)


def memberid_from_request():
    try:
        cookie = request.headers["Cookie"]
    except:
        raise Unauthorized()
    r = requests.get(
        "https://ury.org.uk/api/v2/user/currentuser",
        headers={"Cookie": cookie},
    )
    if r.status_code != 200:
        raise Unauthorized()
    return r.json()["payload"]["memberid"]


@app.route("/img/<task>")
def task_image(task: str):
    try:
        _, query, formatter = next(filter(lambda t: t[0] == task, TASKS))
    except StopIteration:
        return "Invalid task", 404

    result = db.query_one(query, memberid_from_request())
    if result is None:
        return "No results", 400
    text = formatter(result)
    im = generate_image(text)
    buf = BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue(), 200, {"Content-Type": "image/png"}


@app.route("/")
def index():
    try:
        memberid = memberid_from_request()
    except Unauthorized:
        return render_template("signin.html.j2")
    return render_template("index.html.j2", task_names=[t[0] for t in TASKS])


if __name__ == "__main__":
    app.run(port=cfg.http_port)
