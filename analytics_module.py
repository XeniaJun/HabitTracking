from collections import defaultdict


def get_longest_streak(habits, range_streak):
    """
    Calculates the longest streak of habit completions.

    This function takes a list of habits and determines
    the longest streak of consecutive completions for any habit.

    Args:
        range_streak:
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
        days = 0
        if range_streak == "ongoing":
            days += calculate_days(habit.created_at, habit.checkpoints[0].current_checkpoint)
        else:
            # case "total"
            days += calculate_days(habit.created_at, habit.completions[0].completion_date)

        return days

    streak_array = []
    for habit in habits:
        streak_array.append(calculate_streak(habit))
    return max(streak_array)


def analyze_habits(habit_manager):
    """
    Analyzes the habits and provides various insights.

    This function uses the habit manager to list all habits and
    then calculates the longest streak of completions,
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


def get_streak(habit, compare_date):
    return calculate_days(started=habit.created_at, completed=compare_date)
