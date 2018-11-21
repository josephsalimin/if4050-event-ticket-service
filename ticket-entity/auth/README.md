## Authentication REST Service


### Info
- auth_type: partner, consumer
- partner_id only for partner, else input 0

### Routing

#### /auth/create
- Method: POST
- Body
```json5
{
  "name": "your_name",
  "type": "your_auth_type",
  "partner_id": "your_partner_id"
}
```
- Output
```json5
{
  "name": "your_name",
  "auth_type": "your_auth_type",
  "refresh_token": "your_refresh_token",
  "auth_token": "your_auth_token",
  "partner_id": "your_partner_id"
}
```

#### /auth/refresh
- Method: POST
- Body
```json5
{
  "name": "your_name",
  "refresh_token": "your_refresh_token",
}
```
- Output
```json5
{
  "name": "your_name",
  "auth_type": "your_auth_type",
  "refresh_token": "your_refresh_token",
  "auth_token": "your_auth_token",
  "partner_id": "your_partner_id"
}
```

#### /auth/verify
- Method: POST
- Body
```json5
{
  "auth_token" : "your_auth_token"
}
```
- Output
```json5
{
  "id": "your_auth_id",
  "auth_type": "your_auth_type",
  "partner_id": "your_partner_id",
  "valid": true
}
```