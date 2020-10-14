

from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GlobalMedList(Base):
    """
    Bean representing a pre-existing table.
    """
    __tablename__ = 'GlobalMedList'

    Id = Column('ID', Integer, autoincrement=False, primary_key=True)
    Name = Column('NAME', String(128), nullable=False)
    Dose = Column('DOSE', Numeric(12, 2), nullable=True)
    Created = Column('CREATED', DateTime, nullable=False)

    def __repr__(self):
        return f"Med(Name={self.Name}, Dose={self.Dose})"
