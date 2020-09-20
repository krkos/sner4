# This file is part of sner4 project governed by MIT license, see the LICENSE.txt file.
"""
planner command tests
"""

import pytest

from sner.server.planner.commands import command


@pytest.mark.filterwarnings('ignore:.*running the worker with superuser privileges.*')
def test_run_coverage(runner):
    """run planner in test mode to trigger coverage"""

    runner.app.config['SNER_PLANNER']['pipelines'] = [
        {'type': 'queue', 'steps': []},
        {'type': 'standalone', 'steps': []},
        {'type': 'invalid'}
    ]

    result = runner.invoke(command, ['run', '--oneshot'])
    assert result.exit_code == 0
