# Carento

**Carento** is a Python-based project designed to facilitate ***car rental*** services.
This repository reflects a modular and scalable architecture, prepared for local 
development and cloud deployment.

---
## Features

-  User authentication and role separation (customer/vendor)
-  Car management module for vendors
-  Booking management
-  Wallet for payments
-  Review system for feedback
-  Modular folder structure for easy scaling

---
##  Project Structure
```
├── src/
│   ├── auth/
│   │   ├── __init__.py
|   |   ├── Dependencies.py
|   |   ├── oauth2.py
│   │   └── schemas.py
│   ├── booking_table/
│   │   ├── __init__.py
│   │   ├── routes.py
|   |   ├── schemas.py
│   │   └── service.py
│   ├── review/
│   │   ├── __init__.py
│   │   ├── routes.py
|   |   ├── schemas.py
│   │   └── service.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── routes.py
|   |   ├── schemas.py
│   │   └── service.py
│   ├── vehicles/
│   │   ├── __init__.py
│   │   ├── routes.py
|   |   ├── schemas.py
│   │   └── service.py
│   └── wallet/
│   │   ├── __init__.py
│   │   ├── routes.py
|   |   ├── schemas.py
│   │   └── service.py
│   ├── __init__.py
│   ├── config.py
|   ├── README.md
│   └── utils.py
├── .env
├── Procfile
└── requirements.txt
└── README.md



```

---


## Tech Stack

- FASTAPI 
- PostgreSQL
- JWT for authentication 

---



---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/cyxabima/Carento-Server-API.git
cd Carento-Server-API
```

2. **Create a virtual environment:**
```bash
python -m venv venv
```
3. **Activate virtual environment:**
```bash
### On macOS/Linux:
source venv/bin/activate
### On Windows:
venv\Scripts\activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```
5. **Run the Server:**
``` bash 
    fast-api dev src
```
---
## Class Diagrams
```mermaid
classDiagram
    class BaseUser {
        <<abstract>>
        +string uid
        +string email
        +string phone_no
        +string password
        +get_all_user()
        +get_user_by_email()
        +*sign_up()*
        +*login()*
        +*delet_account()*
    }

    class Vendor {
        +string first_name
        +string last_name
        +string business_name 
        +boolean is_business
        +datetime created_at
        +datetime updated_at
        +get_all_vendors()
        +get_vendors_by_email()
        +signup()
        +login()
        +delete_account()  
            
    }

    class Customer {
        +string first_name
        +string last_name
        +datetime created_at
        +datetime updated_at
        +get_all_customers()
        +get_customers_by_email()
        +signup()
        +login()
        +delete_account() 
    }

    class Car {
        +string uid
        +string car_name
        +string image_url
        +string model_year
        +string brand
        +string car_category
        +string engine_size
        +string fuel_type
        +int siting_capacity
        +float price_per_day
        +string registration_no
        +string transmission
        +boolean is_booked
        +datetime created_at
        +datetime updated_at
        +string vendor_id
        +get_car()
        +create_car()
        +edit_car()
        +delete_car()
    }

    class Wallet {
        +string uid
        +float credit
        +customer_id
        +vendor_id
        +get_customer_wallet()
        +add_in_wallet()
        +get_vendor_wallet()
    }

    class Booking {
        +string uid
        +string customer_id
        +string vendor_id
        +string car_id
        +datetime start_time
        +datetime end_time
        +float total_price
        +bool is_active
        +get_booking_by_uid()
        +is_car_available()
        +customer_active_booking()
        +create_booking()
        +delete_booking()
        +get_vendor_booking()
        +get_customer_booking()
    }

    class Review {
        +string uid
        +customer_id
        +car_id
        +int rating
        +string review_text
        +datetime created_at
        +datetime updated_at
        +get_review_by_id()
        +has_reviewed()
        +create_review()
        +edit_review()
        +delte_review()
    }
 %% Inheritance
    Customer --|> BaseUser
    Vendor --|> BaseUser

    %% Composition (strong lifecycle dependency)
    Booking *-- Car : for >
    Booking *-- Wallet : pays with >

    Review *-- Car : about >
    Review *-- Customer : written by >

    %% Aggregation / Composition
    Customer *-- Wallet : owns >
    Vendor *-- Wallet : owns >

    %% Associations
    Vendor "1" --> "many" Car : owns >
    Customer "1" -- "!" Booking : books >
    
    Car "1" -- "many" Review : is reviewed in >
```
