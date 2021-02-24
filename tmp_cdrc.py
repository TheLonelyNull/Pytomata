from overlap_tester import get_test_cases
import re


class CDRC:
    __instance = None
    _cdrc_cases = None

    @staticmethod
    def get_instance() -> 'CDRC':
        if CDRC.__instance is None:
            CDRC()
        return CDRC.__instance

    def __init__(self):
        """Private Constructor"""
        if CDRC.__instance is not None:
            raise Exception("This Class is a Singleton. Use get_instance instead.")
        else:
            CDRC.__instance = self
            self._cdrc_cases = get_test_cases('ampl_cdrc2.test')

    def is_in_cdrc(self, case):
        case = case.rstrip()
        case = case.lstrip()
        case = re.sub(r"\s+", "", case)
        return  case in self._cdrc_cases
