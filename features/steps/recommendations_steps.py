######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=no-name-in-module, missing-timeout

"""
Recommendations Steps

Steps file for recommendations.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given
from compare import expect


@given('the following recommendations')
def step_impl(context):
    """ Delete all Recommendations and load new ones """
    # List all of the recommendations and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/recommendations"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for rec in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{rec['id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new pets
    for row in context.table:
        payload = {
            "product_id": row['product_id'],
            "user_id": row['user_id'],
            "user_segment": row['user_segment'],
            "viewed_in_last7d": row['viewed_in_last7d'] in ['True', 'true', '1'],
            "bought_in_last30d": row['bought_in_last30d'] in ['True', 'true', '1'],
            "last_relevance_date": row['last_relevance_date'],
            "recommendation_type": row['recommendation_type'],
            "origin_product_id": row['origin_product_id'],
            "rating": row['rating']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)
