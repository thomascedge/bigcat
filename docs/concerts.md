# Concerts API Documentation

## Base Path
```
/concerts
```

All endpoints in this router are prefixed with `/concerts`.

---

## **Get All Concerts**

**Endpoint:**  
```
GET /concerts/
```

**Description:**  
Retrieve all concerts.

**Authentication:**  
❌ Not required.

**Response Model:**  
[`ConcertResponse`](src/concerts/model.py)

**Responses:**
- `200 OK` – Returns a list of concerts.

---

## **Get Concert by ID**

**Endpoint:**  
```
GET /concerts/{concert_id}
```

**Description:**  
Fetch details of a specific concert by its ID.

**Path Parameters:**
- `concert_id` (string) – Unique concert identifier.

**Authentication:**  
❌ Not required.

**Response Model:**  
[`Concert`](src/concerts/model.py)

**Responses:**
- `200 OK` – Returns concert details.
- `404 Not Found` – If concert does not exist.

---

## **Search Concerts**

**Endpoint:**  
```
GET /concerts/search
```

**Description:**  
Search for concerts using filters.

**Query Parameters (all optional):**
- `concert_id` (string) – Filter by concert ID.  
- `artist` (string) – Filter by artist name.  
- `tour_name` (string) – Filter by tour name.  
- `venue` (string) – Filter by venue.  
- `location` (string) – Filter by location.  
- `date` (datetime) – Filter by date.  

**Authentication:**  
❌ Not required.

**Response Model:**  
[`ConcertResponse`](src/concerts/model.py)

**Responses:**
- `200 OK` – Returns matching concerts.

---

## **Create Concert**

**Endpoint:**  
```
POST /concerts/
```

**Description:**  
Create a new concert.  

**Authentication:**  
✅ Required (`CurrentUser`).  

**Request Body:**  
[`Concert`](src/concerts/model.py)

Example:
```json
{
  "id": "string",
  "artist": "string",
  "tour_name": "string",
  "venue": "string",
  "location": "string",
  "date": "2025-09-05T20:00:00Z"
}
```

**Responses:**
- `200 OK` – Concert successfully created.
- `401 Unauthorized` – If not authenticated.

---

## **Update Concert**

**Endpoint:**  
```
PATCH /concerts/{concert_id}
```

**Description:**  
Update details of an existing concert.

**Path Parameters:**
- `concert_id` (string) – Unique concert identifier.

**Authentication:**  
✅ Required (`CurrentUser`).  

**Request Body:**  
[`Concert`](src/concerts/model.py)

**Responses:**
- `200 OK` – Concert updated.
- `401 Unauthorized` – If not authenticated.
- `404 Not Found` – If concert does not exist.

---

## **Cancel Concert**

**Endpoint:**  
```
DELETE /concerts/{concert_id}
```

**Description:**  
Cancel (delete) a concert by its ID.

**Path Parameters:**
- `concert_id` (string) – Unique concert identifier.

**Authentication:**  
✅ Required (`CurrentUser`).  

**Responses:**
- `202 Accepted` – Concert successfully canceled.
- `401 Unauthorized` – If not authenticated.
- `404 Not Found` – If concert does not exist.

---

## Models

### **ConcertResponse**
Represents a list of concerts with metadata. Defined in `src/concerts/model.py`.

---

### **Concert**
Represents a concert object. Defined in `src/concerts/model.py`.

| Field       | Type     | Description                |
|-------------|----------|----------------------------|
| `id`        | string   | Unique concert identifier  |
| `artist`    | string   | Artist performing          |
| `tour_name` | string   | Name of the tour           |
| `venue`     | string   | Venue of the concert       |
| `location`  | string   | Location of the concert    |
| `date`      | datetime | Scheduled concert date     |
