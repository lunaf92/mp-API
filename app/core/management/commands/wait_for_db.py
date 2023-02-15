"""
Command class to tell the project to wait for the database to be available 
so we can avoid race condition
"""

import time
from typing import Optional, Any

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write(
                    self.style.WARNING("Database unavailable, retrying in 1 sec...")
                )
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
