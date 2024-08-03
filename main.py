import datetime
import os

import click
import questionary

import analytics_module
from habit import HabitManager
from db.database_module import session
from db.initialize_db import initialize_database


def view_statistics():
    """

    View Statistics

    Displays statistics based on user input.

    Returns:
        None

    Example:
        view_statistics()
    """
    clear_screen()
    choice = questionary.select(
        "Statistic Menu:",
        choices=[
            "get longest streak",
        ]
    ).ask()
    manager = HabitManager(session)
    if choice == "get longest streak":
        longest_streak = analytics_module.analyze_habits(manager)

        # Print the result in a readable format
        print("Analysis Result:")
        print("\nlongest streak from historical data:")
        questionary.print("\t " + str(longest_streak['longest total streak']) + " Days ", style='bold fg:ansiblue')
        print("\nLongest Streak:")
        questionary.print("\t " + str(longest_streak['longest ongoing streak']) + " Days ", style='bold fg:ansiblue')
        print("Daily ongoing Habits:")
        for habit in longest_streak['daily_habits']:
            questionary.print("\t- " + habit.name + "(ID: " + str(habit.id) + ") -" +
                              str(analytics_module.get_streak(habit, habit.checkpoints[0].current_checkpoint)) +
                              " days streak", style='bold fg:ansiblue')
        print("Weekly ongoing Habits:")
        for habit in longest_streak['weekly_habits']:
            questionary.print("\t- " + habit.name + "(ID: " + str(habit.id) + ") -" +
                              str(analytics_module.get_streak(habit, habit.checkpoints[0].current_checkpoint)) +
                              " days streak", style='bold fg:ansiblue')
    input("Press any Key to continue...")


def set_milestone_for_habit():
    """
    Set milestone for habit.

    This method allows the user to set a milestone for a habit by performing a check-in. The user will be prompted to enter the ID of the habit for which they want to set a milestone.

    Raises:
        N/A

    Returns:
        None

    Example:
        set_milestone_for_habit()
    """
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
    Presents the main menu options to the user and performs the respective actions based on the user's choice.

    Returns:
        None
    """
    while True:
        clear_screen()
        choice = questionary.select(
            "Choose an action:",
            choices=[
                "Checkin Habit streak",
                "Create Habit",
                "Create Predefined Habit",
                "Show ongoing Habits",
                "Complete Habit",
                "Habit statistics",
                "Exit"
            ]
        ).ask()
        if choice == "Create Habit":
            name = (questionary.text("Name of habit").ask())
            periodicity = questionary.select("\nHow often do you want to check in your progress?",
                                             choices=["daily", "weekly"]).ask()
            target_duration_in_days = questionary.text("\n How many Days do you want to keep up?(optional)",
                                                       default='').ask()
            create_habit(name, periodicity, target_duration_in_days)
        elif choice == "Checkin Habit streak":
            set_milestone_for_habit()
        elif choice == "Show ongoing Habits":
            print_habits_as_list()
            input("Press any Key to continue...")
        elif choice == "Complete Habit":
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
    """
    Clears the terminal screen.

    This method will clear the terminal screen by executing the appropriate system command based on the operating system.

    Returns:
        None

    Example:
        clear_screen()
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def predefined_habit():
    """
    Creates a predefined habit based on user input.

    This method prompts the user to choose a predefined habit, select how often they want to check in their progress,
    and define the duration for which they want to keep up with the habit.

    Returns:
        None
    """
    create_habit(
        questionary.select("Choose a predefined habit!",
                           choices=["doing exercise ", "meditation", "healthy diet", "going jogging", "doing yoga"]).ask(),
        questionary.select("How often do you want to check in your progress?",
                           choices=["daily", "weekly"]).ask(),
        questionary.text("\n How many Days do you want to keep up?").ask()
    )


def create_habit(name, periodicity, target_day):
    """
    Creates a new habit with the given parameters and adds it to the habit manager.

    Args:
        name (str): The name of the habit.
        periodicity (str): The periodicity of the habit, e.g., "daily", "weekly", "monthly".
        target_day (str): The target day for the habit (optional). If specified, it should be a positive integer representing the number of days from the current date.

    Returns:
        None
    """
    target_day = datetime.datetime.max.date() if \
        (target_day == "" or not str.isdigit(target_day)) else \
        (datetime.datetime.now().date() + datetime.timedelta(int(target_day)))

    manager = HabitManager(session)
    manager.add_habit(name, periodicity, target_day)
    click.echo(f'Habit: {name} added with periodicity: {periodicity}.')


def complete_habit():
    """
    Complete Habit

    This method allows the user to complete a habit by providing the habit ID.

    Returns:
        None

    Example:
        >>> complete_habit()
        Habit: Exercise | Habit ID: 1 | Created on: 2021-01-01 10:00:00
        Habit: Read | Habit ID: 2 | Created on: 2021-01-02 12:00:00
        Enter the ID of the habit to complete: 1
        Habit with ID 1 marked as complete.
        Press any key to continue...

    Raises:
        None
    """

    manager = HabitManager(session)
    for item in manager.list_habits():
        questionary.print("Habit: " + item.name +
                          " | Habit ID: " + str(item.id) +
                          " | Created on: " + str(item.created_at)
                          , style='bold fg:ansiblue')

    habit_id = questionary.text("Enter the ID of the habit to complete: ").ask()
    if (not habit_id.isdigit() or
            (manager.get_completed_habit_by_habit_id(habit_id) is not None
             and manager.get_habit_by_id(habit_id) is not None)):
        input("Invalid or no habit ID given.\n "
              "Press any Key to continue...")
    else:
        if manager.complete_habit(habit_id):
            click.echo(f'Habit with ID {habit_id} marked as complete.')
            manager.delete_checkpoints_for_completed_habit(habit_id)
    input("Press any Key to continue...")


def print_habits_as_list():
    """
    Prints a list of habits.

    This method retrieves a list of habits using the `list_habits()`
    method and prints each habit's details.

    Example usage:
    ```python
    print_habits_as_list()
    ```

    """
    habits = list_habits()
    for habit in habits:
        click.echo(f'Habit {habit.id}: {habit.name} - {habit.periodicity} - created at: {habit.created_at}')


def list_habits():
    """
    Retrieves a list of habits from the HabitManager.

    :return: A list of habits.
    """
    manager = HabitManager(session)
    habits = manager.list_habits()
    return habits


if __name__ == '__main__':
    print("Welcome to Habit Tracker!")
    print("-------------------------\n")
    initialize_database()
    HabitManager(session).validate_habits()
    main_menue()
