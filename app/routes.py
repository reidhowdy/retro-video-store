from io import StringIO
from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import exc
load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()

    response = []
    for customer in customers:
        response.append(customer.to_dict())

    return jsonify(response), 200


@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    try:
        new_customer = Customer.from_dict(request_body)
        db.session.add(new_customer)
        db.session.commit()

        response = {
            "id" : new_customer.customer_id,
            "message" : "Customer successfully created."
        }

        return jsonify(response), 201
    
    except KeyError:
        if "postal_code" not in request_body.keys():
            response = {
                "details" : "Request body must include postal_code."
            }
        elif "name" not in request_body.keys():
            response = {
                "details" : "Request body must include name."
            }
        elif "phone" not in request_body.keys():
            response = {
                "details" : "Request body must include phone."
            }
        
        return jsonify(response), 400

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_a_customer(customer_id):
    # when sqlalchemy gets the customer_id from '/customer/customer_id' it takes customer_id
    # in as a string and has it's own way if discerning if that string is a sqlalchemy 'integer'
    # type or not:
        #SO when we make a guard clause to check if customer_id is an int, 
        # we have to use a string method to determine that
            # we can use .isnumeric() string method
    if not customer_id.isnumeric():
        return jsonify(None), 400
    
    customer = Customer.query.get(customer_id)
    if customer is None: 
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
        
    return jsonify(customer.to_dict()), 200
    
    #original working solution
    # try:
    #     customer = Customer.query.get(customer_id)
    #     if not customer: 
    #         return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    #     else:
    #         return jsonify(customer.to_dict()), 200

    # except exc.SQLAlchemyError:
    #     return jsonify(None), 400
    #     #look into 400: bad request

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    response = []
    for video in videos:
        response.append(video.to_dict())

    return jsonify(response), 200

@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    try:
        new_video = Video.from_dict(request_body)
        db.session.add(new_video)
        db.session.commit()

        return jsonify(new_video.to_dict()), 201

    except:
        if "title" not in request_body.keys():
            response = {
                "details" : "Request body must include title."
            }
        elif "release_date" not in request_body.keys():
            response = {
                "details" : "Request body must include release_date."
            }
        elif "total_inventory" not in request_body.keys():
            response = {
                "details" : "Request body must include total_inventory."
            }
        
        return jsonify(response), 400

@videos_bp.route("/<video_id>", methods=["GET"])
def get_a_video(video_id):
    video = Video.query.get(video_id)

    if not video:
        return jsonify({"message" : f"Video {video_id} was not found"}), 404

    return jsonify(video.to_dict()), 200    
    
@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_a_video(video_id):
    video = Video.query.get(video_id)
    
    if not video:
        return jsonify({"message" : f"Video {video_id} was not found"}), 404
    
    else:
        db.session.delete(video)
        db.session.commit()
        return jsonify(
        {
        "id": video.video_id, #this worked but video_id didnt??
        'details': (f'Video {video.video_id} successfully deleted')
        }

        ), 200


@videos_bp.route("/<video_id>", methods=["PUT"])
def patch_a_video(video_id):

    request_body = request.get_json()

    video = Video.query.get(video_id)

    if not video:
        return jsonify({"message" : f"Video {video_id} was not found"}), 404
    else:

        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]

        db.session.commit()

        return jsonify(video.to_dict()), 200