from voice_bench.numbers import endpoint_digits, same_endpoint


def test_endpoint_digits_strip_formatting_and_sip_wrappers():
    assert endpoint_digits("+91 98765-43210") == "919876543210"
    assert endpoint_digits("sip:+919876543210@sip.example;transport=tcp") == "919876543210"
    assert endpoint_digits("15550100001") == "15550100001"
    assert endpoint_digits("") == ""
    assert endpoint_digits(None) == ""


def test_same_endpoint_requires_identical_digits():
    assert same_endpoint("15550100001", "+15550100001")
    assert same_endpoint("sip:+10000000002@sip.example", "+10000000002")
    assert not same_endpoint("+10000000009", "+10000000002")
    assert not same_endpoint("sip:anonymous@sip.example", "+15550100001")
    assert not same_endpoint("", "")
