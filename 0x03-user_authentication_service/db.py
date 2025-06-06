#!/usr/bin/env python3
"""
python script to implent the add_user method
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        method takes in arbitrary keyword arguments and returns the first
        row found in the users table as filtered by the method’s
        input arguments.
        No validation of input arguments required at this point
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise
        except Exception:
            raise InvalidRequestError()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_source = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, value)
            else:
                raise ValueError()
        self._session.commit()
