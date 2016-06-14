from analyzer import Analyzer
from bug_finder import BugFinder
from exploiter import Exploiter
import logging
from verifier import Verifier

l = logging.getLogger("aegg.aegg")


class AEGG(object):
    def __init__(self, binary):
        self.binary = binary
        self.payloads = []

        self.bug_finder = BugFinder(binary)
        self.analyzer = Analyzer()
        self.exploiter = Exploiter()
        self.verifier = Verifier(binary)

    def exploit_gen(self, path):
        analysis = self.analyzer.analyze(path)
        payload = self.exploiter.generate(path, analysis)
        if self.verifier.verify(payload):
            self.payloads.append(payload)
            return True
        return False

    def hunt(self, n=None, paths=None):
        """
        n: number paths want to check
        paths: angr path object, TODO: an input instead of path
        """
        n = 1 if n is None else n
        paths = [] if paths is None else paths

        l.info('Start hunting ...')
        while len(paths) < n:
            l.info('Bug finding ...')
            found_paths = self.bug_finder.find()
            if found_paths is None:
                break
            l.info('Found: %s' % paths)
            paths.extend(found_paths)
        for path in paths:
            self.exploit_gen(paths)
        l.info('Completed.')
