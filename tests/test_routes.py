"""
Recommendations API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_service.py:TestRecommendationService
"""

import os
import logging
from unittest import TestCase
# from unittest.mock import MagicMock, patch

from urllib.parse import quote_plus
from service import app
from service.models import db, init_db, Recommendation
from service.common import status  # HTTP Status Codes
from tests.factories import RecommendationFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/recommendations"

######################################################################
#  T E S T   S E R V I C E
######################################################################
class TestRecommendationService(TestCase):
    """Recommendation Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Recommendation).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def _create_recommendations(self, count):
        """Factory method to create recommendations in bulk"""
        recommendations = []
        for _ in range(count):
            test_recommendation = RecommendationFactory()
            response = self.client.post(BASE_URL, json=test_recommendation.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED, "Could not create test recommendation"
            )
            new_recommendation = response.get_json()
            test_recommendation.id = new_recommendation["id"]
            recommendations.append(test_recommendation)
        return recommendations

    def test_delete_recommendation(self):
        """It should Delete a Recommendation"""
        test_recommendation = self._create_recommendations(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

######################################################################
#  P L A C E   T E S T   C A S E S  &   S A D   P A T H S   H E R E
#Tip: Make sure to grab from both 'test cases' and 'sad paths'!
######################################################################

    def test_index(self):
        """It should call the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Recommendations REST API Service")

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/healthcheck")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["message"], "Healthy")

######################################################################
    #  RETRIEVE/GET A RECOMMENDATION (READ)
######################################################################

    def test_get_recommendation(self):
        """It should Get a single recommendation"""
        # get the id of a recommendation
        test_recommendation = self._create_recommendations(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["user_segment"], test_recommendation.user_segment)


    def test_get_recommendation_not_found(self):
        """It should not Get a recommendation thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

######################################################################
    #  ADD A RECOMMENDATION (CREATE)
######################################################################

    def test_create_recommendation_no_content_type(self):
        """It should not Create a recommendation with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_recommendation_wrong_content_type(self):
        """It should not Create a recommendation with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

######################################################################
#  Update A RECOMMENDATION (Update)
######################################################################
    def test_update_recommendation(self):
        """It should Update an existing recommendation"""
        # create a recommendation to update
        test_recommendation = RecommendationFactory()
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the recommendation
        new_recommendation = response.get_json()
        logging.debug(new_recommendation)
        new_recommendation["user_segment"] = "unknown"
        response = self.client.put(f"{BASE_URL}/{new_recommendation['id']}",
                                   json=new_recommendation)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_recommendation = response.get_json()
        self.assertEqual(updated_recommendation["user_segment"], "unknown")

    def test_update_recommendation_not_found(self):
        """It should Update a Recommendation and Return Not Found"""
        test_recommendation = RecommendationFactory()
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_recommendation = response.get_json()
        logging.debug(new_recommendation)
        new_recommendation["user_segment"] = "unknown"
        new_recommendation['id'] = 0
        response = self.client.put(f"{BASE_URL}/{new_recommendation['id']}",
                                   json=new_recommendation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

######################################################################
## Some list test are dependent on the tests below.
######################################################################
    def test_create_recommendation(self):
        """It should Create a new Recommendation"""
        test_recommendation = RecommendationFactory()
        logging.debug("Test Recommendation: %s", test_recommendation.serialize())
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_recommendation = response.get_json()
        self.assertEqual(new_recommendation["user_segment"], test_recommendation.user_segment)
        self.assertEqual(new_recommendation["product_id"], test_recommendation.product_id)
        self.assertEqual(new_recommendation["user_id"], test_recommendation.user_id)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_recommendation = response.get_json()
        self.assertEqual(new_recommendation["user_segment"], test_recommendation.user_segment)
        self.assertEqual(new_recommendation["product_id"], test_recommendation.product_id)
        self.assertEqual(new_recommendation["user_id"], test_recommendation.user_id)


######################################################################
    #  LIST A RECOMMENDATION (LIST)
######################################################################

    def test_get_recommendation_list(self):
        """It should Get a list of Recommendations"""
        self._create_recommendations(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_query_recommendation_list_by_user_segment(self):
        """It should Query Recommendations by User Segment"""
        recommendations = self._create_recommendations(10)
        test_user_segment = recommendations[0].user_segment
        user_segment_recommendations = [
            recommendation for recommendation in recommendations if (
            recommendation.user_segment == test_user_segment)]
        response = self.client.get(
            BASE_URL,
            query_string=f"user_segment={quote_plus(test_user_segment)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(user_segment_recommendations))
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["user_segment"], test_user_segment)

    def test_query_recommendation_list_by_product_id(self):
        """It should Query Recommendations by Product ID"""
        recommendations = self._create_recommendations(10)
        test_product_id = recommendations[0].product_id
        product_id_recommendations = [
            recommendation for recommendation in recommendations if (
            recommendation.product_id == test_product_id)]
        response = self.client.get(
            BASE_URL,
            query_string=f"product_id={test_product_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(product_id_recommendations))
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["product_id"], test_product_id)

    def test_query_recommendation_list_by_user_id(self):
        """It should Query Recommendations by User ID"""
        recommendations = self._create_recommendations(10)
        test_user_id = recommendations[0].user_id
        user_id_recommendations = [
            recommendation for recommendation in recommendations if (
            recommendation.user_id == test_user_id)]
        response = self.client.get(
            BASE_URL,
            query_string=f"user_id={test_user_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(user_id_recommendations))
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["user_id"], test_user_id)

    def test_query_recommendation_list_by_viewed_in_last7d(self):
        """It should Query Recommendations by views in the last seven days"""
        recommendations = self._create_recommendations(10)
        test_viewed_in_last7d = recommendations[0].viewed_in_last7d
        viewed_in_last7d_recommendations = [
            recommendation for recommendation in recommendations if (
            recommendation.viewed_in_last7d == test_viewed_in_last7d)]
        response = self.client.get(
            BASE_URL,
            query_string=f"viewed_in_last7d={test_viewed_in_last7d}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(viewed_in_last7d_recommendations))
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["viewed_in_last7d"], test_viewed_in_last7d)

    def test_query_recommendation_list_by_bought_in_last30d(self):
        """It should Query Recommendations by bought in the last 30 days"""
        recommendations = self._create_recommendations(10)
        test_bought_in_last30d = recommendations[0].bought_in_last30d
        bought_in_last30d_recommendations = [
            recommendation for recommendation in recommendations if (
            recommendation.bought_in_last30d == test_bought_in_last30d)]
        response = self.client.get(
            BASE_URL,
            query_string=f"bought_in_last30d={test_bought_in_last30d}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(bought_in_last30d_recommendations))
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["bought_in_last30d"], test_bought_in_last30d)