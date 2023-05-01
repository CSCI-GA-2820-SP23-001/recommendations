# NYU DevOps Project Template

[![Build Status](https://github.com/CSCI-GA-2820-SP23-001/recommendations/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP23-001/recommendations)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP23-001/recommendations/branch/master/graph/badge.svg?token=A2OEYESQ3M)](https://codecov.io/gh/CSCI-GA-2820-SP23-001/recommendations)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is a skeleton you can use to start your projects

## Overview

This service allows product managers to query, create, delete, list and update recommendations for our E commerce application. The `/service` folder contains your `models.py` file for the model and a `routes.py` file for the services. The `/tests` folder contains test cases for testing the model and the service separately. 

##  Setup

The service can be launched using the "flask run" command in terminal and launching the recommendations platform in a browser (localhost:8000)

## Service
The service can be used through the cloud based UI. Searchable parameters include Recommendation ID, Product ID, User ID, User Segment, Viewed in last 7D (boolean), Viewed in last 30D (boolean). 

Using the UI the product marketing manager should be able to query (search) by these parameters and list results as well as update or change the resulting data. Results will be displayed at the bottom of the page.

Non searchable parameters include last relevance date, type, origin product ID, and rating.

## Contents

The project contains the following:

| Service | Method |
| -------- | -------- |
| update_recommendation | PUT |
| delete_recommendation | DELETE |
| list_recommendations | GET |
|get_recommendation | GET |
| create_recommendation | POST |
| list_popular_recommendations | GET |
| update_recommendation_rating | PUT |


```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.

