# Test Results

## Test command

```bash
python3 week02-web-security/week02-xss-capstone/tests/xss_regression_tests.py
```

## Result

```text
[PASS] Home route returns 200
[PASS] Reflected vulnerable response contains raw marker
[PASS] Reflected safe response contains escaped marker
[PASS] Comment POST returns redirect
[PASS] Comments page returns 200
[PASS] Stored vulnerable section contains raw marker
[PASS] Stored safe section contains escaped marker
[PASS] DOM page contains vulnerable and safe sinks
[PASS] Unknown route returns 404

Passed: 9
Failed: 0
```

## Methodology

The tests use only Python standard-library modules.

HTTP GET requests verify status codes and response bodies.

A custom redirect handler prevents the client from automatically following the comment POST redirect. This allows the test to inspect the original `303` response and its `Location` header.

The reflected tests compare raw and escaped rendering of the same marker.

Each stored rendering test submits its own marker before requesting the comments page. The rendering tests therefore do not depend on the execution order of the suite.

The vulnerable and safe stored sections are extracted and checked separately.

## Exit behavior

The test process exits with code `0` when all checks pass.

It returns a non-zero code when one or more checks fail.

## Limitations

The application server must already be running on `127.0.0.1:8005`.

The suite checks HTTP responses but does not execute JavaScript in a real browser.

It confirms that the DOM page contains `URLSearchParams`, `innerHTML`, and `textContent`, but browser execution is verified separately in `evidence/dom_browser_summary.txt`.

Comments are stored only in memory and disappear when the server restarts.
