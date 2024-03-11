from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session, joinedload

from model.predictor import Predictor
from repository.base_repository import BaseRepository
from core.exceptions import NotFoundError


class PredictorRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Predictor)

    def read_by_name(self, name: str, eager=False):
        with self.session_factory() as session:
            query = session.query(self.model)
            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager)))
            query = query.filter(self.model.name == name).first()
            if not query:
                raise NotFoundError(detail=f"not found name : {name}")
            return query
