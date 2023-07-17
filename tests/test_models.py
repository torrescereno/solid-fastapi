from app.models.user import User


# Test unitarios
def test_user_model():
    user = User(id=1, username="test", password="testpass")

    assert user.id == 1
    assert user.username == "test"
    assert user.password == "testpass"

    user.id = 2
    user.username = "test2"
    user.password = "testpass2"

    assert user.id == 2
    assert user.username == "test2"
    assert user.password == "testpass2"
