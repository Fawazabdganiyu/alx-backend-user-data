#!/usr/bin/env python3
"""DB module
"""
from typing import TypeVar

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User

UserT = TypeVar("UserT", bound=User)


class DB:
    """DB class
    """

    user_id: int = 0

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")  # , echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(
            self, email: str, hashed_password: str,
            session_id: str = 'session', reset_token: str = 'token'
    ) -> UserT:
        """Add a new user"""
        self.user_id += 1
        user = User(id=self.user_id, email=email,
                    hashed_password=hashed_password,
                    session_id=session_id, reset_token=reset_token)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> UserT:
        """Find a user by the given arbitrary keyword arguments"""
        user = self._session.query(User).filter_by(**kwargs).first()
        # InvalidRequestError would be raised implicitly when
        # wrong query arguments are passed
        if not user:
            raise NoResultFound
        return user
