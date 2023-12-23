from datetime import timedelta

from app.core.security import create_access_token


def test_create_access_token_success():
    # given
    subject = "test"
    expires_delta = timedelta(minutes=5)

    # when
    token = create_access_token(subject=subject, expires_delta=expires_delta)

    # then
    assert isinstance(token, str)
    assert token != ""
