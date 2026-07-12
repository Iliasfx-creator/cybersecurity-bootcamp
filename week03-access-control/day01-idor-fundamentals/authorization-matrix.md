# Authorization Matrix

## Read and update decisions

| Actor | Resource | Action | Vulnerable result | Safe result | Expected result |
|---|---|---|---|---|---|
| Alice | Alice document 101 | Read | Allowed | Allowed | Allowed |
| Alice | Alice document 101 | Update | Allowed | Allowed | Allowed |
| Alice | Bob document 201 | Read | Incorrectly allowed | Denied with 404 | Denied |
| Alice | Bob document 201 | Update | Incorrectly allowed | Denied with 404 | Denied |
| Bob | Bob document 201 | Read | Allowed | Allowed | Allowed |
| Bob | Bob document 201 | Update | Allowed | Allowed | Allowed |
| Bob | Alice document 101 | Read | Incorrectly allowed | Denied with 404 | Denied |
| Bob | Alice document 101 | Update | Incorrectly allowed | Denied with 404 | Denied |
| Anonymous | Any document | Read | Denied with 401 | Denied with 401 | Denied |
| Anonymous | Any document | Update | Denied with 401 | Denied with 401 | Denied |
| Alice | Invalid identifier | Read | Denied with 400 | Denied with 400 | Denied |
| Alice | Missing document 999 | Read | Denied with 404 | Denied with 404 | Denied |

## Vulnerable request flow

The vulnerable endpoints perform:

```text
1. Check for an authenticated session.
2. Validate the document ID.
3. Retrieve the document by ID.
4. Return or update the document.
```

The ownership check is missing.

## Safe request flow

The safe endpoints perform:

```text
1. Check for an authenticated session.
2. Validate the document ID.
3. Retrieve the document by ID.
4. Compare the document owner with the authenticated user.
5. Perform the read or update only when authorized.
```

The essential rule is:

```python
document["owner"] == current_user
```

## Response policy

The application uses:

| Condition | Response |
|---|---|
| Missing or invalid session | `401 Unauthorized` |
| Malformed identifier | `400 Bad Request` |
| Missing document | `404 Not Found` |
| Foreign document on safe route | `404 Not Found` |
| Authorized operation | `200 OK` |

The safe endpoints intentionally return the same `404` response for nonexistent and foreign documents.

This avoids confirming whether another user's resource exists.
