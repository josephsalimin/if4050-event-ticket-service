## Partner REST Service

### Info
- Must include Header Authentication Token
- Must JSON

### Routing

#### /partner/
- Method: POST
- Body
```json5
{
  "name": "your_name",
  "address": "your_address",
  "email": "your_email",
  "contact_number": "your_contact_number"
}
```
- Output
```json5
{
  "name": "your_name",
  "address": "your_address",
  "email": "your_email",
  "contact_number": "your_contact_number"
}
```

#### /partner/
- Method: GET
- Parameter
```
- name [OPTIONAL] 
```
- Output
```json5
[
  {
    "name": "your_name",
    "address": "your_address",
    "email": "your_email",
    "contact_number": "your_contact_number"
  }
]
```

#### /partner/<partner_id>
- Method: GET
- Output
```json5
{
  "name": "your_name",
  "address": "your_address",
  "email": "your_email",
  "contact_number": "your_contact_number"
}
```

#### /user/<partner_id>
- Method: PUT
- Body
```json5
{
  "name": "your_name",
  "address": "your_address",
  "email": "your_email",
  "contact_number": "your_contact_number"
}
```
-Output
```json5
{
  "name": "your_name",
  "address": "your_address",
  "email": "your_email",
  "contact_number": "your_contact_number"
}
```