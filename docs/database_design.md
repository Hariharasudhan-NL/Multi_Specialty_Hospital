# Database Design

## ER Diagram (Text-based)
```
[User]
- id (PK)
- email
- role

[Patient]
- id (PK)
- name
- status

[Bed]
- id (PK)
- bed_code
- current_state

[DischargeEvent]
- id (PK)
- bed_id (FK)
- event_type
- timestamp
```
