import datetime
import os

import click
import questionary
from prompt_toolkit.styles import Style

from Habit import HabitManager
from db.DatabaseModule import session, Habit


# TODO: implement this with the already implemented AnalyticsModule.py. it still needs refactoring
def view_statistics():
    clear_screen()
    choice = questionary.select(
        "Statistic Menu:",
        choices=[
            "get longest streak",
            "Create Habit",
            "Read Items",
            "Complete habit",
            "Create Predefined Habit",
            "Habit statistics",
            "Exit"
        ]
    ).ask()
    pass


def set_milestone_for_habit():
    list_habits()


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
                                             choices=["daily", "weekly"]).ask()
            target_duration_in_days = questionary.text("\n How many Days do you want to keep up?", default='30').ask()
            target_date = datetime.datetime.now().date() + datetime.timedelta(days=int(target_duration_in_days))
            add_habit(name, periodicity, target_date)
        elif choice == "Checkin Habit streak":
            set_milestone_for_habit()
        elif choice == "Read Items":
            list_habits()
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
                           choices=["Nail biting", "smoking", "eating sugar"]).ask(),
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
    if not habit_id or not manager.get_habit_by_id(habit_id):
        input("Invalid or no habit ID given.\n "
              "Press any Key to continue...")
        pass
    else:
        manager.mark_habit_complete(habit_id)
        click.echo(f'Habit with ID {habit_id} marked as complete.')


def list_habits():
    """
    Lists all habits in the Habit Tracker.

    This function retrieves all habits from the database and displays them.
    """
    manager = HabitManager(session)
    habits = manager.list_habits()
    for habit in habits:
        click.echo(f'Habit {habit.id}: {habit.name} - {habit.periodicity} - created at: {habit.created_at}')
    input("Press any Key to continue...")


if __name__ == '__main__':
    main_menue()
