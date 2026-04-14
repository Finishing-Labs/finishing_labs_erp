"""
Models Package - Database initialization

This creates the SQLAlchemy database instance that all models will use.
For now, we're just setting up the foundation - actual models will be added later.
"""
from flask_sqlalchemy import SQLAlchemy

# Create the database instance
# This will be initialized in app.py with app.config settings
db = SQLAlchemy()

# Import models here when they're created
# from .customer import Customer
# from .order import Order, OrderItem
# from .production import ProductionJob
# etc.
