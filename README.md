## Django Server for Ecommerce
Deployed using nixpacks.json and railway.json to railway
## Django REST Server with Elasticsearch Integration

This Django project is a REST server that provides construction rates calculation and also integrates with Django-Oscar Commerce for purchasing hardware materials. The server is built using Django and Django REST Framework, and Elasticsearch is used to improve the search functionality.
## Features

    Calculates construction rates based on various parameters such as area, material type, labor cost, etc.
    Integrates with Django-Oscar Commerce to allow users to purchase hardware materials.
    Utilizes Elasticsearch to provide a fast and accurate search functionality.

Requirements

    Python 3.x
    Django 3.x
    Django REST Framework
    Elasticsearch

## Installation

Clone the repository to your local machine:

### bash

    git clone https://github.com/your_username/your_project.git

Install the required packages using pip:

bash

    pip install -r requirements.txt

Create a new Elasticsearch index:

bash

    python manage.py search_index --rebuild

Start the server:

bash

    python manage.py runserver

Usage
Construction Rates Calculation

To calculate the construction rates, make a POST request to the /construction-rates/ endpoint with the following parameters:

    area: The area of the construction site in square feet.
    material_type: The type of material to be used for construction.
    labor_cost: The cost of labor per hour.

Example:

bash

    curl -X POST http://localhost:8000/construction-rates/ -d '{"area": 1000, "material_type": "brick", "labor_cost": 50}' -H 'Content-Type: application/json'

The server will return the calculated rate as a JSON response:

json

    {
        "rate": 125000
    }

Hardware Material Purchase

To purchase hardware materials, first create an account on the Django-Oscar Commerce store. Then, make a POST request to the /api/basket/add-product/ endpoint with the following parameters:

    product_id: The ID of the product to be purchased.
    quantity: The quantity of the product to be purchased.

Example:

bash

    curl -X POST http://localhost:8000/api/basket/add-product/ -d '{"product_id": 1, "quantity": 2}' -H 'Content-Type: application/json' -H 'Authorization: Token <your_auth_token>'

The server will return a JSON response containing the updated basket:

json

    {
        "id": 1,
        "lines": [
            {
                "id": 1,
                "product": {
                    "id": 1,
                    "title": "Hammer",
                    "price": "10.00",
                    "currency": "USD"
                },
                "quantity": 2,
                "line_price": "20.00",
                "line_price_excl_tax": "20.00",
                "unit_price": "10.00",
                "unit_price_excl_tax": "10.00"
            }
        ],
        "is_tax_known": false,
        "num_items": 2,
        "total_excl_tax": "20.00",
        "total_incl_tax": "20.00",
        "total_tax": "0.00"
    }

Search Functionality

The server utilizes Elasticsearch to provide a fast and accurate search functionality. To search for a product, make a GET request to the /api/search/ endpoint with the following parameter:

    q: The search query.

Example:

bash

    curl http://localhost:8000/api/search/?q=hammer

