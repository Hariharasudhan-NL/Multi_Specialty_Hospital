# Failure Cases

1. **Stale Data**: Bed status not updated for >60 mins. System shows `DATA_STALE`.
2. **Conflict**: Cleaning marked complete but bed is still occupied. System flags `CONFLICT`.
3. **Network Disconnect**: WebSocket drops. System attempts reconnect and shows offline banner.
4. **Invalid Input**: Future timestamps. Rejected as `INVALID`.
5. **Duplicate Event**: Same event logged twice. Flagged as `DUPLICATE`.
6. **Missing Order**: Readiness confirmed but no discharge order. Shows `ORDER_PENDING`.
7. **No Exit**: Cleaning started before patient exit. Shows warning.
8. **Unauthorized Access**: Role-based access violation. Returns 401/403.
