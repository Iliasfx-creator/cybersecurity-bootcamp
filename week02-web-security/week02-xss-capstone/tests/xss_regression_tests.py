from __future__ import annotations

import sys
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import (
    HTTPRedirectHandler,
    Request,
    build_opener,
    urlopen,
)

BASE_URL = "http://127.0.0.1:8005"
MARKER = "<b>test-marker</b>"
ESCAPED_MARKER = "&lt;b&gt;test-marker&lt;/b&gt;"


class NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def get(path: str) -> tuple[int, str, dict[str, str]]:
    try:
        with urlopen(BASE_URL + path, timeout=5) as response:
            body = response.read().decode("utf-8")
            return response.status, body, dict(response.headers)
    except HTTPError as error:
        body = error.read().decode("utf-8")
        return error.code, body, dict(error.headers)


def post_without_redirect(
    path: str,
    form_data: dict[str, str],
) -> tuple[int, str, dict[str, str]]:
    encoded_data = urlencode(form_data).encode("utf-8")

    request = Request(
        BASE_URL + path,
        data=encoded_data,
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    opener = build_opener(NoRedirectHandler())

    try:
        with opener.open(request, timeout=5) as response:
            body = response.read().decode("utf-8")
            return response.status, body, dict(response.headers)
    except HTTPError as error:
        body = error.read().decode("utf-8")
        return error.code, body, dict(error.headers)


def extract_section(body: str, element_id: str) -> str:
    start_marker = f'<ul id="{element_id}">'
    end_marker = "</ul>"

    start = body.find(start_marker)
    if start == -1:
        raise AssertionError(f"Section not found: {element_id}")

    end = body.find(end_marker, start)
    if end == -1:
        raise AssertionError(f"Closing tag not found: {element_id}")

    return body[start:end]


def run_test(name: str, function) -> bool:
    try:
        function()
        print(f"[PASS] {name}")
        return True
    except Exception as error:
        print(f"[FAIL] {name}: {error}")
        return False


def test_home_returns_200() -> None:
    status, body, _ = get("/")
    assert status == 200, f"Expected 200, received {status}"
    assert "XSS Capstone" in body


def test_reflected_vulnerable_contains_raw_marker() -> None:
    path = "/reflected-vuln?q=%3Cb%3Etest-marker%3C%2Fb%3E"
    status, body, _ = get(path)

    assert status == 200
    assert MARKER in body


def test_reflected_safe_contains_escaped_marker() -> None:
    path = "/reflected-safe?q=%3Cb%3Etest-marker%3C%2Fb%3E"
    status, body, _ = get(path)

    assert status == 200
    assert ESCAPED_MARKER in body
    assert f"You searched for: {MARKER}" not in body


def test_comment_post_redirects() -> None:
    status, _, headers = post_without_redirect(
        "/comments",
        {"comment": MARKER},
    )

    assert status == 303, f"Expected 303, received {status}"
    assert headers.get("Location") == "/comments"


def test_comments_page_returns_200() -> None:
    status, body, _ = get("/comments")

    assert status == 200
    assert "Vulnerable comments" in body
    assert "Safe comments" in body


def test_stored_vulnerable_section_contains_raw_marker() -> None:
    _, body, _ = get("/comments")
    vulnerable_section = extract_section(body, "vulnerable-comments")

    assert MARKER in vulnerable_section


def test_stored_safe_section_contains_escaped_marker() -> None:
    _, body, _ = get("/comments")
    safe_section = extract_section(body, "safe-comments")

    assert ESCAPED_MARKER in safe_section
    assert MARKER not in safe_section


def test_dom_page_contains_both_sinks() -> None:
    status, body, _ = get("/dom")

    assert status == 200
    assert ".innerHTML" in body
    assert ".textContent" in body
    assert "URLSearchParams" in body


def test_unknown_route_returns_404() -> None:
    status, _, _ = get("/not-found")
    assert status == 404


def main() -> int:
    tests = [
        ("Home route returns 200", test_home_returns_200),
        (
            "Reflected vulnerable response contains raw marker",
            test_reflected_vulnerable_contains_raw_marker,
        ),
        (
            "Reflected safe response contains escaped marker",
            test_reflected_safe_contains_escaped_marker,
        ),
        ("Comment POST returns redirect", test_comment_post_redirects),
        ("Comments page returns 200", test_comments_page_returns_200),
        (
            "Stored vulnerable section contains raw marker",
            test_stored_vulnerable_section_contains_raw_marker,
        ),
        (
            "Stored safe section contains escaped marker",
            test_stored_safe_section_contains_escaped_marker,
        ),
        (
            "DOM page contains vulnerable and safe sinks",
            test_dom_page_contains_both_sinks,
        ),
        ("Unknown route returns 404", test_unknown_route_returns_404),
    ]

    results = [run_test(name, function) for name, function in tests]

    passed = sum(results)
    failed = len(results) - passed

    print()
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
