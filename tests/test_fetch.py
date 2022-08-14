
import json

import pytest
import responses
from aisles.fetch import fetch_data_uncompressed
from requests import Session


@responses.activate
def test_fetch_data_uncompressed():
    responses.add(
        responses.GET,
        "http://test123.com/",
        body='{"body": "success"}',
        status=200,
        content_type="application/json",
    )

    resp = fetch_data_uncompressed("http://test123.com/", session=Session())

    assert json.loads(resp) == {"body": "success"}
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://test123.com/"
    assert responses.calls[0].response.text == '{"body": "success"}'


@responses.activate
def test_fetch_uncompressed_fail():
    responses.add(
        responses.GET,
        "http://test123.com/error",
        body='{"error": "error"}',
        status=404,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        "http://test123.com/success",
        body='{"success": "success"}',
        status=200,
        content_type="application/json",
    )

    with pytest.raises(Exception):
        fetch_data_uncompressed("http://test123.com/error", session=Session())

    fetch_data_uncompressed("http://test123.com/success", session=Session())

    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == "http://test123.com/error"
    assert responses.calls[1].request.url == "http://test123.com/success"
