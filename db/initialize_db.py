import datetime

from sqlalchemy import create_engine, inspect

import json
from db.database_module import session, Habit, engine, Base, Completion, Checkpoint


def tables_initialized():
    """
    Checks if the tables are initialized.

    Returns:
        bool: True if the tables are initialized, False otherwise.
    """
    return session.query(Habit).count() != 0


def initialize_database():
    """
    Initialize the database.

    If the database exists and the tables are not initialized, loads data from SQL and prints a success message.
    Otherwise, prints a message indicating that the database is already initialized with values.

    Returns:
        None

    Example Usage:
        >>> initialize_database()
    """
    if database_exists(engine.url) and not tables_initialized():
        load_data_from_sql()
        print("Values are initialized successfully.")
    else:
        print("Database already initialized with values.")


def database_exists(url):
    """Check if the specified database has certain tables.

    Args:
        url (str): The URL of the database.

    Returns:
        bool: True if any of the tables 'habits', 'checkpoints', or 'completions' exist in the database, False otherwise.
    """
    w_engine = create_engine(url)
    return (inspect(w_engine).has_table('habits') or
            inspect(w_engine).has_table('checkpoints') or
            inspect(w_engine).has_table('completions'))


def create_database(url):
    """
    Args:
        url (str): The URL to connect to the database.

    Note:
        This method creates a database using SQLAlchemy's `create_engine` and `Base.metadata.create_all` functions.

    Example:
        >>> url = 'mysql://username:password@localhost/db_name'
        >>> create_database(url)

    """
    w_engine = create_engine(url)
    Base.metadata.create_all(w_engine)


def submit_values(object_to_inject):
    """
    Args:
        object_to_inject: The object to be added to the session and committed to the database.

    """
    session.add(object_to_inject)
    session.commit()


def load_data_from_sql():
    """

    Loads data from SQL databases and populates the corresponding objects with the retrieved data.

    Returns:
        None
    """
    habits = json.load(open('db/json/habit.json'))

    completed = json.load(open('db/json/completions.json'))

    checkpoint = json.load(open('db/json/checkpoints.json'))
    date_format = '%Y-%m-%d'
    for habit_data in habits:
        habit = Habit(id=habit_data['id'],
                      periodicity=habit_data['periodicity'],
                      name=habit_data['name'],
                      created_at=datetime.datetime.strptime(habit_data['created_at'],
                                                            date_format).date(),
                      target_date=datetime.datetime.strptime(habit_data['target_date'],
                                                             date_format).date())
        submit_values(habit)

    for completion_data in completed:
        completion = Completion(id=completion_data['id'],
                                habit_id=completion_data['habit_id'],
                                completion_status=completion_data['completion_status'],
                                completion_date=datetime.datetime.strptime(completion_data['completion_date'],
                                                                           date_format).date())
        submit_values(completion)

    for checkpoint_data in checkpoint:
        checkpoint = Checkpoint(id=checkpoint_data['id'],
                                habit_id=checkpoint_data['habit_id'],
                                current_checkpoint=datetime.datetime.strptime(checkpoint_data['current_checkpoint'],
                                                                              date_format).date(),
                                last_checkpoint=datetime.datetime.strptime(checkpoint_data['last_checkpoint'],
                                                                           date_format).date(),
                                next_checkpoint=datetime.datetime.strptime(checkpoint_data['next_checkpoint'],
                                                                           date_format).date(),
                                is_valid_streak=checkpoint_data['is_valid_streak'])
        submit_values(checkpoint)
