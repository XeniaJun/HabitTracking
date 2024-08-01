import datetime

import questionary
from sqlalchemy import select

import AnalyticsModule
from db.DatabaseModule import Habit, Completion, Checkpoint


def get_date_differenz(current_checkpoint, last_checkpoint):
    return (current_checkpoint - last_checkpoint).days


def set_checkpoint(base_date, periodicity):
    time_to_add = datetime.timedelta(days=1) if periodicity == "daily" else datetime.timedelta(weeks=1)
    return base_date + time_to_add


def streak_is_valid(next_checkpoint, current_checkpoint):
    return True if next_checkpoint >= datetime.datetime.now().date() >= current_checkpoint else False


def print_list(headline, broken_habits):
    questionary.print(headline, style='bold fg:darkred')
    for broken_habit in broken_habits:
        questionary.print(
            " - " + broken_habit.name + "(ID: " + str(broken_habit.id) + "), after" + AnalyticsModule.get_streak(
                broken_habit.id) + "sucessfull Days", style='bold fg:ansiblue')
    input("Press any Key to continue...")


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
        self.checkin_habit(new_habit.id)
        print(f'Inserted new habit_id: {new_habit.id} ,habit {new_habit.name}, Periodicity: {new_habit.periodicity}, '
              f'target date: {target_date}')
        print(f'done')

    def is_running_habit_streak(self, habit: int):
        """

        Args:
            habit:

        Returns:

        """
        checkpoint = self.get_checkpoint_by_habit_id(habit)
        return True if checkpoint is not None and checkpoint.is_valid_streak else False

    def complete_habit(self, habit_id: int):
        """
        Marks a habit as complete by adding a completion record.

        Args:
            habit_id (int): The ID of the habit to mark as complete.
        """
        checkpoint_status = self.get_checkpoint_by_habit_id(habit_id)
        habit = self.get_habit_by_id(habit_id)
        if checkpoint_status is not None:
            completion = Completion(habit_id=habit_id,
                                    completion_status="SUCCESSFULLY" if checkpoint_status.is_valid_streak else "FAILED")
        else:
            completion = Completion(habit_id=habit_id,
                                    completion_status="ABORTED")
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

    def read_habits_by_status(self, habit_status: str):
        """

        Args:
            habit_status:
        """
        habit_list = self.list_habits()
        result = []
        if habit_status == "completed":
            completed = self.get_completed_habits()
            print("Completed")
        elif habit_status == "running":
            result = self.get_ongoing_habits()
            print("Running")
        else:
            #case "failed":
            print("Failed")
        return result

    def get_habit_by_name(self, name):
        return self.session.query(Habit).filter_by(name=name).first()

    def get_ongoing_habits(self):
        """

        Returns:

        """
        subquery = select(Completion.habit_id).subquery()
        return self.session.query(Habit).filter(Habit.id.notin_(select(subquery))).all()

    def get_completed_habits(self):
        """

        Returns:

        """
        subquery = self.session.query(Completion.habit_id).subquery()
        return self.session.query(Habit).filter(Habit.id.in_(subquery)).all()

    def checkin_habit(self, habit: int):
        habit = self.session.query(Habit).filter_by(id=habit).first()
        habit_target_date = habit.target_date

        if self.is_running_habit_streak(habit.id):
            checkpoint = self.get_checkpoint_by_habit_id(habit.id)

            checkpoint.is_valid_streak = streak_is_valid(checkpoint.next_checkpoint, checkpoint.current_checkpoint)
            checkpoint.last_checkpoint = checkpoint.current_checkpoint
            checkpoint.current_checkpoint = datetime.date.today()
            checkpoint.next_checkpoint = set_checkpoint(datetime.datetime.now().date(), habit.periodicity) if (
                    habit_target_date > datetime.datetime.now().date()) else None
            self.session.commit()
        else:
            checkpoint = self.get_checkpoint_by_habit_id(habit.id)
            if checkpoint is None:
                checkpoint = Checkpoint(habit_id=habit.id, next_checkpoint=set_checkpoint(
                    datetime.datetime.now().date(), habit.periodicity))
                self.session.add(checkpoint)
                self.session.commit()
            else:
                questionary.print("this Habit broke the streak, due to missing checkpoint."
                                  , style='bold fg:red')

    def get_habit_by_id(self, habit_id: int):
        return self.session.query(Habit).filter_by(id=habit_id).first()

    def get_completed_habit_by_habit_id(self, habit_id: int):
        return self.session.query(Completion).filter_by(habit_id=habit_id).first()

    def delete_checkpoints_for_completed_habit(self, habit_id: int):
        self.session.query(Checkpoint).filter(Checkpoint.habit_id == habit_id).delete()
        self.session.commit()

    def get_checkpoint_by_habit_id(self, habit_id: int):
        return self.session.query(Checkpoint).filter_by(habit_id=habit_id).first()

    def validate_habit(self):
        ongoing_habits = self.read_habits_by_status("running")
        broken_habits = []
        for habit in ongoing_habits:
            checkpoint = self.get_checkpoint_by_habit_id(habit.id)
            if not streak_is_valid(checkpoint.next_checkpoint, checkpoint.current_checkpoint):
                checkpoint.is_valid_streak = False
                broken_habits.append(habit)
                self.session.commit()
                self.complete_habit(habit.id)
            else:
                pass
        print_list("you broke the streak for following Habits:\n", broken_habits)

    def get_completion_by_habit_id(self, habit_id):
        return self.session.query(Completion).filter_by(habit_id=habit_id).first()
