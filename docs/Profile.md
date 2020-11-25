## Profile API

#### 1. Get profile

- URL: `${BASE_URL}/profile`
- Method: `GET`
- Authentication: `Bearer ${ACCESS_TOKEN}`
- Header: `None`
- Request Body: `None`
- Response: `Profile data`
- Status Code:
    + Succsss: `200`
    + Entity not exist: `404`
    + Internal server error: `500`

##### Ex. 
- Request
```text
curl --location --request GET '${BASE_URL}/profile' \
--header 'Authorization: Bearer ${ACCESS_TOKEN}'
```
- Response
```text
{
    "data": {
        "email": "joe.biden@hotmail.com",
        "first_name": "Joe",
        "id": 1,
        "last_name": "Biden",
        "phone_number": null,
        "role": "User",
        "verified": true
    },
    "error": false
}
```

#### 2. Update

- URL: `${BASE_URL}/profile`
- Method: `PUT`
- Authentication: `Bearer ${ACCESS_TOKEN}`
- Header: `Content-Type: application/json`
- Request Body: `json body`
- Response: Profile
- Status Code:
    + Succsss: `200`
    + Entity not exist: `404`
    + Internal server error: `500`

##### Ex. 
- Request
```text
curl --location --request PUT '${BASE_URL}/profile' \
--header 'Authorization: Bearer ${ACCESS_TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "email": "donald.trump@hotmail.com",
  "first_name": "Donald",
  "last_name": "Trump",
  "phone_number": "207-731-8826",
  "role": "Admin"
}'
```
- Response
```text
{
    "data": {
        "email": "donald.trump@hotmail.com",
        "first_name": "Donald",
        "id": 1,
        "last_name": "Trump",
        "phone_number": "207-731-8826",
        "role": "Admin",
        "verified": true
    },
    "error": false
}
```

#### 3. Password Reset

- URL: `${BASE_URL}/profile/password-reset`
- Method: `PUT`
- Authentication: `Bearer ${ACCESS_TOKEN}`
- Header: `Content-Type: application/json`
- Request Body: `json body`
- Response: success message
- Status Code:
    + Succsss: 200
    + Bad request: 400
    + Entity not exist: 404
    + Internal server error: 500

##### Ex. 
- Request
```text
curl --location --request GET '${BASE_URL}/profile/password-reset' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer ${ACCESS_TOKEN}' \
--data-raw '{
    "email": "donald.trump@yhotmail.com",
    "current_password": "password123P!",
    "new_password": "newpwd123P!"
}'
```
- Response
```text
{
    "message": "Password reset success!"
}
```