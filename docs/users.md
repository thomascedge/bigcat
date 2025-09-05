# Users API Documentation

## Base Path
```
/users
```

All endpoints in this router are prefixed with `/users`.

---

## **Get Current User**

**Endpoint:**  
```
GET /users/me
```

**Description:**  
Fetch the details of the currently authenticated user.

**Authentication:**  
✅ Requires authentication (the current user is resolved via `CurrentUser` dependency).  

**Response Model:**  
[`UserResponse`](src/users/model.py)  

**Response Example (200 OK):**
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "created_at": "2025-09-05T12:00:00Z"
}
```

**Error Codes:**
- `401 Unauthorized` – if the user is not authenticated.
- `404 Not Found` – if the user does not exist in the database.

---

## **Change Password**

**Endpoint:**  
```
PUT /users/change-password
```

**Description:**  
Update the authenticated user’s password.

**Authentication:**  
✅ Requires authentication.  

**Request Body:**  
[`PasswordChange`](src/users/model.py)

Example:
```json
{
  "old_password": "string",
  "new_password": "string"
}
```

**Responses:**
- `200 OK` – Password successfully updated.
- `400 Bad Request` – Invalid input (e.g., incorrect old password).
- `401 Unauthorized` – If the user is not authenticated.

---

## Models

### **User**
Represents a user’s public profile. Defined in `src/users/model.py`.

| Field          | Type     | Description                   |
|----------------|----------|-------------------------------|
| `uid`          | string   | Unique identifier of the user |
| `first_name`   | string   | The user’s first name         |
| `last_name`    | string   | The user’s last name          |
| `email`        | string   | The user’s email address      |
| `password_hash`| string   | The user’s email address      |



### **UserResponse**
Represents a user response. Defined in `src/users/model.py`.

| Field          | Type     | Description                   |
|----------------|----------|-------------------------------|
| `uid`          | string   | Unique identifier of the user |
| `first_name`   | string   | The user’s first name         |
| `last_name`    | string   | The user’s last name          |
| `email`        | string   | The user’s email address      |

---

### **PasswordChange**
Represents the payload required to change a user’s password. Defined in `src/users/model.py`.

| Field                  | Type   | Description                   |
|------------------------|--------|-------------------------------|
| `current_password`.    | string | Current password              |
| `new_password`         | string | New password to set           |
| `new_password_confirm` | string | New password to set           |