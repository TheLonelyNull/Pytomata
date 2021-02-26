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
        self._LR_type = args[0]
        self._grammar_file = args[1]
        self._draw_graph = args[2]
        self._test_suite_type = args[3]
        self._output_file_name = args[4]
        self._classic = args[5]
        self._classic_improved = args[6]
        self._seed = args[7]

    def should_produce_graph(self):
        return self._draw_graph

    def get_automaton_type(self):
        return self._LR_type

    def get_grammar_filename(self):
        return self._grammar_file

    def get_test_suite_type(self):
        return self._test_suite_type

    def should_output_to_file(self):
        return self._output_file_name is not None

    def get_output_filename(self):
        return self._output_file_name

    def get_clasic_flag(self):
        return self._classic

    def get_classic_improved_flag(self):
        return self._classic_improved

    def get_seed(self):
        if self._seed is None:
            return 1
        return self._seed
