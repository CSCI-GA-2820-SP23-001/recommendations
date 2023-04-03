"""
Recommendations Service

Paths:
------
GET /recommendations - Returns a list all of the Recommendations
GET /recommendations/{id} - Returns the Recommendation with a given id number
POST /recommendations - creates a new Recommendation record in the database
PUT /recommendations/{id} - updates a Recommendation record in the database
DELETE /recommendations/{id} - deletes a Recommendation record in the database

GET /recommendations/popular - Returns a list of popular recommendations
    required parameter: 'count' [Popular -> Recent (7d) and most viewed]
"""

# from flask import Flask, make_response
import datetime
from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Recommendation

# Import Flask application
from . import app

######################################################################
# GET HEALTH CHECK
######################################################################


@app.route("/healthcheck")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Recommendations REST API Service",
            version="1.0",
            paths=url_for("list_recommendations", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s",
                     request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )

######################################################################
#  R E S T   A P I   E N D P O I N T S
# @everyone - add your code below here!
######################################################################

######################################################################
# LIST ALL RECOMMENDATIONS (LIST)
######################################################################


@app.route("/recommendations", methods=["GET"])
def list_recommendations():
    """Returns all of the Recommendations"""
    app.logger.info("Request for recommendation list")
    recommendations = []
#    rec_id = request.args.get("id")
    user_segment = request.args.get("user_segment")
    product_id = request.args.get("product_id")
    user_id = request.args.get("user_id")
    viewed_in_last7d = request.args.get("viewed_in_last7d")
    bought_in_last30d = request.args.get("bought_in_last30d")
    last_relevance_date = request.args.get("last_relevance_date")
    recommendation_type = request.args.get("recommendation_type")
    if user_segment:
        recommendations = Recommendation.find_by_user_segment(user_segment)
    elif product_id:
        recommendations = Recommendation.find_by_product_id(product_id)
    elif user_id:
        recommendations = Recommendation.find_by_user_id(user_id)
    elif viewed_in_last7d:
        recommendations = Recommendation.find_by_viewed_in_last7d(viewed_in_last7d)
    elif bought_in_last30d:
        recommendations =Recommendation.find_by_bought_in_last30d(bought_in_last30d)
    else:
        recommendations = Recommendation.all()

    results = [recommendation.serialize()
               for recommendation in recommendations]
    app.logger.info("Returning %d recommendations", len(results))
    return jsonify(results), status.HTTP_200_OK

######################################################################
# RETRIEVE A RECOMMENDATION (READ)
######################################################################


@app.route("/recommendations/<int:rec_id>", methods=["GET"])
def get_recommendation(rec_id):
    """
    Retrieve a single recommendation
    This endpoint will return a recommendation based on it's id
    """
    app.logger.info("Request for recommendation with id: %s", rec_id)
    recommendation = Recommendation.find(rec_id)
    if not recommendation:
        abort(status.HTTP_404_NOT_FOUND,
              f"recommendation with id '{rec_id}' was not found.")

    app.logger.info("Returning recommendation: %s",
                    recommendation.user_segment)
    return jsonify(recommendation.serialize()), status.HTTP_200_OK

######################################################################
# ADD A NEW RECOMMENDATION (CREATE)
######################################################################


@app.route("/recommendations", methods=["POST"])
def create_recommendation():
    """
    Creates a recommendation
    This endpoint will create a recommendation based the data in the body that is posted
    """
    app.logger.info("Request to create a recommendation")
    check_content_type("application/json")
    recommendation = Recommendation()
    recommendation.deserialize(request.get_json())
    recommendation.create()
    message = recommendation.serialize()
    location_url = url_for("get_recommendation",
                           rec_id=recommendation.id, _external=True)

    app.logger.info("Recommendation with ID [%s] created.", recommendation.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
# DELETE A RECOMMENDATION
######################################################################


@app.route("/recommendations/<int:rec_id>", methods=["DELETE"])
def delete_recommendation(rec_id):
    """
    Delete a recommendation
    This endpoint will delete a recommendation based the id specified in the path
    """
    app.logger.info("Request to delete recommendation with id: %s", rec_id)
    recommendation = Recommendation.find(rec_id)
    if recommendation:
        recommendation.delete()

    app.logger.info("Recommendation with ID [%s] delete complete.", rec_id)
    return "", status.HTTP_204_NO_CONTENT

######################################################################
# UPDATE AN EXISTING recommendation
######################################################################


@app.route("/recommendations/<int:rec_id>", methods=["PUT"])
def update_recommendations(rec_id):
    """
    Update a recommendation

    This endpoint will update a recommendation based the body that is posted
    """
    app.logger.info("Request to update recommendation with id: %s", rec_id)
    check_content_type("application/json")

    recommendation = Recommendation.find(rec_id)
    if not recommendation:
        abort(status.HTTP_404_NOT_FOUND,
              f"recommendation with id '{rec_id}' was not found.")

    recommendation.deserialize(request.get_json())
    recommendation.id = rec_id
    recommendation.update()

    app.logger.info("recommendation with ID [%s] updated.", recommendation.id)
    return jsonify(recommendation.serialize()), status.HTTP_200_OK

######################################################################
# LIST POPULAR RECOMMENDATIONS (POPULAR = MOST VIEWED AND RECENT)
######################################################################


@app.route("/recommendations/popular", methods=["GET"])
def list_popular_recommendations():
    """Returns count number of popular recommendations"""
    app.logger.info("Request to list popular recommendations")
    recommendations = []

    # Required parameter
    count = request.args.get("count")

    # Filter by last week
    last_week_date = datetime.date.today() - datetime.timedelta(days=7)
    recommendations = Recommendation.find_after_last_relevance_date(
        last_week_date.isoformat())

    # Get number of views for products viewed_in_last7d
    popular_tracker = {}
    for recommendation in recommendations:
        if recommendation.viewed_in_last7d:
            if recommendation.product_id in popular_tracker:
                popular_tracker[recommendation.product_id] += 1
            else:
                popular_tracker[recommendation.product_id] = 1

    # Sort by most popular products
    sorted_tracker = sorted(popular_tracker.items(),
                            key=lambda x: x[1], reverse=True)

    # Process results after checking for corner cases
    results = []
    if (count is None) or not count.isnumeric():
        abort(status.HTTP_400_BAD_REQUEST,
              "Parameter 'count' not specified/malformed")
    elif int(count) > len(sorted_tracker):
        abort(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
              "Too many recommendations requested")
    elif int(count) <= 0:
        abort(status.HTTP_406_NOT_ACCEPTABLE,
              "Invalid number of recommendations requested")
    else:
        for rec in sorted_tracker[:int(count)]:
            prod_res = Recommendation.find_by_product_id(rec[0])
            results.append(prod_res[0].serialize())

    app.logger.info("Returning %d popular recommendations", len(results))
    return jsonify(results), status.HTTP_200_OK
