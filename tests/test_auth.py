from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import hash_password, verify_password
from app.database import engine
from app.models import User


def test_hash_password_returns_a_hash_without_plaintext():
    password = "correct-password"

    hashed_password = hash_password(password)

    assert hashed_password
    assert hashed_password != password
    assert password not in hashed_password


def test_original_password_verifies_successfully():
    password = "correct-password"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_incorrect_password_does_not_verify():
    hashed_password = hash_password("correct-password")

    assert verify_password("incorrect-password", hashed_password) is False


def test_hashing_functions_do_not_return_plaintext_password():
    password = "correct-password"
    hashed_password = hash_password(password)

    assert password not in hashed_password
    assert verify_password(password, hashed_password) is True


def test_registration_creates_user_with_normalized_email_and_hashed_password(
    client,
):
    email = f"{uuid4()}@example.com"
    password = "correct-password"

    try:
        response = client.post(
            "/auth/register",
            json={"email": f"  {email.upper()}  ", "password": password},
        )

        assert response.status_code == 201
        assert response.json()["email"] == email
        assert isinstance(response.json()["id"], int)
        assert "password_hash" not in response.json()
        assert "password" not in response.json()

        with Session(engine) as session:
            user = session.scalar(select(User).where(User.email == email))

            assert user is not None
            assert user.password_hash != password
            assert user.password_hash.startswith("$argon2id$")
            assert verify_password(password, user.password_hash)
    finally:
        with Session(engine) as session:
            user = session.scalar(select(User).where(User.email == email))
            if user is not None:
                session.delete(user)
                session.commit()


def test_register_duplicate_normalized_email_returns_conflict(client):
    email = f"{uuid4()}@example.com"

    try:
        first_response = client.post(
            "/auth/register",
            json={"email": email, "password": "correct-password"},
        )
        second_response = client.post(
            "/auth/register",
            json={"email": f"  {email.upper()}  ", "password": "other-password"},
        )

        assert first_response.status_code == 201
        assert second_response.status_code == 409
    finally:
        with Session(engine) as session:
            user = session.scalar(select(User).where(User.email == email))
            if user is not None:
                session.delete(user)
                session.commit()


def test_register_invalid_input_returns_422(client):
    response = client.post(
        "/auth/register",
        json={"email": "not-an-email", "password": "short"},
    )

    assert response.status_code == 422
