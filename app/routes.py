from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()

    response = []
    for customer in customers:
        response.append({
            "name": customer.name,
            "id" : customer.cutomer_id,
            "phone": customer.phone_number,
            "postal_code": customer.postal_code
        })

    return jsonify(response), 200

