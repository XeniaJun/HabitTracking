import datetime
import os

import click
import questionary
from prompt_toolkit.styles import Style

import AnalyticsModule
from Habit import HabitManager
from db.DatabaseModule import session, Habit


# TODO: implement this with the already implemented AnalyticsModule.py. it still needs refactoring
def view_statistics():
    clear_screen()
    choice = questionary.select(
        "Statistic Menu:",
        choices=[
            "get longest streak",
        ]
    ).ask()
    manager = HabitManager(session)
    if choice == "get longest streak":
        longest_streak = AnalyticsModule.analyze_habits(manager)

        # Print the result in a readable format
        print("Analysis Result:")
        print(f"Longest Streak: {longest_streak['longest_streak']}")
        print("Daily Habits:")
        for habit in longest_streak['daily_habits']:
            print(f" - {habit.name} (ID: {habit.id})")
        print("Weekly Habits:")
        for habit in longest_streak['weekly_habits']:
            print(f" - {habit.name} (ID: {habit.id})")
            #questionary.print("" + item.
            #                  , style='bold fg:red')
    input("Press any Key to continue...")


def set_milestone_for_habit():
    print_habits_as_list()
    answer = questionary.text("type Habit ID -  to do check in:").ask()
    exit_text = "wrong input character given. ID is not valid."
    if answer.isdigit():
        manager = HabitManager(session)
        manager.checkin_habit(int(answer))
        exit_text = "Press any Key to continue..."
    input(exit_text)


def main_menue():
    """
    Main menu for the Habit Tracker CLI application.

    This function displays a menu with options to create habits, read items,
    complete habits, create predefined habits, or exit the application.
    The user is prompted to select an action, which is then executed.
    """
    while True:
        clear_screen()
        choice = questionary.select(
            "Choose an action:",
            choices=[
                "Checkin Habit streak",
                "Create Habit",
                "Read Items",
                "Complete habit",
                "Create Predefined Habit",
                "Habit statistics",
                "Exit"
            ]
        ).ask()
        if choice == "Create Habit":
            name = questionary.text("Name of habit", default="nothing").ask()
            periodicity = questionary.select("\nWhat do you want to add?",
                                             choices=["every day", "every week"]).ask()
            target_duration_in_days = questionary.text("\n How many Days do you want to keep up?", default='30').ask()
            target_date = datetime.datetime.now().date() + datetime.timedelta(days=int(target_duration_in_days))
            add_habit(name, periodicity, target_date)
        elif choice == "Checkin Habit streak":
            set_milestone_for_habit()
        elif choice == "Read Items":
            print_habits_as_list()
            input("Press any Key to continue...")
        elif choice == "Complete habit":
            complete_habit()
        elif choice == "Create Predefined Habit":
            predefined_habit()
        elif choice == "Habit statistics":
            view_statistics()
        elif choice == "Exit":
            print("Exiting the application.")
            break

        clear_screen()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def predefined_habit():
    """
    Creates a predefined habit using predefined options.

    This function prompts the user to select a predefined habit and its
    periodicity, then adds the habit using the add_habit function.
    """
    add_habit(
        questionary.select("Choose a predefined habit!",
                           choices=["Nail biting", "smoking", "eating sugar", "doing drugs", "drinking alcohol"]).ask(),
        questionary.select("How often do you want to set checkpoints?",
                           choices=["every day", "every week"]).ask(),
        datetime.datetime.now().date() + datetime.timedelta(
            days=int(questionary.text("\n How many Days do you want to keep up?", default='30').ask()))
    )


def add_habit(name, periodicity, target_day):
    """
    Adds a new habit to the Habit Tracker.

    This function creates a new habit using the provided name and periodicity,
    then adds it to the database.

    Args:
        name (str): The name of the habit.
        periodicity (str): The periodicity of the habit (e.g., daily, weekly).
        param target_day (Date): The target day of the habit.
    """
    manager = HabitManager(session)
    manager.add_habit(name, periodicity, target_day)
    click.echo(f'Habit {name} added with periodicity {periodicity}.')


def complete_habit():
    """
    Marks a habit as complete.

    This function prompts the user to enter the ID of the habit to be marked as
    complete, then updates the habit's completion status in the database.
    """

    manager = HabitManager(session)
    for item in manager.list_habits():
        questionary.print("Habit: " + item.name +
                          " | Habit ID: " + str(item.id) +
                          " | Created on: " + str(item.created_at)
                          , style='bold fg:ansiblue')

    habit_id = questionary.text("Enter the ID of the habit to complete:").ask()
    if (not habit_id.isdigit() or
            (manager.get_completed_habit_by_habit_id(habit_id) is not None
             and manager.get_habit_by_id(habit_id) is not None)):
        input("Invalid or no habit ID given.\n "
              "Press any Key to continue...")
        pass
    else:
        manager.mark_habit_complete(habit_id)
        click.echo(f'Habit with ID {habit_id} marked as complete.')
        manager.delete_checkpoints_for_completed_habit(habit_id)


def print_habits_as_list():
    habits = list_habits()
    for habit in habits:
        click.echo(f'Habit {habit.id}: {habit.name} - {habit.periodicity} - created at: {habit.created_at}')


def list_habits():
    """
    Lists all habits in the Habit Tracker.

    This function retrieves all habits from the database and displays them.
    """
    manager = HabitManager(session)
    habits = manager.list_habits()
    return habits


if __name__ == '__main__':
    main_menue()
