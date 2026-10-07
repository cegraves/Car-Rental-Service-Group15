# Car Rental Service 🏎️🏎️ – Group 15

## CIS 453 – Software Specification and Design

This repository contains our group project for CIS 453.

The goal of the project is to apply the Software Development Life Cycle (SDLC) by planning, designing, implementing, and testing a prototype Car Rental Service.

## Team Members

- Claire Graves
- Ryan Cupplo
- Tanner Moore
- Tanzila Uddin

## Repository Contents

The repository contains:

- Flask/Python application source code
- HTML frontend template
- Database setup documentation
- Booking/payment flow diagram
- Project README and repository files

## Project Overview

Citrus Rentals is a web-based car rental prototype designed primarily for the Syracuse University community. Users can browse rental vehicles, filter vehicles by category, and submit vehicle reservations.

The project was developed throughout several phases:

- Week 1: Planning and requirements gathering
- Week 2: System architecture and design
- Week 3: Prototype development
- Week 4: Implementation, testing, and reflection


## Technology Stack

- HTML – Frontend structure
- CSS – Frontend styling
- JavaScript – Booking modal interaction
- Python / Flask – Backend and web application
- Flask-SQLAlchemy – Database integration
- MySQL – Database
- GitHub – Version control and team repository

## Current Prototype Features

The current prototype includes:

- Displaying rental vehicles stored in the MySQL database
- Vehicle images and daily rental prices loaded dynamically from the database
- Filtering vehicles by category (SUV, Sedan, Truck, and Electric)
- Vehicle selection and booking form
- JavaScript-based booking and payment modals
- Pickup and return date selection
- Syracuse `@syr.edu` email validation
- 9-digit SUID validation
- Prevention of overlapping bookings for the same vehicle
- Automatic creation of a user record when a new customer makes a booking
- Booking information stored in the MySQL database
- Multi-step booking and mock payment checkout
- Dynamic rental price calculation based on selected dates and daily vehicle price
- Payment records stored in MySQL with booking ID, amount, and status


## Database

The database design contains five main tables:

- `user`
- `category`
- `vehicle`
- `booking`
- `payment`

The `user` and `vehicle` tables connect to bookings, while vehicles are organized by category. A payment table is also included in the database design for the planned payment functionality.

## Project Architecture

The project follows a three-layer architecture:

1. **Presentation Layer** – HTML, CSS, and JavaScript used for the user interface
2. **Application Layer** – Python and Flask used for application logic, validation, and booking processing
3. **Data Layer** – MySQL used to store users, vehicles, categories, bookings, and payment information

Flask connects the frontend to the MySQL database through Flask-SQLAlchemy.
