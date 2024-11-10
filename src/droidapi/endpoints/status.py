from flask import request

from droidapi import authorized_only
from droidapi.app import app


@app.route("/api/v1/status", methods=["GET"])
def status():
    return {"status": "ok"}

@app.route("/api/v1/token", methods=["GET"])
@authorized_only
def token():
    return {"status": "ok", "token": request.current_token.to_dict()}