# Seats API Documentation

## Base Path
`/seats`

All endpoints in this router are prefixed with `/seats`.

---

## **Get Seat by ID**

**Endpoint:**  
`GET /seats/{seat_id}`

**Description:**  
Retrieve details for a specific seat by its ID.

**Path Parameters:**
- `seat_id` (string) – Unique identifier for the seat.

**Authentication:**  
❌ Not required.

**Response Model:**  
[`Seat`](src/seats/model.py)

**Responses:**
- `200 OK` – Returns seat details.
- `404 Not Found` – If seat does not exist.

---

## **Search Seats**

**Endpoint:**  
`GET /seats/`

**Description:**  
Search for seats by optional filters.

**Query Parameters (optional):**
- `concert_id` (string) – Filter seats by concert ID.  
- `venue` (string) – Filter seats by venue.  

**Authentication:**  
❌ Not required.

**Response Model:**  
[`SeatResponse`](src/seats/model.py)

**Responses:**
- `200 OK` – Returns filtered list of seats.

---

## **Create Seats**

**Endpoint:**  
`POST /seats/`

**Description:**  
Create new seats for a concert or venue.

**Authentication:**  
✅ Required (`CurrentUser`).

**Request Body:**
- `seats` (list of [`Seat`](src/seats/model.py)) – List of seat objects to create.

**Responses:**
- `200 OK` – Seats successfully created.
- `400 Bad Request` – Invalid request payload.
- `401 Unauthorized` – If not authenticated.

---

## **Edit Seat**

**Endpoint:**  
`PUT /seats/edit/{seat_id}`

**Description:**  
Update details of an existing seat.

**Path Parameters:**
- `seat_id` (string) – Unique identifier for the seat.

**Authentication:**  
✅ Required (`CurrentUser`).

**Request Body:**
- `seat_update` ([`Seat`](src/seats/model.py)) – Updated seat details.

**Responses:**
- `200 OK` – Seat successfully updated.
- `400 Bad Request` – Invalid update request.
- `401 Unauthorized` – If not authenticated.
- `404 Not Found` – If seat does not exist.

---

## **Delete Seat**

**Endpoint:**  
`DELETE /seats/{seat_id}`

**Description:**  
Delete an existing seat by its ID.

**Path Parameters:**
- `seat_id` (string) – Unique identifier for the seat.

**Authentication:**  
✅ Required (`CurrentUser`).

**Responses:**
- `200 OK` – Seat successfully deleted.
- `401 Unauthorized` – If not authenticated.
- `404 Not Found` – If seat does not exist.

---

## Models

### **SeatResponse**
Represents a list of seats with metadata. Defined in `src/seats/model.py`.

---

### **Seat**
Represents a seat object. Defined in `src/seats/model.py`.

| Field        | Type     | Description                        |
|--------------|----------|------------------------------------|
| `id`         | string   | Unique seat identifier             |
| `concert_id` | string   | ID of the related concert          |
| `venue`      | string   | Venue name                         |
| `section`    | string   | Seat section                       |
| `row`        | string   | Seat row                           |
| `number`     | string   | Seat number                        |
| `status`     | string   | Availability status (available/booked/reserved) |
