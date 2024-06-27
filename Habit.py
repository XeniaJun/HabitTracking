import datetime

import questionary
from sqlalchemy import func, Integer, cast
from sqlalchemy.orm import joinedload

from db.DatabaseModule import Habit, Completion, Checkpoint


def get_date_differenz(current_checkpoint, last_checkpoint):
    return (current_checkpoint - last_checkpoint).days


class HabitManager:
    """
    Manages habit tracking, including creating habits,
    marking them as complete, and listing all habits.

    Attributes:
        session: Database session for performing database operations.
    """

    def __init__(self, session):
        """
        Initializes HabitManager with a database session.

        Args:
            session: The database session to use.
        """
        self.session = session

    def add_habit(self, name, periodicity, target_date):
        """
        Adds a new habit to the database.

        Args:
            name (str): The name of the habit.
            periodicity (str): The periodicity of the habit.
            :param name: The name of the habit.
            :param periodicity: The periodicity of the habit.
            :param target_date: The date the habit tracker should be finished.
        """
        new_habit = Habit(name=name, periodicity=periodicity, target_date=target_date)
        self.session.add(new_habit)
        self.session.commit()

    def is_running_habit_streak(self, habit: int):
        checkpoint = self.session.query(Checkpoint).filter_by(habit_id=habit).first()
        if checkpoint is not None and checkpoint.is_valid_streak:
            return True
        elif checkpoint is None:
            return False

    def mark_habit_complete(self, habit_id):
        """
        Marks a habit as complete by adding a completion record.

        Args:
            habit_id (int): The ID of the habit to mark as complete.
        """
        checkpoint_status = self.session.query(Checkpoint).filter_by(habit_id=habit_id).first()
        completion = Completion(habit_id=habit_id,
                                completion_status="SUCCESSFULLY" if checkpoint_status.is_valid_streak else "FAILED")
        self.session.add(completion)
        self.session.commit()

    def get_habit(self, habit_id):
        """
        Retrieves a habit by its ID.

        Args:
            habit_id (int): The ID of the habit to retrieve.

        Returns:
            Habit: The habit with the specified ID, or None if not found.
        """
        return self.session.query(Habit).filter_by(id=habit_id).first()

    def list_habits(self):
        """
        Lists all habits in the database.

        Returns:
            list: A list of all habits.
        """
        return (self.session.query(Habit)
                .outerjoin(Completion, Habit.id == Completion.habit_id)
                .filter(Completion.habit_id == None)
                .all())

    def get_habit_by_name(self, name):
        return self.session.query(Habit).filter_by(name=name).first()

    def get_habit_by_join(self):
        return self.session.query(Habit).options(joinedload(Checkpoint.habit_id))

    def checkin_habit(self, habit: int):
        if self.is_running_habit_streak(habit):
            checkpoint = self.session.query(Checkpoint).filter_by(habit_id=habit).first()
            habit_target_date = self.session.query(Habit).filter_by(id=habit).first().target_date

            checkpoint.is_valid_streak = True if ((get_date_differenz(checkpoint.current_checkpoint,
                                                                      checkpoint.last_checkpoint) == 1
                                                   or get_date_differenz(checkpoint.current_checkpoint,
                                                                         checkpoint.last_checkpoint) == 0)
                                                  and checkpoint.is_valid_streak) else False
            checkpoint.last_checkpoint = checkpoint.current_checkpoint
            checkpoint.current_checkpoint = datetime.date.today()
            checkpoint.next_checkpoint = datetime.date.today() if habit_target_date > datetime.date.today() else None
            self.session.commit()
        else:
            checkpoint = self.session.query(Checkpoint).filter_by(habit_id=habit).first()
            if checkpoint is None:
                checkpoint = Checkpoint(habit_id=habit)
                self.session.add(checkpoint)
                self.session.commit()
            else:
                questionary.print("this Habit broke the streak, due to missing checkpoint."
                                  , style='bold fg:red')

    def get_habit_by_id(self, habit_id):
        return self.session.query(Habit).filter_by(id=habit_id).first()

    def get_completed_habit_by_habit_id(self, habit_id):
        return self.session.query(Completion).filter_by(habit_id=habit_id).first()

    def delete_checkpoints_for_completed_habit(self, habit_id):
        self.session.query(Checkpoint).filter(Checkpoint.habit_id == habit_id).delete()
        self.session.commit()
