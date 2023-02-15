"""
All tests for commands in this project
"""

from unittest.mock import patch

from django.db.utils import OperationalError
from django.core.management import call_command
from django.test import SimpleTestCase

from psycopg2 import OperationalError as Psycopg2Error


# This decorator will get used by all functions in the class
# will add an argument to every function to simulate the built-in
# method check of the Command class
@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Tests for commands"""

    def test_db_is_available(self, patched_check):
        """Test and make sure the command to wait for DB works"""
        patched_check.return_value = True

        call_command("wait_for_db")

        # check that the check command is being called with the default DB
        patched_check.assert_called_once_with(databases=["default"])

    # This mimicks the behaviour of the sleep function.
    # We don't want to wait in the test so this will catch the sleep and carry on
    @patch("time.sleep")
    def test_wait_for_unavailable_db(self, patched_sleep, patched_check):
        """Test and make sure we're catching errors and wait"""
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.called_with(databases=["default"])
