## Ticket REST Service

### Info
- Must include Header Authentication Token
- Must JSON

### Routing

#### /ticket_section/
- Method: POST
- Body
```json5
{
  "event_id": "event_id",
  "section_list": [
    {
      "name": "section_name",
      "price": "section_price",
      "capacity": "section_capacity",
      "has_seat": "boolean"
    }
  ]
}
```
- Output
```json5
true
```

#### /ticket_section/event?
- Method: GET
- Parameter
```
- id [MUST]
```
- Output
```json5
[
  {
    "name": "section_name",
    "price": "section_price",
    "capacity": "section_capacity",
    "has_seat": "boolean"
  }
]
```

#### /ticket_section/validation
- Method: POST
- Input
```json5
{
  "section_list": [
    {
      "id": "section_id",
      "quantity": "section_quantity",
    }
  ]
}
```
- Output
```json5
true
```

#### /ticket_section/<section_id>
- Method: GET
- Output
```json5
{
  "name": "section_name",
  "price": "section_price",
  "capacity": "section_capacity",
  "has_seat": "boolean"
}
```

#### /ticket_section/reduce
- Method: POST
- Input
```json5
{
  "section_list": [
    {
      "id": "section_id",
      "quantity": "section_quantity",
    }
  ]
}
```
```
- Output
```json5
true
```

#### /ticket_section/add
- Method: POST
- Input
```json5
{
  "section_list": [
    {
      "id": "section_id",
      "quantity": "section_quantity",
    }
  ]
}
```
- Output
```json5
true
```

#### /ticket/
- Method: POST
- Input
```json5
{
  "order_id": "order_id",
  "section_list": [
    {
      "id": "section_id",
      "quantity": "section_quantity",
    }
  ]
}
```
- Output
```json5
[
  {
    "order_id": "order_id",
    "section": {
      "name": "section_name",
      "price": "section_price",
      "capacity": "section_capacity",
      "has_seat": "boolean"
    }
  }
]
```

#### /ticket/remove
- Method: DELETE
- Input
```json5
{
  "order_id": "order_id"
}
```
- Output
```json5
true
```

#### /ticket/<ticket_id>
- Method: GET
- Output
```json5
{
  "order_id": "order_id",
  "section": {
    "name": "section_name",
    "price": "section_price",
    "capacity": "section_capacity",
    "has_seat": "boolean"
  }
}
```

#### /ticket/order?
- Method: GET
- Parameter
```
- id [MUST]
```
- Output
```json5
[
  {
    "order_id": "order_id",
    "section": {
      "name": "section_name",
      "price": "section_price",
      "capacity": "section_capacity",
      "has_seat": "boolean"
    }
  }
]
```