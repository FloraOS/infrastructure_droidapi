import os
from datetime import datetime
import _md5
from flask import request
from werkzeug.utils import secure_filename

from droidapi.app import app
from droidapi.db import db
from droidapi.db.models.update import Update
from droidapi.helpers.authorization import authorized_only
from droidapi.helpers.form import need_form_fields


def update_from_form(form, file, filename, device, build_type, build_id) -> Update:
    update_model = Update()
    update_model.file_name = secure_filename(filename)
    update_model.timestamp = datetime.fromisoformat(form["isotime"])
    update_model.base_version = form["base_version"]
    update_model.file_id = _md5.md5(file + device + build_type + build_id).hexdigest()
    update_model.url = app.config["UPLOADS_URL"] + filename
    update_model.build_id = build_id
    update_model.size = file.size()
    return update_model

@app.route("/api/v1/update/push/<device>/<buildtype>/<build_id>", methods=["POST"])
@authorized_only
@need_form_fields(["base_version", "isotime"])
def update_push(device: str, buildtype: str, build_id: str):
    if 'ota.zip' not in request.files:
        return {"status": "no_file"}, 400
    file = request.files['file']
    filename = f"FloraOS-{build_id}-{device}-{buildtype}-OTA.zip"
    filename = secure_filename(filename)
    update_model = update_from_form(request.form, file, filename, device, buildtype, build_id)
    db.session.add(update_model)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    db.session.commit()
    return {"status": "ok"}, 201

@app.route("/api/v1/update/<device>/<buildtype>/<build_id>", methods=["GET"])
def update_get(device: str, buildtype: str, build_id: str):
    # We assume that all updates are incremental
    current_version = db.session().query(Update).filter_by(build_id=build_id, device=device, buildtype=buildtype).first()
    if current_version is None:
        # Unknown version: likely first update ever, return just all known updates
        all_updates_for_device = db.session().query(Update).filter_by(device=device, buildtype=buildtype).all()
        response = list()
        for update in all_updates_for_device:
            response.append(update.to_dict())
        return dict(response=response)
    # We know this version
    current_timestamp = current_version.timestamp
    # So find next one
    next_update = (db.session.query(Update)
                   .filter((Update.device==device) & (Update.buildtype==buildtype) & (Update.timestamp >= current_timestamp))
                   .order_by(Update.timestamp)).first()
    if next_update is None: # No updates
        return dict(response=list())
    return dict(response=[next_update])