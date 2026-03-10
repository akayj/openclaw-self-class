# Feishu Calendar API Notes

## Gotchas

1. **Attendees must be added separately** — Creating an event with `attendees` in the body does NOT work. Must POST to `/calendar/v4/calendars/{cal_id}/events/{event_id}/attendees` after creation.

2. **attendee_ability defaults to "none"** — This hides participants from each other. Always set to `"can_see_others"` when creating events.

3. **Bot cannot DM users who haven't chatted with it** — Error 230013. Use group chat mentions instead.

4. **Name search needs user_access_token** — `POST /search/v1/user` requires user identity, not tenant identity. Use email-based lookup (`POST /contact/v3/users/batch_get_id`) as fallback.

5. **Contacts scope** — batch_get_id only returns users within the app's contact scope. If a user isn't found, they may be outside the scope (admin must expand it).

## API Endpoints

- **Auth**: `POST /open-apis/auth/v3/tenant_access_token/internal`
- **Create event**: `POST /open-apis/calendar/v4/calendars/{cal_id}/events`
- **Delete event**: `DELETE /open-apis/calendar/v4/calendars/{cal_id}/events/{event_id}`
- **Update event**: `PATCH /open-apis/calendar/v4/calendars/{cal_id}/events/{event_id}`
- **Add attendees**: `POST /open-apis/calendar/v4/calendars/{cal_id}/events/{event_id}/attendees`
- **Remove attendee**: `DELETE` with attendee_id in body
- **List events**: `GET /open-apis/calendar/v4/calendars/{cal_id}/events?start_time=&end_time=`
- **Lookup user**: `POST /open-apis/contact/v3/users/batch_get_id`

## Timestamp Format

All timestamps are Unix seconds (string). Timezone specified separately as `"Asia/Shanghai"`.
