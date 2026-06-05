class TurboEnvError(Exception):
    message = "An error occurred in TurboEnv."


class MissingEnvVariableError(TurboEnvError):
    message = "The specified environment variable is missing: {values}"

    def __init__(self, *values: str):
        self.values = ', '.join(values)
        message = self.message.format(values=self.values)
        super().__init__(message)
