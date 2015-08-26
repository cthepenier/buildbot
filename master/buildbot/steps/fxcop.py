import re

from buildbot.steps.shell import ShellCommand
from buildbot.status.results import SUCCESS
from buildbot.status.results import WARNINGS

class FxCop(ShellCommand):

    ''' A Step to run FxCop analysis '''

    name = "FxCop"
    haltOnFailure = True

    def __init__(self, fxcop_path, project_path,**kwargs):
        self.warnings = 0
        ShellCommand.__init__(self, **kwargs)

        command = [fxcop_path, '/project:"{0}"'.format(project_path), '/console']
        self.setCommand(command)

    def createSummary(self, log):
        warningPattern = re.compile('^.* : warning  : CA\d+ :')
        warnings = []

        for line in log.getText().split('\n'):
            if warningPattern.match(line):
                warnings.append(line)
                self.warnings += 1

        if self.warnings > 0:
            self.addCompleteLog('warnings', "\n".join(warnings))

        self.step_status.setStatistic('warnings', self.warnings)

    def evaluateCommand(self, cmd):
        if self.warnings:
            return WARNINGS
        else:
            return SUCCESS

    def describe(self, done=False):
        if not done:
            return ["running fxcop"]

        description = [self.name]
        return description
