# This is a sample Python script.
import questionary
from prompt_toolkit.styles import Style
from sqlalchemy.orm import Session

from db.Model import Base
from db.habitDB import engine, HabitsDB, read_default_habits


def create_new_habit():
    pass

# TODO: retrieve all Entries from Database which are not default
def view_habits():
    pass


def find_key(input_dict, value):
    for key, val in input_dict.items():
        if val == value: return key
    return "None"


def status_habits():
    pass


def delete_habit():
    pass

'''
main method which is being executed
'''

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    rslt = read_default_habits()
    '''
    Key Value Pair for shortening the procession of the selection
    '''
    main_menu = {
        'S': 'Status of chosen Habits',
        'R': 'View existing Habits',
        'C': 'create new habits',
        'D': 'delete habits',
        'E': 'end program'}

    '''
    initial selection phase
    '''
    initialEntry = (questionary.select("Hello, what would you like to do?",
                                       choices=list(main_menu.values()),
                                       default="View existing Habits",
                                       style=Style([("selected", "noreverse")]))
                    .ask())
answers = "you chose : " + initialEntry
questionary.print(answers, style='bold fg:green')

answerSelector = find_key(main_menu, initialEntry)


'''
handling the different Cases
'''

match initialEntry:
    case 'R':
        view_habits()
    case 'C':
        create_new_habit()
    case 'D':
        delete_habit()
    case 'S':
        status_habits()
    case 'E':
        quit(0)
