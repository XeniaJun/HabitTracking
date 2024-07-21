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
   git clone git@github.com:XeniaJun/HabitTracking.git
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
        A[Main Menu] -->|Choose an action| B{Actions}
    B -->|Checkin Habit streak| C[set_milestone_for_habit]
    B -->|Create Habit| D[Add Habit]
    B -->|Read Items| E[print_habits_as_list]
    B -->|Complete Habit| F[complete_habit]
    B -->|Create Predefined Habit| G[predefined_habit]
    B -->|Habit Statistics| H[view_statistics]
    B -->|Exit| I[Exit Application]

    C --> J[Check Habit ID]
    J -->|Valid ID| K[Mark Habit as Complete]
    J -->|Invalid ID| L[Error Message]

    D --> M[Ask for Name]
    D --> N[Ask for Periodicity]
    D --> O[Ask for Target Duration]
    D --> P[Compute Target Date]
    D --> Q[add_habit]

    F --> R[List All Habits]
    R --> S[Ask for Habit ID]
    S -->|Valid ID| T[Mark Habit Complete]
    S -->|Invalid ID| U[Error Message]

    G --> V[Choose Predefined Habit]
    G --> W[Choose Periodicity]
    G --> X[Ask for Target Duration]
    G --> Y[Compute Target Date]
    G --> Z[add_habit]

    H --> AA[Choose Statistics Option]
    AA -->|Get Longest Streak| AB[Analyze Habits]
    AB --> AC[Display Longest Streak]
    AC --> AD[Display Daily Habits]
    AC --> AE[Display Weekly Habits]

    click C href "javascript:alert('Navigate to set_milestone_for_habit');"
    click D href "javascript:alert('Navigate to add_habit');"
    click E href "javascript:alert('Navigate to print_habits_as_list');"
    click F href "javascript:alert('Navigate to complete_habit');"
    click G href "javascript:alert('Navigate to predefined_habit');"
    click H href "javascript:alert('Navigate to view_statistics');"

%% Individual node styling. Try the visual editor toolbar for easier styling!
%%    style E color:#FFFFFF, fill:#AA00FF, stroke:#AA00FF
    style D color:#FFFFFF, stroke:#00C853, fill:#00C853
    style E color:#FFFFFF, stroke:#00C853, fill:#00C853
    style C color:#FFFFFF, stroke:#00C853, fill:#00C853
    style H color:#FFFFFF, stroke:#00C853, fill:#00C853
    style G color:#FFFFFF, stroke:#00C853, fill:#00C853
    style F color:#FFFFFF, stroke:#00C853, fill:#00C853
    style A color:#FFFFFF, stroke:#2962FF, fill:#2962FF
    style I color:#FFFFFF, stroke:#00C853, fill:#00C853

```
