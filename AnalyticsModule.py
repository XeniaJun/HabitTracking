def get_longest_streak(habits):
    def calculate_streak(completions):
        streak = 0
        max_streak = 0
        completions = sorted(completions)
        for i in range(1, len(completions)):
            if (completions[i] - completions[i - 1]).days <= 1:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
        return max_streak

    return max((calculate_streak([comp.completion_date for comp in habit.completions]) for habit in habits), default=0)


def get_habits_by_periodicity(habits, periodicity):
    return [habit for habit in habits if habit.periodicity == periodicity]


def analyze_habits(habit_manager):
    habits = habit_manager.list_habits()
    longest_streak = get_longest_streak(habits)
    daily_habits = get_habits_by_periodicity(habits, 'daily')
    weekly_habits = get_habits_by_periodicity(habits, 'weekly')
    return {
        'longest_streak': longest_streak,
        'daily_habits': daily_habits,
        'weekly_habits': weekly_habits
    }
