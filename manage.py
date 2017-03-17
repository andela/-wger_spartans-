#!/usr/bin/env python
import sys
import os

from django.core.management import execute_from_command_line

from tasks import (
    setup_django_environment,
    get_user_config_path
)

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wger.settings")

    execute_from_command_line(sys.argv)
