class CustomStep:
    def __init__(self, config, file_manager):
        self.config = config
        self.file_manager = file_manager

    def run(self):
        raise NotImplementedError("O CustomStep deve implementar o método run.")