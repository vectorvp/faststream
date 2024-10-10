from faststream.response import Response, ensure_response


def test_raw_data() -> None:
    resp = ensure_response(1)
    assert resp.body == 1
    assert resp.headers == {}


def test_response_with_response_instance() -> None:
    resp = ensure_response(Response(1, headers={"some": 1}))
    assert resp.body == 1
    assert resp.headers == {"some": 1}


def test_headers_override() -> None:
    resp = Response(1, headers={"some": 1})
    resp.add_headers({"some": 2})
    assert resp.headers == {"some": 2}


def test_headers_with_default() -> None:
    resp = Response(1, headers={"some": 1})
    resp.add_headers({"some": 2}, override=False)
    assert resp.headers == {"some": 1}
