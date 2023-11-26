import os
import sys


def is_pytest_running():
    print('!!!!!!!', os.getenv('PYTEST_RUNNING'))
    return os.getenv('PYTEST_RUNNING') == 'true' or os.path.basename(
        sys.argv[0]) in ('pytest', 'py.test')
