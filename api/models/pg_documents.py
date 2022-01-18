from sqlalchemy import Table, Column, DateTime, String, Boolean, ForeignKey, event, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import orm
from .pg_helpers.sqlalchemy_helper import SqlalchemyHelper
from .pg_helpers.norm_model import PGNormModel
from .pg_helpers.uuid_helper import uuid_str


class PgDocument(SqlalchemyHelper.Base, PGNormModel):
    """
    Document SQLAlchemy model.
    """

    __tablename__ = 'documents'

    id = Column(UUID(), primary_key=True, default=uuid_str)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    is_pinned = Column(Boolean, default=False)
    deleted_at = Column(DateTime, default=None, nullable=True)
    parent_id = Column(UUID(), ForeignKey('documents.id', ondelete="CASCADE"))

    def __repr__(self):
        return f'Document<id: {self.id}, title: {self.title}>'

    def serialize(self):
        data = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
        }

        return data
