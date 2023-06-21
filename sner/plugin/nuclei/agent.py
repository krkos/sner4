# This file is part of sner4 project governed by MIT license, see the LICENSE.txt file.
"""
sner agent nuclei module
"""

import shlex
from pathlib import Path

from schema import Schema, Optional

from sner.agent.modules import ModuleBase


class AgentModule(ModuleBase):
    """
    nuclei module

    ## target specification
    target = host-target
    """

    CONFIG_SCHEMA = Schema({
        'module': 'nuclei',
        'args': str
    })

    def __init__(self):
        super().__init__()
        self.loop = True

    def run_scan(self, assignment, targets, targets_file, output_file, extra_args=None):  # pylint: disable=too-many-arguments
        """run scan"""

        Path(targets_file).write_text('\n'.join(targets), encoding='utf-8')

        timing_args = []
        if 'timing_perhost' in assignment['config']:
            output_rate = assignment['config']['timing_perhost'] * len(targets)
            timing_args = [
                '-retries', '3',
                '-timeout', '600',
                '-rate-limit', str(output_rate)
            ]

        output_args = ['-o', output_file, '-j']
        target_args = ['-l', targets_file]

        cmd = ['nuclei'] + (extra_args or []) + shlex.split(assignment['config']['args']) + timing_args + output_args + target_args
        return self._execute(cmd, output_file)

    def run(self, assignment):
        """run the agent"""

        super().run(assignment)
        ret = 0

        if assignment['targets'] and self.loop:
            ret |= self.run_scan(assignment, targets, 'targets', 'output')
        return ret

    def terminate(self):  # pragma: no cover  ; not tested / running over multiprocessing
        """terminate scanner if running"""

        self.loop = False
        self._terminate()
