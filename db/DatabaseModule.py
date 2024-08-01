import datetime

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Habit(Base):
    """
    Represents a habit in the habit tracking system.

    Attributes:
        id (int): Primary key.
        name (str): Name of the habit.
        periodicity (str): Frequency of the habit (e.g., daily, weekly).
        created_at (datetime): Timestamp when the habit was created.
        completions (list of Completion): List of completions associated with this habit.
    """
    __tablename__ = 'habits'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    periodicity = Column(String, nullable=False)
    created_at = Column(Date, default=datetime.datetime.today().date())
    target_date = Column(Date, nullable=True)
    completions = relationship('Completion', back_populates='habit')
    checkpoints = relationship('Checkpoint', back_populates='habit')


class Completion(Base):
    """
    Represents a completion record for a habit.

    Attributes:
        id (int): Primary key.
        habit_id (int): Foreign key to the associated habit.
        completion_status (str): Status of the completion.
        completion_date (datetime): Timestamp when the habit was completed.
        habit (Habit): The habit associated with this completion.
    """
    __tablename__ = 'completions'
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey('habits.id'))
    completion_status = Column(String, nullable=False)
    completion_date = Column(Date, default=datetime.datetime.now(datetime.timezone.utc).date())
    habit = relationship('Habit', back_populates='completions')


class Checkpoint(Base):
    """
    Represents a checkpoint for tracking progress on a habit.

    Attributes:
        id (int): Primary key.
        habit_id (int): Foreign key to the associated habit.
        last_checkpoint (datetime): Timestamp of the last checkpoint.
        current_checkpoint (datetime): Timestamp of the current checkpoint.
        habit (Habit): The habit associated with this checkpoint.
        completion (Completion): The completion associated with this habit (if any).
    """
    __tablename__ = 'checkpoints'
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey('habits.id'))
    last_checkpoint = Column(Date, default=datetime.datetime.now(datetime.timezone.utc).date())
    current_checkpoint = Column(Date, default=datetime.datetime.now(datetime.timezone.utc).date())
    next_checkpoint = Column(Date, default=datetime.datetime.now(datetime.timezone.utc).date() +
                                           datetime.timedelta(days=int(1)))
    is_valid_streak = Column(Boolean, default=True)
    habit = relationship('Habit', back_populates='checkpoints')


# Set up the database engine and create all tables
engine = create_engine('sqlite:///habits.db')
Base.metadata.create_all(engine)

# Create a session factory bound to the engine
Session = sessionmaker(bind=engine)
session = Session()
