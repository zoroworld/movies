Great! Based on your GitHub repo structure, here’s a **proper README** for your Movie Theatre Ticket Booking System, including explanations for `Theatre`, `Movie`, `Seat`, `Show`, `ShowTime`, `Booking`, etc.

---

# Movie Theatre Ticket Booking System

A **Movie Theatre Ticket Booking System** allows users to view movies, show times, and seat availability. Customers can choose a movie, theatre, and seats, then book tickets online or offline. After payment, a digital or printed ticket is generated, saving time and reducing queues.

---

## Features

* View all available **movies** and **showtimes**
* Check **seat availability** in theatres
* Book tickets **online or offline**
* Generate **digital or printed tickets**
* Admin can manage **movies, theatres, shows, and bookings**

---

## Project Structure

### 1. **Theatre**

Represents a movie theatre. Contains information like:

* Name of theatre
* Location
* Number of screens
* Seating capacity

### 2. **Movie**

Represents a movie being shown:

* Title, genre, language
* Duration
* Release date
* Rating

### 3. **Seat**

Represents a seat in a theatre screen:

* Seat number
* Row
* Status (available/booked)

### 4. **Show**

Represents a particular screening of a movie at a theatre:

* Movie reference
* Theatre reference
* Show date & time
* Screen number

### 5. **ShowTime**

Represents the timing of a movie show:

* Start time
* End time
* Can be associated with multiple shows

### 6. **Booking**

Represents a ticket booking:

* User/customer reference
* Movie & Show reference
* Seats booked
* Payment status
* Booking timestamp

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/zoroworld/movies.git
cd movies
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run migrations**

```bash
python manage.py migrate
```

4. **Start the server**

```bash
python manage.py runserver
```

5. **Access the app**

```
http://127.0.0.1:8000/
```

---

## Technologies Used

* Python 3.x
* Django 5.x
* SQLite (default, can switch to PostgreSQL)
* HTML, CSS, JavaScript
* Docker (optional for deployment)
* Razorpay (payment integration)

---

## Usage

1. **Browse Movies** – View all movies playing in theatres.
2. **Check Shows** – View show times for each movie.
3. **Select Seats** – Choose available seats in a theatre.
4. **Book Tickets** – Pay online or reserve offline.
5. **Get Ticket** – Receive a digital ticket or print a physical copy.

---

## Notes

* Admin can add/remove **theatres, movies, shows, and showtimes**
* Customers can see **real-time seat availability**
* Designed to reduce queues and streamline ticket booking

##  Login Credentials (Demo)

| Username | Password  | Role     |
|----------|-----------|----------|
| admin    | admin123# | ADMIN    |
| user     | user123#  | CUSTOMER |

