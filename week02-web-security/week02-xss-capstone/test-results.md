# Test Results

## Test command

```bash
python3 week02-web-security/week02-xss-capstone/tests/xss_regression_tests.py
Result
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
Methodology

The tests use only Python standard-library modules.

HTTP GET requests verify status codes and response bodies.

A custom redirect handler prevents the client from automatically following the comment POST redirect, allowing the 303 response and Location header to be checked directly.

The reflected tests compare raw and escaped rendering of the same marker.

Each stored rendering test creates the comment state that it requires before requesting the comments page.

The stored sections are examined separately so raw rendering in the intentionally vulnerable section does not create a false result for the safe section.

Exit behavior

The test process returns exit code 0 when all checks pass.

It returns a non-zero exit code when one or more checks fail.

This makes the test file suitable for future continuous-integration use.

Limitations

The server must already be running on 127.0.0.1:8005.

The suite checks response content but does not run a real browser.

It confirms that the DOM page contains URLSearchParams, innerHTML, and textContent, but it does not execute JavaScript.

Actual DOM execution was therefore verified separately in a browser and documented in evidence/dom_browser_summary.txt.

The test server stores comments only in memory, so its state disappears when the process restarts.
