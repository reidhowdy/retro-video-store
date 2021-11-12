from app import db
from flask import Blueprint, json, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from datetime import timedelta, date
from dotenv import load_dotenv
load_dotenv()

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def check_out():
    try:
        request_body = request.get_json()
        video = Video.query.get(request_body["video_id"])
        customer = Customer.query.get(request_body["customer_id"])
        if not video or not customer:
            return jsonify(None), 404

        videos_checked_out = Rental.query.filter_by(video_id=request_body["video_id"]).count()

        if video.total_inventory-videos_checked_out == 0:
            return jsonify({"message" : "Could not perform checkout"}), 400

        rental = Rental(video_id=request_body["video_id"], 
        customer_id=request_body["customer_id"], 
        due_date=date.today() + timedelta(days=7),
        )

        db.session.add(rental)
        db.session.commit()

        videos_checked_out += 1

        return jsonify({"customer_id": rental.customer_id,
            "video_id": rental.video_id,
            "due_date": rental.due_date,
            "videos_checked_out_count": videos_checked_out,
            "available_inventory": video.total_inventory-videos_checked_out}), 200
    except KeyError:
        return jsonify(None), 400


@rentals_bp.route("/check-in", methods=["POST"])
def check_in():
    try:
        request_body = request.get_json()
        video = Video.query.get(request_body["video_id"])
        customer = Customer.query.get(request_body["customer_id"])
        if not video or not customer:
            return jsonify(None), 404
        
        if video not in customer.videos:
            return jsonify({"message": f"No outstanding rentals for customer {request_body['customer_id']} and video {request_body['video_id']}"}), 400

        videos_checked_out = Rental.query.filter_by(video_id=request_body["video_id"]).count()
    
        rental = Rental.query.filter(Rental.customer_id==request_body['customer_id'], Rental.video_id==request_body['video_id'])
        rental.return_date = date.today()
        db.session.commit()

        videos_checked_out -= 1

        return jsonify({
            'video_id' : video.video_id,
            'customer_id' : customer.customer_id,
            "videos_checked_out_count": videos_checked_out,
            "available_inventory": video.total_inventory-videos_checked_out
        }), 200

    except KeyError:
        return jsonify(None), 400