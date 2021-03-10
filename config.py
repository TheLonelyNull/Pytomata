import input_validator


class Config:
    __instance = None

    @staticmethod
    def get_instance() -> 'Config':
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        """Private Constructor"""
        if Config.__instance is not None:
            raise Exception("This Class is a Singleton. Use get_instance instead.")
        else:
            Config.__instance = self
            self._get_args()

    def _get_args(self):
        args = input_validator.parse_args()
        self._args = args

    def should_produce_graph(self):
        return self._args['graph']

    def get_automaton_type(self):
        return self._args['lr']

    def get_grammar_filename(self):
        return self._args['input_file']

    def get_test_suite_type(self):
        return self._args['coverage']

    def should_output_to_file(self):
        return self._args['output_file'] is not None

    def get_output_filename(self):
        return self._args['output_file']

    def get_clasic_flag(self):
        return self._args['classic']

    def get_classic_improved_flag(self):
        return self._args['classicimproved']

    def get_seed(self):
        return self._args['seed']

    def get(self, str):
        if str not in self._args:
            return None
        return self._args[str]