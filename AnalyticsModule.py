from collections import defaultdict

from sqlalchemy import func

from Habit import HabitManager
from db.DatabaseModule import session


def get_longest_streak(habits, range):
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
        checkpoint = manager.get_checkpoint_by_habit_id(habit.id)
        days = 0
        if range == "ongoing":
            days += calculate_days(habit.created_at, checkpoint.current_checkpoint)
        else:
            #case "total"
            days += calculate_days(habit.created_at, completion.completion_date)

        return days

    streak_array = []
    for habit in habits:
        streak_array.append(calculate_streak(habit))
    return max(streak_array)


#def get_habits_by_periodicity(habits, periodicity):
#    """
#    Filters habits by their periodicity.
#
#    This function returns a list of habits that match the specified periodicity.
#
#    Args:
#        habits (list): A list of Habit objects.
#        periodicity (str): The periodicity to filter by (e.g., 'daily', 'weekly').
#
#   Returns:
#        list: A list of Habit objects with the specified periodicity.
#    """
#    return [habit for habit in habits if habit.periodicity == periodicity]


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
    habits = habit_manager.get_ongoing_habits()
    historical_habits = habit_manager.get_completed_habits()
    longest_ongoing_streak = get_longest_streak(habits, "ongoing")
    longest_total_streak = get_longest_streak(historical_habits, "total")
    habits_by_periodicity = defaultdict(list)
    for habit in habits:
        habits_by_periodicity[habit.periodicity].append(habit)

    return {
        'longest ongoing streak': longest_ongoing_streak,
        'longest total streak': longest_total_streak,
        'daily_habits': habits_by_periodicity.get('daily', []),
        'weekly_habits': habits_by_periodicity.get('weekly', [])

    }


def calculate_days(started, completed):
    return (completed - started).days if completed > started else 0


def get_streak(habit_id):
    manager = HabitManager(session)
    habit_start = manager.get_habit_by_id(habit_id).created_at
    completed = manager.get_completion_by_habit_id(habit_id)
    return calculate_days(started=habit_start, completed=completed)
