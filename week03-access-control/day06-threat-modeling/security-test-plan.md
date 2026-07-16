
Security Test Plan
Approach

Each high-risk flow receives positive and negative testing.

For denied mutations, verification includes both the HTTP response and a
second read from trusted test setup to confirm that state did not change.

Test	Threats	Actor and setup	Action	Expected secure result
ST-01	T-01	Tenant-A user, tenant-B document	Request the foreign document ID	Same concealed denial as nonexistent object; no properties disclosed
ST-02	T-02	Tenant-A user, tenant-B document/file	Update and delete foreign object	Denied; database and storage hashes remain unchanged
ST-03	T-03	Normal user update	Add tenant, owner, role and support properties	Sensitive properties rejected or ignored; trusted values unchanged
ST-04	T-04	User with limited read permission	Inspect complete API response	Restricted properties absent
ST-05	T-05	Normal tenant user	Directly invoke organization export	Denied; no job, output or download created
ST-06	T-06	User and tenant administrator	Invoke support-admin operation	Denied for both; no target state change
ST-07	T-07	Valid session followed by logout/revocation	Replay the old session	Authentication fails
ST-08	T-08	Active tenant-admin session	Downgrade role, then create invitation/export	Existing session immediately loses privileged access
ST-09	T-09	Valid invitation fixture	Change binding, replay, revoke and expire token	Every invalid acceptance fails; membership remains absent
ST-10	T-10	Lower-privileged actor	Repeat denied v2 actions through v1	Equivalent denial or v1 unavailable
ST-11	T-11	Authorized and denied privileged actions	Inspect audit records and attempt mutation	Complete attribution exists; unauthorized log mutation fails
ST-12	T-12	Authenticated tenant user	Exceed quotas and concurrency limits	Controlled limit response; bounded work and stable service
ST-13	T-13	Tenant-A user	Supply tenant B in header, query and body separately	Tenant context remains A; foreign object access denied
ST-14	T-14	Authorized download followed by expiry	Reuse URL for another object/method or after expiry	Storage denies every out-of-scope or expired request
Routing discrepancy tests

For every privileged endpoint:

Test /api/v1 and /api/v2.
Test allowed and unsupported HTTP methods.
Test trailing slash and normalized route variants.
Test duplicate and conflicting tenant parameters.
Confirm gateway and backend interpret the same path.
Confirm endpoint authorization is not dependent on Referer.
Evidence requirements

Evidence should include:

actor role and tenant fixture,
sanitized request,
response status and relevant body,
before-and-after object state,
audit-event identifier where applicable,
API version and method,
test result.

Any example containing authentication material must use:

Cookie: session=REDACTED
Password: REDACTED
Regression triggers

The threat model and tests must be reviewed when:

a role or permission changes,
a new API version or endpoint is introduced,
document sharing is added,
storage-download behavior changes,
a new external provider is added,
session or invitation formats change,
export scope changes,
a tenant identifier is added to any request schema.
