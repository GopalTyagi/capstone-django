# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime
from .models import CarMake, CarModel
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


def initiate():
    car_make_data = [
        {"name":"NISSAN", "description":"Great cars. Japanese technology"},
        {"name":"Mercedes", "description":"Great cars. German technology"},
        {"name":"Audi", "description":"Great cars. German technology"},
        {"name":"Kia", "description":"Great cars. Korean technology"},
        {"name":"Toyota", "description":"Great cars. Japanese technology"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(CarMake.objects.create(
            name=data['name'], 
            description=data['description']
        ))

    car_model_data = [
        {"name":"Pathfinder", "type":"SUV", "year": 2023, "car_make":car_make_instances[0]},
        {"name":"Qashqai", "type":"SUV", "year": 2023, "car_make":car_make_instances[0]},
        {"name":"XTRAIL", "type":"SUV", "year": 2023, "car_make":car_make_instances[0]},
        {"name":"A-Class", "type":"SUV", "year": 2023, "car_make":car_make_instances[1]},
        {"name":"C-Class", "type":"SUV", "year": 2023, "car_make":car_make_instances[1]},
        {"name":"E-Class", "type":"SUV", "year": 2023, "car_make":car_make_instances[1]},
        {"name":"A4", "type":"SUV", "year": 2023, "car_make":car_make_instances[2]},
        {"name":"A5", "type":"SUV", "year": 2023, "car_make":car_make_instances[2]},
        {"name":"A6", "type":"SUV", "year": 2023, "car_make":car_make_instances[2]},
        {"name":"Sorrento", "type":"SUV", "year": 2023, "car_make":car_make_instances[3]},
        {"name":"Carnival", "type":"SUV", "year": 2023, "car_make":car_make_instances[3]},
        {"name":"Cerato", "type":"Sedan", "year": 2023, "car_make":car_make_instances[3]},
        {"name":"Corolla", "type":"Sedan", "year": 2023, "car_make":car_make_instances[4]},
        {"name":"Camry", "type":"Sedan", "year": 2023, "car_make":car_make_instances[4]},
        {"name":"Kluger", "type":"SUV", "year": 2023, "car_make":car_make_instances[4]},
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            car_make=data['car_make'],
            type=data['type'],
            year=data['year']
        )

def get_cars(request):
    count = CarMake.objects.all().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]
    return JsonResponse({"CarModels": cars})

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
