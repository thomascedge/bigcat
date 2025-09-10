# Authentication API

This module provides authentication endpoints for user registration and login, built with [FastAPI](https://fastapi.tiangolo.com/), MongoDB, and OAuth2.

## Base Path
```
/auth
```

---

## Endpoints

### **POST** `/auth/`

Register a new user.  
This endpoint is **rate-limited to 5 requests per hour per client**.

#### Request Body
`application/json`

```json
{
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string"
}
```

*(Fields come from the `RegisterUserRequest` model.)*

#### Responses
- **201 Created** – User successfully registered.  
- **400 Bad Request** – Invalid input (e.g., user already exists, malformed request).  
- **429 Too Many Requests** – Rate limit exceeded.  

---

### **POST** `/auth/token`

Authenticate an existing user and receive an access token.  
Follows the OAuth2 password flow.

#### Request Body
`application/x-www-form-urlencoded`

```json
{
  "email": "string Required",
  "password": "string Required",
  "scope": "string"
}
```

#### Response
`application/json`

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

*(Matches the `Token` model.)*

#### Responses
- **200 OK** – Token successfully issued.  
- **401 Unauthorized** – Invalid credentials.  

---

## Models

### `RegisterUserRequest`
Represents the payload for registering a new user. Example fields:

```json
{
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string"
}
```

*(Confirm exact schema in `src/auth/model.py`.)*

---

### `Token`
Represents an authentication token returned upon successful login.

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

---

## Rate Limiting

- `POST /auth/` → **5 requests/hour per client**  
- `POST /auth/token` → no explicit rate limit defined  

---

## Dependencies

- **FastAPI** – Web framework  
- **MongoDB (pymongo)** – Database backend  
- **OAuth2PasswordRequestForm** – Standardized login form  
- **Authentication service** – Implemented in `src/auth/service.py`  
- **Rate limiting** – Implemented via `src/rate_limiting.py`

---

## Notes

- Tokens are issued using OAuth2 with bearer token format.  
- The database is injected via `Depends(get_database)` from `src.database.core`.  
- The authentication logic itself lives in `src/auth/service.py`.  
