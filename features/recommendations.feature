Feature: Recommendations service back-end
    As a Recommendations Marketing Manager
    I need a RESTful catalog service
    So that I can keep track of all recommendations

Background:
    Given the following recommendations
        | product_id | user_id  | user_segment | viewed_in_last7d  | bought_in_last30d | last_relevance_date | recommendation_type  | origin_product_id | rating |
        | 123        | 456      | Tech MBA     | True              | True              | 2019-11-18          | NEW_ARRIVAL          |                   | 4      |
        | 123        | 456      | Tech MBA     | False             | False             | 2022-10-01          | TOP_RATED            |                   | 5      |
        | 234        | 457      | Happy Prof   | True              | False             | 2021-09-28          | TRENDING             |                   | 5      |
        | 235        | 458      | DevOps TA    | False             | True              | 2020-09-30          | ADD_ON               | 123               | 4      |
        | 236        | 459      | DevOps TA    | True              | True              | 2020-09-30          | FREQ_BOUGHT_TOGETHER | 234               | 3      |
        | 345        | 233      | Dog Dad      | False             | True              | 2022-08-30          | UPGRADE              | 677               |        |
        | 7888       | 112      | Musician     | False             | False             | 2023-03-31          | RECOMMENDED_FOR_YOU  |                   | 2      |
        | 289        | 996      | Developer    | True              | False             | 2020-02-17          | SIMILAR_PRODUCT      | 234               | 1      |
        | 343        | 457      | Happy Prof   | False             | False             | 2017-01-01          | UNKNOWN              |                   |        |
        | 555        | 888      | AI Bot       | True              | True              | 2023-04-01          | UNKNOWN              |                   |        |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Recommendations REST API Service" in the title
    And I should not see "404 Not Found"


Scenario: Update a Recommendation
    When I visit the "Home Page"
    And I set the "Product ID" to "555"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "555" in the "Product ID" field
    And I should see "888" in the "User ID" field
    When I change "Product ID" to "789"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "789" in the "Product ID" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "789" in the results
    And I should not see "555" in the results
