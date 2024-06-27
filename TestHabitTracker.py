import os
import unittest
from unittest.mock import patch, MagicMock
import datetime

from Habit import HabitManager
from db.DatabaseModule import session, Habit
from main import view_statistics, set_milestone_for_habit, main_menue, clear_screen, predefined_habit, add_habit, \
    complete_habit, print_habits_as_list, list_habits


class TestHabitTracker(unittest.TestCase):

    @patch('main.questionary.select')
    @patch('main.AnalyticsModule.analyze_habits')
    def test_view_statistics(self, mock_analyze_habits, mock_select):
        mock_select.return_value.ask.return_value = "get longest streak"
        mock_analyze_habits.return_value = {
            'longest_streak': 10,
            'daily_habits': [],
            'weekly_habits': []
        }

        with patch('builtins.input', return_value=''):
            view_statistics()

        mock_select.assert_called_once()
        mock_analyze_habits.assert_called_once()

    @patch('main.questionary.text')
    @patch('main.print_habits_as_list')
    def test_set_milestone_for_habit(self, mock_print_habits_as_list, mock_text):
        mock_text.return_value.ask.return_value = "1"
        mock_manager = MagicMock()
        with patch('main.HabitManager', return_value=mock_manager):
            with patch('builtins.input', return_value=''):
                set_milestone_for_habit()

        mock_text.assert_called_once()
        mock_print_habits_as_list.assert_called_once()
        mock_manager.checkin_habit.assert_called_once_with(1)

    @patch('main.questionary.select')
    @patch('main.add_habit')
    @patch('builtins.input', return_value='wurstbrot')
    def test_main_menue_create_habit(self, mock_input, mock_add_habit, mock_select):
        mock_select.return_value.ask.side_effect = [
            "Create Habit", "New Habit", "every day", "30", "Exit"
        ]

        with patch('main.clear_screen'):
            main_menue()

        self.assertEqual(mock_select.return_value.ask.call_count, 5)
        mock_add_habit.assert_called_once_with("New Habit", "every day",
                                               datetime.date.today() + datetime.timedelta(days=30))

    @patch('main.os.system')
    def test_clear_screen(self, mock_system):
        clear_screen()
        mock_system.assert_called_once_with('cls' if os.name == 'nt' else 'clear')

    @patch('main.questionary.select')
    @patch('main.add_habit')
    def test_predefined_habit(self, mock_add_habit, mock_select):
        mock_select.return_value.ask.side_effect = [
            "Nail biting", "every day", "30"
        ]

        predefined_habit()

        self.assertEqual(mock_select.return_value.ask.call_count, 3)
        mock_add_habit.assert_called_once_with("Nail biting", "every day",
                                               datetime.date.today() + datetime.timedelta(days=30))

    @patch('main.HabitManager')
    @patch('click.echo')
    def test_add_habit(self, mock_click_echo, mock_HabitManager):
        mock_manager = mock_HabitManager.return_value
        add_habit("Test Habit", "daily", datetime.date.today())

        mock_manager.add_habit.assert_called_once_with("Test Habit", "daily", datetime.date.today())
        mock_click_echo.assert_called_once_with('Habit Test Habit added with periodicity daily.')

    @patch('main.questionary.text')
    @patch('main.HabitManager')
    @patch('click.echo')
    def test_complete_habit(self, mock_click_echo, mock_HabitManager, mock_text):
        mock_manager = mock_HabitManager.return_value
        mock_manager.list_habits.return_value = [MagicMock(id=1, name="Test Habit", created_at=datetime.date.today())]
        mock_text.return_value.ask.return_value = "1"

        with patch('builtins.input', return_value=''):
            complete_habit()

        mock_text.assert_called_once()
        mock_manager.mark_habit_complete.assert_called_once_with("1")
        mock_click_echo.assert_called_once_with('Habit with ID 1 marked as complete.')

    @patch('click.echo')
    def test_print_habits_as_list(self, mock_click_echo):
        mock_habits = [
            MagicMock(id=1, name="Habit 1", periodicity="daily", created_at=datetime.date.today()),
            MagicMock(id=2, name="Habit 2", periodicity="weekly", created_at=datetime.date.today())
        ]

        with patch('main.list_habits', return_value=mock_habits):
            print_habits_as_list()

        self.assertEqual(mock_click_echo.call_count, 2)
        mock_click_echo.assert_any_call(f'Habit 1: Habit 1 - daily - created at: {datetime.date.today()}')
        mock_click_echo.assert_any_call(f'Habit 2: Habit 2 - weekly - created at: {datetime.date.today()}')

    @patch('main.HabitManager')
    def test_list_habits(self, mock_HabitManager):
        mock_manager = mock_HabitManager.return_value
        list_habits()

        mock_manager.list_habits.assert_called_once()


if __name__ == '__main__':
    unittest.main()
