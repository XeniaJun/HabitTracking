from db.DatabaseModule import Habit, Completion


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

    def add_habit(self, name, periodicity):
        """
        Adds a new habit to the database.

        Args:
            name (str): The name of the habit.
            periodicity (str): The periodicity of the habit.
        """
        new_habit = Habit(name=name, periodicity=periodicity)
        self.session.add(new_habit)
        self.session.commit()

    def mark_habit_complete(self, habit_id):
        """
        Marks a habit as complete by adding a completion record.

        Args:
            habit_id (int): The ID of the habit to mark as complete.
        """
        completion = Completion(habit_id=habit_id)
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
        return self.session.query(Habit).all()
