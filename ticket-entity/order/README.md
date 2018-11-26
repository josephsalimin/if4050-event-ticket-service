## Order REST Service

### Info
- Must include Header Authentication Token
- Must JSON

### Routing

#### /order/
- Method: POST
- Body
```json5
{
  "user_id": "your_user_id",
  "total_price": "total_price",
  "section_list": [
    {
      "id": "section_id",
      "quantity": "ticket_quantity"
    }
  ]
}
```
- Output
```json5
{
  "id": "order_id",
  "user_id": "your_user_id",
  "total_price": "total_price",
  "status": "order_status"
}
```

#### /order/<order_id>
- Method: PUT
- Output
```json5
[
  {
    "id": "section_id",
    "quantity": "ticket_quantity"
  }
]
```

#### /order/<order_id>
- Method: DELETE
- Output
```json5
[
  {
    "id": "section_id",
    "quantity": "ticket_quantity"
  }
]
```

#### /order/<order_id>
- Method: GET
- Output
```json5
{
  "id": "order_id",
  "user_id": "your_user_id",
  "total_price": "total_price",
  "status": "order_status"
}
```

#### /order/user
- Method: GET
- Parameter
```
- id [MUST]
```
- Output
```json5
[
  {
    "user_id": "your_user_id",
    "total_price": "total_price",
    "status": "order_status",
  }
 ]
```