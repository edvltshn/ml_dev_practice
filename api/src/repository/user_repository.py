from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from  core.exceptions import NotFoundError

from  model.user import User
from  repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)

    def update_user_balance(self, user, new_balance):
        with self.session_factory() as session:
            try:
                user = session.query(self.model).filter(self.model.id == user.id).one()
                user.blance = new_balance 
                session.commit()

            except NoResultFound:
                raise NotFoundError(detail=f"User with id {user.id} not found.")
