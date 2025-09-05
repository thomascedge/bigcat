# Bookings API Documentation

## Base Path

All endpoints in this router are prefixed with `/bookings`.

---

## **Get All Bookings**

**Endpoint:**  

**Description:**  
Retrieve all bookings for the authenticated user.

**Authentication:**  
✅ Required (`CurrentUser`).

**Response Model:**  
[`BookingResponse`](src/bookings/model.py)

**Responses:**
- `200 OK` – Returns user’s bookings.
- `401 Unauthorized` – If not authenticated.

---

## **Search Booking**

**Endpoint:**  

**Description:**  
Search for bookings by filters.

**Query Parameters (optional):**
- `booking_id` (string) – Filter by booking ID.  
- `venue` (string) – Filter by venue.  

**Authentication:**  
✅ Required (`CurrentUser`).

**Response Model:**  
[`BookingResponse`](src/bookings/model.py)

**Responses:**
- `200 OK` – Returns filtered bookings.
- `401 Unauthorized` – If not authenticated.

---

## **Book Tickets**

**Endpoint:**  

**Description:**  
Book tickets for a concert.

**Authentication:**  
✅ Required (`CurrentUser`).

**Request Parameters:**
- `concert_id` (string) – ID of the concert.  
- `seats` (list of strings) – Seat IDs to book.  

**Responses:**
- `200 OK` – Tickets successfully booked.
- `400 Bad Request` – Invalid seat selection or concert.
- `401 Unauthorized` – If not authenticated.

---

## **Add Seat to Booking**

**Endpoint:**  

**Description:**  
Add a seat to an existing booking.

**Path Parameters:**
- `booking_id` (string) – Unique booking identifier.

**Authentication:**  
✅ Required (`CurrentUser`).

**Request Parameters:**
- `seat_id` (string) – Seat ID to add.

**Responses:**
- `200 OK` – Seat successfully added.
- `400 Bad Request` – Invalid seat or booking.
- `401 Unauthorized` – If not authenticated.

---

## **Remove Seat from Booking**

**Endpoint:**  

**Description:**  
Remove a seat from an existing booking.

**Path Parameters:**
- `booking_id` (string) – Unique booking identifier.

**Authentication:**  
✅ Required (`CurrentUser`).

**Request Parameters:**
- `seat_id` (string) – Seat ID to remove.

**Responses:**
- `200 OK` – Seat successfully removed.
- `400 Bad Request` – Invalid seat or booking.
- `401 Unauthorized` – If not authenticated.

---

## **Cancel Booking**

**Endpoint:**  

**Description:**  
Cancel an existing booking.

**Path Parameters:**
- `booking_id` (string) – Unique booking identifier.

**Authentication:**  
✅ Required (`CurrentUser`).

**Responses:**
- `200 OK` – Booking successfully canceled.
- `404 Not Found` – If booking does not exist.
- `401 Unauthorized` – If not authenticated.

---

## **Edit Booking**

**Endpoint:**  

**Description:**  
Edit booking details.

**Authentication:**  
✅ Required (`CurrentUser`).

**Request Parameters:**
- `booking_id` (string) – Unique booking identifier.  
- `booking_update` ([`Booking`](src/bookings/model.py)) – Updated booking details.  

**Responses:**
- `200 OK` – Booking updated.
- `400 Bad Request` – Invalid update request.
- `401 Unauthorized` – If not authenticated.
- `404 Not Found` – If booking does not exist.

---

## Models

### **BookingResponse**
Represents a list of bookings with metadata. Defined in `src/bookings/model.py`.

---

### **Booking**
Represents a booking object. Defined in `src/bookings/model.py`.

| Field        | Type     | Description                  |
|--------------|----------|------------------------------|
| `id`         | string   | Unique booking identifier    |
| `concert_id` | string   | ID of the booked concert     |
| `user_id`    | string   | ID of the booking user       |
| `seats`      | list     | List of booked seat IDs      |
| `status`     | string   | Booking status (active/canceled) |
| `created_at` | datetime | Booking creation timestamp   |
