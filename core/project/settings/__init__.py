import os.path
from pathlib import Path

from split_settings.tools import include, optional

from core.core_utils.utils.pytest import is_pytest_running

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Namespacing our own custom environment variables
ENVVAR_SETTINGS_PREFIX = 'CORESETTINGS_'

LOCAL_SETTINGS_PATH = os.getenv(f'{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH')

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = f'local/settings{".unittests" if is_pytest_running() else ".dev"}.py'

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = os.path.join(BASE_DIR, LOCAL_SETTINGS_PATH)

from django.conf import settings

include(
    'base.py',
    'custom.py',
    optional(LOCAL_SETTINGS_PATH),
    'envvars.py',
    'docker.py',
)

if not is_pytest_running():
    assert SECRET_KEY is not NotImplemented  # type: ignore
