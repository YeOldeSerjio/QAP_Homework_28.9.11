from pydantic import BaseModel
import pytest
import requests


class AccessTokenRequest(BaseModel):
    access_token: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str


def test_access_token_required():
    request = {
        "access_token": "token111"
    }
    AccessTokenRequest(**request)


def test_users_get_response():
    response = [
        {"id": 101, "first_name": "Alan", "last_name": "McAllan"},
        {"id": 202, "first_name": "Marty", "last_name": "McMarty"}
    ]
    users = [User(**user) for user in response]


def test_access_token_required():
    request = {}
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def test_access_token_format():
    request = {
        "access_token": "invalid_token_format"
    }
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def test_users_get_access():
    response = [
        {"id": 101, "first_name": "Alan", "last_name": "McAllan"},
        {"id": 202, "first_name": "Marty", "last_name": "McMarty"}
    ]
    users = [User(**user) for user in response]
    assert len(users) == 2
    assert users[0].id == 101
    assert users[0].first_name == "Alan"
    assert users[0].last_name == "McAllan"


def test_users_get_no_users():
    response = []
    users = [User(**user) for user in response]
    assert len(users) == 0


def test_user_format():
    user = {
        "id": "invalid_id_format",
        "first_name": "Alan",
        "last_name": "McAllan"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_name_format():
    user = {
        "id": 101,
        "first_name": "Alien",
        "last_name": "McAllan"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_lastname_format():
    user = {
        "id": 202,
        "first_name": "Marty",
        "last_name": "Moriarty"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_get_one_user():
    response = [{"id": 202, "first_name": "Marty", "last_name": "McMarty"}]
    users = [User(**user) for user in response]
    assert len(users) == 1
    assert users[0].id == 202
    assert users[0].first_name == "Marty"
    assert users[0].last_name == "MCMarty"


def test_users_get_max_users():
    response = [{"id": i, "first_name": "User", "last_name": str(i)} for i in range(100)]
    users = [User(**user) for user in response]
    assert len(users) == 100
    assert users[-1].id == 99
    assert users[-1].first_name == "User"
    assert users[-1].last_name == "99"


def test_users_get_invalid_response():
    response = [{"invalid_attr": "value"}]
    with pytest.raises(ValueError):
        users = [User(**user) for user in response]
