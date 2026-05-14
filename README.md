# JWT Authentication API

A Flask API using JWT authentication.

## Features
- User registration
- User login
- JWT token generation
- Protected routes
- SQLite database

## Technologies Used
- Python
- Flask
- PyJWT
- SQLite3

## Installation

pip install flask pyjwt

## Run

python app.py

## API Endpoints

POST /register  
POST /login  
GET /profile

## Example Login JSON

{
    "username": "admin",
    "password": "1234"
}

## Purpose
focuses on JWT authentication and API security.
