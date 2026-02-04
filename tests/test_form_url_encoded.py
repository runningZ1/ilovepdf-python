from ilovepdf.request_payload import FormUrlEncoded


def test_form_url_encoded_nested():
    body = {
        "a": {"b": 1},
        "c": ["x", "y"],
        "d": None,
    }
    encoded = FormUrlEncoded(body).extract_to_str()
    assert "a[b]=1" in encoded
    assert "c[0]=x" in encoded
    assert "c[1]=y" in encoded
    assert "d=" not in encoded
