import pytest
from db import User, create_user, Session


@pytest.fixture
def session():
    session = Session()
    yield session
    session.rollback()


def test_create_user(session):
    create_user('Han Solo', session)
    session.commit()
    user = session.query(User).filter_by(name='Han Solo').first()
    assert user is not None
    assert user.name == 'Han Solo'
