from sqlalchemy.orm.scoping import scoped_session


class BaseDAO:
    def __init__(self, session: scoped_session):
        """Session needs to be submitted when creating dao object"""
        self.session = session
