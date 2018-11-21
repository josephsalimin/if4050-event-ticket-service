## User REST Service

### Info
- Company ID 1: owned by TicketX
- Must include Header Authentication Token
- Must JSON

### Routing

#### /user/
- Method: POST
- Body
```json5
{
  "username": "your_username",
  "fullname": "your_fullname",
  "email": "your_email",
  "password": "your_password",
  "address": "your_address"
}
```
- Output
```json5
{
  "username": "your_username",
  "fullname": "your_fullname",
  "email": "your_email",
  "password": "your_password",
  "address": "your_address",
  "company_id": "your_company_id"
}
```

#### /user/
- Method: GET
- Parameter
```
- username [OPTIONAL] 
- email [OPTIONAL]
```
- Output
```json5
[
  {
    "username": "your_username",
    "fullname": "your_fullname",
    "email": "your_email",
    "password": "your_password",
    "address": "your_address"
  }
]
```

#### /user/<user_id>
- Method: GET
- Output
```json5
{
  "username": "your_username",
  "fullname": "your_fullname",
  "email": "your_email",
  "password": "your_password",
  "address": "your_address"
}
```

#### /user/<user_id>
-Method: PUT
-Body
```json5
{
  "fullname": "your_fullname",
  "address": "your_address"
}
```
-Output
```json5
{
  "username": "your_username",
  "fullname": "your_fullname",
  "email": "your_email",
  "password": "your_password",
  "address": "your_address"
}
```