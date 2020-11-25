## Authentication API

#### 1. Signup

- URL: `${BASE_URL}/auth/sign-up`
- Method: `POST`
- Header: `Content-Type: application/json`
- Request Body: `Json body`
- Response: `Json body`
- Status Code:
    + Signup success: `201`
    + Bad request: `400`
    + Internal server error: `500`

##### Ex. 
- Request
```text
curl --location --request POST '${BASE_URL}/auth/sign-up' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@yahoo.com",
    "password": "password123P!",
    "role": "Admin",
    "first_name": "John",
    "last_name": "Doe"
}'
```
- Response
```text
{
    "data": {
        "message": "Email sent!"
    },
    "error": false
}
```

#### 2. Signin

- URL: `${BASE_URL}/auth/sign-in`
- Method: `POST`
- Header: `Content-Type: application/json`
- Request Body: `Json body`
- Response: `Auth Token`
- Status Code:
    + Signin success: `200`
    + Bad request: `400`
    + Internal server error: `500`

##### Ex. 
- Request
```text
curl --location --request POST '${BASE_URL}/auth/sign-in' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@gmail.com",
    "password": "password123P!"
}'
```
- Response
```text
{
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDYzMzU3ODAsIm5iZiI6MTYwNjMzNTc4MCwianRpIjoiYWM4ODZhYWEtMGUzZC00YTI2LWE5MTItZTI2YWRlZjU2ZTA1IiwiZXhwIjoxNjA2OTQwNTgwLCJpZGVudGl0eSI6Im1hdGV1c2JwLnVwQGhvdG1haWwuY29tIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.gNdMt_imvceoB-6F78cvJstSqGCXo4BCf-QNotxjksk",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDYzMzU3ODAsIm5iZiI6MTYwNjMzNTc4MCwianRpIjoiNmMwODA4OWQtMjQ3YS00YjM5LTkyM2ItZWI1ODMzNjVhMjY4IiwiZXhwIjoxNjA4OTI3NzgwLCJpZGVudGl0eSI6Im1hdGV1c2JwLnVwQGhvdG1haWwuY29tIiwidHlwZSI6InJlZnJlc2gifQ.9Bc5cJtwbHJs3mpaTGC8xkNbbViaNeofyK2PzizYL8g"
    },
    "error": false
}
```