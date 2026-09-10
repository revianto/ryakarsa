---
name: apitester
description: Interact with Olsera's internal API Tester (apitester.staging.indociti.com) — list collections, browse folders/requests, view environments, create/update/delete requests and folders, and run ad-hoc HTTP requests through its server-side proxy. Use when the user asks about API Tester collections, requests, environments, or wants to run/check an API test there.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash(~/.agents/skills/apitester/scripts/*.sh *)
  - Bash(cat *)
---

# /apitester — Olsera API Tester

Talks to API Tester's internal REST API (`https://apitester.staging.indociti.com/api/v1/*`)
using a JWT access token the user obtains by logging in themselves. Claude never sees the
user's API Tester password.

## Session handling — read first

All API calls go through `~/.agents/skills/apitester/scripts/api.sh`, which reads the token
file at `~/.config/apitester-skill/token.json`.

- If a call fails with `NOT_LOGGED_IN` or `SESSION_EXPIRED`: **stop and tell the user** to run
  this themselves, in their own terminal (not via your Bash tool — the script reads their
  password with a hidden prompt, and it must never be typed into chat or run by you on their
  behalf):

  ```
  bash ~/.agents/skills/apitester/scripts/login.sh
  ```

  Wait for them to confirm before retrying the API call.
- Never ask the user to paste their password or access token into chat. If they do anyway,
  treat it as sensitive: don't echo it back.

## Core concepts

- **Collection** → **Folder** (nestable via `parent_folder_id`) → **Request**. A collection
  can also have **Environments**, each holding key/value **variables** used as `{{key}}`
  placeholders inside request URLs/headers/bodies (e.g. `{{url}}/{{domain}}`).
- To find a collection's `id` from a name, use:
  ```
  bash ~/.agents/skills/apitester/scripts/resolve_collection.sh "<partial collection name>"
  ```
  If more than one match, ask the user which one they mean.

## Handling secrets — read before touching environments

Environment variables routinely hold **real staging credentials** (JWT bearer tokens seen
in the wild look like `"key":"bearer","value":"Bearer eyJhbGc..."`, but any key named
`token`/`bearer`/`secret`/`password`/`auth`/`key` should be treated the same way):

- **Never print a variable's raw value in chat** when its key name suggests a credential.
  Summarize instead ("environment `Production Akar Gemilang` has a `bearer` variable set,
  value withheld").
- Non-secret variables (e.g. `url`, `domain`) are fine to show as-is.
- This applies to any endpoint that returns environment data, not just the one documented
  below.

## Preview before every write or execution (POST/PUT/DELETE, and running a request)

Never call `api.sh` with POST, PUT, or DELETE — or execute a request via the proxy — as your
first move. Always:

1. Gather the data needed (resolve collection/folder, fetch existing request if
   editing/deleting).
2. Show the user a **preview block** of exactly what will happen, e.g.:

   ```
   Akan membuat request baru:
     Collection: Toko Mobile V2
     Folder:     General > Shipping
     Name:       Get shipping rate
     Method:     GET
     URL:        {{url}}/en/{{domain}}/shipping/rate

   Lanjutkan?
   ```
   For delete: show the request/folder's name and method — make clear it's permanent.
   For **running a request** (via the proxy, see below): if the method is POST/PUT/DELETE/
   PATCH, warn explicitly that this sends a real request to the target API and may cause real
   side effects on that system (e.g. creating an order) — GET/HEAD requests are lower-risk and
   don't need this extra warning, but still show what's about to be called.
3. Wait for the user's explicit go-ahead in chat.
4. Only after confirmation, run the actual write/execute call.

This applies every time, not just the first time in a session.

## Operations

All calls: `bash ~/.agents/skills/apitester/scripts/api.sh <METHOD> <path> [json-body]`

### List collections
```
api.sh GET "/api/v1/collections"
```
Returns `{"data":[...], "metadata":{...}}` — each item has `id`, `name`, `description`,
`owner_name`, `permission` (`owner`/etc.), `team_id`.

### Get one collection (folders + requests tree)
```
api.sh GET "/api/v1/collections/<id>"
```
Returns `{"collection":{...}, "folders":[{id, name, parent_folder_id, sort_order}, ...],
"requests":[{id, name, method, url, folder_id, sort_order}, ...], "user_permission":"..."}`.
`folders`/`requests` are flat lists — reconstruct the tree via `parent_folder_id`/`folder_id`
(root items have `folder_id`/`parent_folder_id` = `null`).

### List environments for a collection
```
api.sh GET "/api/v1/collections/<id>/environments"
```
Returns an array of `{id, name, variables:[{key, value}, ...]}`. **Apply the secret-redaction
rule above before showing this to the user.**

### Get one request's full detail
```
api.sh GET "/api/v1/requests/<id>"
```
Returns `{"request":{id, name, method, url, headers, params, body, body_type, auth,
folder_id, description, pre_request_script, test_script, ...}, "sample_responses":[...]}`.

### Create a request
```
api.sh POST "/api/v1/collections/<id>/requests" '{"name":"<name>","method":"GET","url":"<url>", ...}'
```
Required: `name`, `method`. Optional: `url`, `folder_id` (put it inside a folder instead of
root), `headers`, `params`, `body`, `body_type`, `description`, `auth`.

### Update a request
```
api.sh PUT "/api/v1/requests/<id>" '{"name":"<name>","method":"GET","url":"<url>", ...}'
```
Send the fields you're changing; fields you omit are left as-is (observed behavior — verify
by re-fetching the request after a partial update if the exact merge semantics matter for
what you're doing).

### Delete a request
```
api.sh DELETE "/api/v1/requests/<id>"
```
**Permanent.** Returns `{"id":<id>,"success":true}`. Always confirm the request's name/method
with the user first (see Preview section).

### Create a folder
```
api.sh POST "/api/v1/collections/<id>/folders" '{"name":"<name>","parent_folder_id":null}'
```
Omit or set `parent_folder_id` to `null` for a root-level folder.

### Delete a folder
```
api.sh DELETE "/api/v1/folders/<id>"
```
**Permanent** — deleting a folder likely orphans or cascades to requests inside it (not
verified which). Confirm with the user and check the folder's contents first via the
collection detail endpoint.

### Run an ad-hoc HTTP request (the "Send" button)
```
api.sh POST "/api/v1/proxy" '{"method":"GET","url":"<url>","headers":{},"params":{},"body":null}'
```
This is executed **server-side** (the API Tester backend makes the call, not the browser/your
shell) — so it works even for staging APIs that block your IP or need internal network access.
`headers`/`params` must be **objects** (`{"Key":"Value"}`), not arrays — sending an array
fails with a 406 validation error. `body` is a raw string (or `null`) — for JSON bodies,
stringify it yourself and set an appropriate `Content-Type` header.

Response: `{"data":{"status":200,"status_text":"200 OK","headers":{...},"body":"<raw
string>","body_parsed":<parsed JSON if applicable>,"content_type":"...","elapsed_ms":123,
"size":273}}`.

**Resolving `{{variable}}` placeholders**: this endpoint does NOT resolve `{{url}}`-style
placeholders itself — if a saved request uses them, fetch the collection's environments
first (see above), substitute the values into `method`/`url`/`headers`/`params`/`body`
yourself before calling `/api/v1/proxy`. Never substitute a redacted secret value without
having actually read it from the environments call in this same turn (i.e. don't guess).

## Example flow

User: "lihat request apa aja di collection Toko Mobile V2, folder Shipping"
1. `resolve_collection.sh "toko mobile"` → get collection `id`.
2. `api.sh GET "/api/v1/collections/<id>"` → find folder `Shipping`'s `id` in `folders`,
   then filter `requests` where `folder_id` matches.

User: "jalankan request Get customer deposit Show pakai environment Production Akar Gemilang"
1. Fetch the request detail (`GET /api/v1/requests/<id>`) and the collection's environments.
2. Substitute `{{url}}`/`{{domain}}`/etc. in the request's URL/headers using the matching
   environment's variables.
3. Show the preview (method, resolved URL, note if a secret variable is being used —
   without printing its value) and get confirmation.
4. `api.sh POST "/api/v1/proxy" '{"method":"...","url":"...","headers":{...}, ...}'` →
   summarize the result (status, elapsed_ms, body preview).
