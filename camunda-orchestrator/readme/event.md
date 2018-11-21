## Event REST Service

### Info
- Must include Header Authentication Token
- Must JSON

### Routing

#### /event/
- Method: POST
- Body
```json5
{
  "partner_id": "your_partner_id",
  "name": "event_name",
  "description": "event_description",
  "location": "event_location",
  "start_at": "event_start_time",
  "end_at": "event_end_time"
}
```
- Output
```json5
{
  "partner_id": "your_partner_id",
  "name": "event_name",
  "description": "event_description",
  "location": "event_location",
  "start_at": "event_start_time",
  "end_at": "event_end_time"
}
```

#### /event/<event_id>
- Method: PUT
- Body
```json5
{
  "partner_id": "your_partner_id",
  "name": "event_name",
  "description": "event_description",
  "location": "event_location",
  "start_at": "event_start_time",
  "end_at": "event_end_time"
}
```
- Output
```json5
{
  "partner_id": "your_partner_id",
  "name": "event_name",
  "description": "event_description",
  "location": "event_location",
  "start_at": "event_start_time",
  "end_at": "event_end_time"
}
```

#### /event/<event_id>
- Method: GET
- Output
```json5
{
  "partner_id": "your_partner_id",
  "name": "event_name",
  "description": "event_description",
  "location": "event_location",
  "start_at": "event_start_time",
  "end_at": "event_end_time"
}
```

### /event/history
- Method: GET
- Output
```json5
[
  {
    "partner_id": "your_partner_id",
    "name": "event_name",
    "description": "event_description",
    "location": "event_location",
    "start_at": "event_start_time",
    "end_at": "event_end_time"
  }
]
```

### /event/available
- Method: GET
- Output
```json5
[
  {
    "partner_id": "your_partner_id",
    "name": "event_name",
    "description": "event_description",
    "location": "event_location",
    "start_at": "event_start_time",
    "end_at": "event_end_time"
  }
]
```

#### /event/partner
- Method: GET
- Parameter
```
- id [MUST]
```
- Output
```json5
[
  {
    "partner_id": "your_partner_id",
    "name": "event_name",
    "description": "event_description",
    "location": "event_location",
    "start_at": "event_start_time",
    "end_at": "event_end_time"
  }
]
```



