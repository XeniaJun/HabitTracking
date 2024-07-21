import datetime

from sqlalchemy import create_engine, inspect

import json
from db.DatabaseModule import session, Habit, engine, Base, Completion, Checkpoint


def tables_initialized():

    value_to__check = session.query(Habit).count() != 0
    db_values = session.query(Habit).all()
    return session.query(Habit).count() != 0


def initialize_database():
    if database_exists(engine.url) and not tables_initialized():
        load_data_from_sql()
        print("Values are initialized successfully.")
    else:
        print("Database already initialized with values.")


def database_exists(url):
    w_engine = create_engine(url)
    return (inspect(w_engine).has_table('habits') or
            inspect(w_engine).has_table('checkpoints') or
            inspect(w_engine).has_table('completions'))


def create_database(url):
    w_engine = create_engine(url)
    Base.metadata.create_all(w_engine)


def submit_values(object_to_inject):
    session.add(object_to_inject)
    session.commit()


def load_data_from_sql():
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
