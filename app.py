import base64
import os
import pickle

from flask import Flask, abort, jsonify, make_response, render_template_string, request, send_file

import db
import utils

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-123"

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")


def load_session():
    raw = request.cookies.get("session_data")
    if not raw:
        return {}
    return pickle.loads(base64.b64decode(raw))


@app.post("/login")
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    user = db.get_user(username)
    if not user or user["password_hash"] != utils.hash_password(password):
        abort(401)
    data = base64.b64encode(pickle.dumps({"user_id": user["id"], "username": username})).decode()
    resp = make_response(jsonify(ok=True))
    resp.set_cookie("session_data", data)
    return resp


@app.get("/products")
def products():
    return jsonify(db.search_products(request.args.get("q", "")))


@app.get("/invoice/<int:invoice_id>")
def invoice(invoice_id):
    if "user_id" not in load_session():
        abort(401)
    inv = db.get_invoice(invoice_id)
    if not inv:
        abort(404)
    return jsonify(inv)


@app.get("/download")
def download():
    name = request.args.get("file", "")
    return send_file(os.path.join(UPLOAD_DIR, name))


@app.get("/hello")
def hello():
    name = request.args.get("name", "guest")
    return render_template_string(f"<h1>Hello {name}!</h1>")


@app.get("/tools/ping")
def ping():
    return utils.ping_host(request.args.get("host", "127.0.0.1"))


@app.get("/tools/disk")
def disk():
    return utils.disk_usage()


@app.get("/preview")
def preview():
    return utils.fetch_preview(request.args.get("url", ""))


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
