from abc import abstractmethod
from contextlib import contextmanager

from utils.utils import log_error


class BaseRepository:
    def __init__(self, model, session_factory):
        self.model = model
        self._session_factory = session_factory

    @contextmanager
    def get_session(self):
        session = self._session_factory()
        session.expire_on_commit = False
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            log_error(self.model.__name__, e)
            raise e
        finally:
            # For scoped_session, use remove() to clear the current thread's session.
            # If you’re using a plain session, you’d call session.close() instead.
            if hasattr(self._session_factory, "remove"):
                self._session_factory.remove()
            else:
                session.close()

    def get_all(self):
        """
        Fetch all records from the model provided.
        Returns a list of objects.
        """
        if self.model is None:
            raise ValueError("Model is not defined for this repository.")

        with self.get_session() as session:
            return session.query(self.model).all()

    def create(self, obj_data: dict):
        """
        Create a new record using the model provided.
        Returns the created object.
        """
        if self.model is None:
            raise ValueError("Model is not defined for this repository.")

        with self.get_session() as session:
            obj = self.model(**obj_data)
            session.add(obj)
            # Optionally, flush to get assigned IDs immediately
            session.flush()
            return obj

    def create_all(self, objs_data: list):
        if self.model is None:
            raise ValueError("Model is not defined for this repository.")

        with self.get_session() as session:
            objs = [self.model(**data) for data in objs_data]
            session.add_all(objs)
            session.flush()
            return objs

    def execute(self, query):
        """
        Execute a raw SQL query or a SQLAlchemy text query.
        Returns all fetched results.
        """
        with self.get_session() as session:
            session.execute(query)


class CrossChainRepository(BaseRepository):
    @abstractmethod
    def populate_table(self, query) -> None:
        pass

    @abstractmethod
    def get_number_of_records(self) -> None:
        pass

    @abstractmethod
    def get_min_timestamp(self) -> None:
        pass

    @abstractmethod
    def get_max_timestamp(self) -> None:
        pass

    @abstractmethod
    def empty_table(self) -> None:
        pass

    @abstractmethod
    def get_unique_src_dst_contract_pairs(self) -> None:
        pass
