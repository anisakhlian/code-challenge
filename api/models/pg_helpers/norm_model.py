import copy
import random
from typing import List
from sqlalchemy import Column, func, DateTime
from sqlalchemy.ext.declarative import declared_attr


class PGNormModel:

    @declared_attr
    def updated_at(self):
        return Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @declared_attr
    def created_at(self):
        return Column(DateTime, default=func.now(), nullable=False)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'{self.__class__.__name__}<id: {self.id}>'
