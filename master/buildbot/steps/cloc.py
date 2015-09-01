import re

from buildbot.steps.shell import ShellCommand
from buildbot.status.results import SUCCESS

class Cloc(ShellCommand):

    ''' A Step to display LOC counter '''

    name = "cloc"
    haltOnFailure = True

    def __init__(self, cloc_path, targets, exclude_dirs=[], exclude_exts=[], **kwargs):
        ShellCommand.__init__(self, **kwargs)

        command = [cloc_path]
        if exclude_dirs:
            command.append('--exclude-dir={0}'.format(','.join(exclude_dirs)))
        if exclude_exts:
            command.append('--exclude-ext={0}'.format(','.join(exclude_exts)))
        command.extend(targets)
        self.setCommand(command)
        self.description = [self.name]

    def createSummary(self, log):

        csharp_loc_pattern = re.compile(r'^C#\s+\d+\s+\d+\s+\d+\s+(\d+)')
        total_loc_pattern = re.compile(r'^SUM:\s+\d+\s+\d+\s+\d+\s+(\d+)')

        for line in log.getText().split('\n'):
            m = csharp_loc_pattern.match(line)
            if m:
                self.description.append('C# LOC : {0}'.format(m.group(1)))
            m = total_loc_pattern.match(line)
            if m:
                self.description.append('Total LOC : {0}'.format(m.group(1)))

    def evaluateCommand(self, cmd):
        return SUCCESS

    def describe(self, done=False):
        if not done:
            return ["running", "cloc"]

        return self.description
