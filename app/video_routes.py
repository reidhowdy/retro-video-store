""" from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import exc
load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"])
def get_video():
    videos = Video.query.all()

    response = []
    for video in videos:
        response.append(video.to_dict())

    return jsonify(response), 200


@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    #try:
    new_video = Video.from_dict(request_body)
    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_dict()), 201

    #response = {

    #} """



