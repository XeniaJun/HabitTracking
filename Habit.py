from sqlalchemy.orm import joinedload

from db.DatabaseModule import Habit, Completion, Checkpoint


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
        new_habit = self.session.query(Habit).filter_by(name=name).first()
        self.checkin_habit(habit=new_habit)

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

    def checkin_habit(self, habit):
        checkpoint = Checkpoint(habit_id=habit.id)
        self.session.add(checkpoint)
        self.session.commit()

    def get_habit_by_id(self, habit_id):
        return self.session.query(Habit).filter_by(id=habit_id).first()
