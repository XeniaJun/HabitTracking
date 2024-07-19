from collections import defaultdict

from sqlalchemy import func

from Habit import HabitManager
from db.DatabaseModule import session


def get_longest_streak(habits):
    """
    Calculates the longest streak of habit completions.

    This function takes a list of habits and determines the longest streak of consecutive completions for any habit.

    Args:
        habits (list): A list of Habit objects.

    Returns:
        int: The length of the longest completion streak.
    """

    def calculate_streak(habit):
        """
        Helper function to calculate the streak from a list of completion dates.

        Args:
            completions (list): A sorted list of datetime objects representing completion dates.

        Returns:
            int: The longest streak of consecutive completions.
        """
        manager = HabitManager(session)
        completion = manager.get_completed_habit_by_habit_id(habit.id)
        checkpoints = manager.get_checkpoint_by_habit_id(habit.id)

        return checkpoints.current_checkpoint - habit.created_at

    streak_array = []
    for habit in habits:
        streak_array.append(calculate_streak(habit))
    return max(streak_array)


def get_habits_by_periodicity(habits, periodicity):
    """
    Filters habits by their periodicity.

    This function returns a list of habits that match the specified periodicity.

    Args:
        habits (list): A list of Habit objects.
        periodicity (str): The periodicity to filter by (e.g., 'daily', 'weekly').

    Returns:
        list: A list of Habit objects with the specified periodicity.
    """
    return [habit for habit in habits if habit.periodicity == periodicity]


def analyze_habits(habit_manager):
    """
    Analyzes the habits and provides various insights.

    This function uses the habit manager to list all habits and then calculates the longest streak of completions,
    and categorizes habits by their periodicity (daily or weekly).

    Args:
        habit_manager (HabitManager): An instance of HabitManager to interact with the database.

    Returns:
        dict: A dictionary containing the longest streak, daily habits, and weekly habits.
    """
    habits = habit_manager.list_habits()
    longest_streak = get_longest_streak(habits)

    habits_by_periodicity = defaultdict(list)
    for habit in habits:
        habits_by_periodicity[habit.periodicity].append(habit)

    return {
        'longest_streak': longest_streak,
        'daily_habits': habits_by_periodicity.get('every day', []),
        'weekly_habits': habits_by_periodicity.get('every week', [])

    }
