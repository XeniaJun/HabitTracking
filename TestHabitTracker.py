import os
import unittest
from unittest.mock import patch, MagicMock
import datetime

from main import view_statistics, set_milestone_for_habit, clear_screen, predefined_habit, add_habit, \
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


    @patch('main.os.system')
    def test_clear_screen(self, mock_system):
        clear_screen()
        mock_system.assert_called_once_with('cls' if os.name == 'nt' else 'clear')

    @patch('main.HabitManager')
    @patch('click.echo')
    def test_add_habit(self, mock_click_echo, mock_HabitManager):
        mock_manager = mock_HabitManager.return_value
        add_habit("Test Habit", "daily", datetime.date.today())

        mock_manager.add_habit.assert_called_once_with("Test Habit", "daily", datetime.date.today())
        mock_click_echo.assert_called_once_with('Habit Test Habit added with periodicity daily.')

    @patch('main.HabitManager')
    def test_list_habits(self, mock_HabitManager):
        mock_manager = mock_HabitManager.return_value
        list_habits()

        mock_manager.list_habits.assert_called_once()


if __name__ == '__main__':
    unittest.main()
