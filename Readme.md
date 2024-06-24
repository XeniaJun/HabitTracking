# Habit Tracker

Habit Tracker is a command-line application to help users manage their habits. Users can create, read, complete, and manage habits with predefined options. The application uses SQLAlchemy for database interactions and Questionary for a user-friendly CLI interface.

## Features

- Create new habits with specified periodicity (daily or weekly)
- List all existing habits
- Mark habits as complete
- Create predefined habits
- Interactive CLI interface

## Requirements

- Python 3.7 or later
- SQLAlchemy
- Click
- Questionary

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/XeniaJun/habit-tracker.git
   cd habit-tracker
   ```
   
2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
   ```
   
## Usage

Run the main menu to start the application:
```sh
    python main.py
```

## Class Diagram

```mermaid
classDiagram
    class Habit {
        Integer id
        String name
        String periodicity
        DateTime created_at
        +add_habit(name, periodicity)
        +mark_habit_complete(habit_id)
        +get_habit(habit_id)
        +list_habits()
    }

    class Completion {
        Integer id
        Integer habit_id
        String completion_status
        DateTime completion_date
    }

    class Checkpoints {
        Integer id
        Integer habit_id
        DateTime last_checkpoint
        DateTime current_checkpoint
    }

    Habit --> Completion 
    Habit --> Checkpoints 
    Completion --> Habit 
    Checkpoints --> Habit 
```

## Code Structure
- **main.py**: The main entry point for the CLI application.
- **Habit.py**: Contains the HabitManager class for managing habits.
- **db/DatabaseModule.py**: Database models and session setup.


## Sequence Diagramm

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Questionary
    participant HabitManager
    participant Database

    User->>CLI: python main_menue()
    CLI->>Questionary: select action
    Questionary-->>CLI: Create Habit
    CLI->>Questionary: ask for habit name
    Questionary-->>CLI: return habit name
    CLI->>Questionary: ask for periodicity
    Questionary-->>CLI: return periodicity
    CLI->>HabitManager: add_habit(name, periodicity)
    HabitManager->>Database: insert habit
    Database-->>HabitManager: habit added
    HabitManager-->>CLI: habit added confirmation
    CLI-->>User: display confirmation

    User->>CLI: python main_menue()
    CLI->>Questionary: select action
    Questionary-->>CLI: Read Items
    CLI->>HabitManager: list_habits()
    HabitManager->>Database: query habits
    Database-->>HabitManager: return habits
    HabitManager-->>CLI: return habits
    CLI-->>User: display habits

    User->>CLI: python main_menue()
    CLI->>Questionary: select action
    Questionary-->>CLI: Complete habit
    CLI->>Questionary: ask for habit id
    Questionary-->>CLI: return habit id
    CLI->>HabitManager: mark_habit_complete(habit_id)
    HabitManager->>Database: update habit status
    Database-->>HabitManager: habit status updated
    HabitManager-->>CLI: habit marked complete confirmation
    CLI-->>User: display confirmation

    User->>CLI: python main_menue()
    CLI->>Questionary: select action
    Questionary-->>CLI: Create Predefined Habit
    CLI->>Questionary: ask for predefined habit
    Questionary-->>CLI: return predefined habit
    CLI->>Questionary: ask for periodicity
    Questionary-->>CLI: return periodicity
    CLI->>HabitManager: add_habit(predefined habit, periodicity)
    HabitManager->>Database: insert habit
    Database-->>HabitManager: habit added
    HabitManager-->>CLI: habit added confirmation
    CLI-->>User: display confirmation

    User->>CLI: python main_menue()
    CLI->>Questionary: select action
    Questionary-->>CLI: Exit
    CLI-->>User: print "Exiting the application."
```
## Flow Chart
```mermaid
flowchart TD
    A[Start Application] --> B[Main Menu]
    B --> C{Choose an action}
    C --> D[Create Habit]
    C --> E[Read Items]
    C --> F[Complete habit]
    C --> G[Create Predefined Habit]
    C --> H[Habit statistics]
    C --> I[Exit]
    
    D --> J[Prompt for habit name]
    J --> K[Prompt for periodicity]
    K --> L[Call add_habit]
    L --> B
    
    E --> M[Call list_habits]
    M --> B
    
    F --> N[Prompt for habit ID]
    N --> O[Call complete_habit]
    O --> B
    
    G --> P[Prompt for predefined habit]
    P --> Q[Prompt for periodicity]
    Q --> R[Call add_habit]
    R --> B
    
    H --> S[Call get_statistics]
    S --> B
    
    I --> T[Print 'Exiting the application.']
    T --> U[End]
    
    click L href "add_habit"
    click M href "list_habits"
    click O href "complete_habit"
    click R href "add_habit"
    click S href "get_statistics"

```