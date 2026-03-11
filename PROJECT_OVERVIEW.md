# Hiecon Website Project Overview

## What this project is
This repository is a **Django 5** website for Hiecon that combines:
- A public marketing website (home/about/services/contact)
- A product catalog with filtering and product detail pages
- Basic account registration/login
- A cart and cart submission workflow
- Newsletter subscription and contact-query email handling

## Tech stack
- Python 3.11 (`runtime.txt`)
- Django 5 (`requriment.txt`)
- MySQL backend (`mywebsite/settings.py`)
- Jazzmin for Django admin UI customization
- Static/media asset serving configured in Django

## High-level structure
- `mywebsite/`: Django project configuration (`settings.py`, root URLs, WSGI/ASGI)
- `hiecon/`: Main application logic (models, forms, views, app URL routes, templates)
- `static/`: Front-end CSS/JS/image assets
- `media/`: Uploaded product images
- `db.sqlite3`: Local SQLite file exists, though current settings are configured for MySQL

## Main domain models (`hiecon/models.py`)
- `Customer`: Extends Django `User` with profile fields (name/address/email/mobile)
- `Product`: Product catalog records with category/subcategory/make, specs, catalogue links, and up to 5 images; generates slug from product name
- `Cart`: Cart header linked to a customer, with total calculation helper and last submission timestamp
- `Cartproduct`: Line items for cart quantity/subtotal
- `Solution`: Named solutions grouped by category
- `Newsletter`: Stores subscribed email addresses
- `Visitor`: Stores a simple counter used by the homepage

## Routing and request flow
- Root URL config includes `hiecon.urls` and admin routes (`mywebsite/urls.py`)
- App URL routes map to page views and e-commerce flows (`hiecon/urls.py`), including:
  - Marketing pages (`/`, `/about/`, `/services/`, `/contact/`)
  - Product list and details (`/products/`, `/products/<slug>/`)
  - Auth pages (`/register/`, `/login/`, `/logout/`)
  - Cart actions (`/cart/`, `/add_to_cart/...`, `/update_quantity/...`, `/submit_cart/`)
  - Newsletter and query handlers

## Important view behavior (`hiecon/views.py`)
- `Index`: Increments visitor counter and computes cart count for logged-in users
- `ProductListView`: Supports search (`query`) and filtering (`category`, `subcategory`, `make`) plus pagination
- `ProductDetailView`: Supports ID or slug lookup and builds a list of product images plus similar products
- Registration/Login/Logout: Custom user account flows
- Cart views: Add/remove/update quantity and submit cart (which emails admin and rotates to a new cart)
- `handle_query_form`: Sends contact form content via email
- `newsletter_subscribe`: Stores unique newsletter emails

## Templates and UI
- `hiecon/templates/base.html` is the shared shell (header/footer/nav/assets)
- Page templates for home, product list/detail, cart, auth, and static content pages
- `static/hiecon/css/style.css` and `static/hiecon/js/main.js` provide front-end styling and interactions

## Configuration notes
- `ALLOWED_HOSTS = ['*']` and `DEBUG = True` in settings indicate development-style configuration.
- SMTP credentials and Django `SECRET_KEY` are currently hardcoded in settings.
- Static files are collected into `staticfiles/`; media is in `media/`.

## Potential cleanup opportunities
- There are duplicate function definitions for cart handlers in `views.py`.
- Some model methods appear misspelled (e.g., `_str_` instead of `__str__`).
- Cart line-item logic references `product.price`, but `Product` currently has no `price` field in the model.
- URL config contains duplicate route definitions for product detail.

