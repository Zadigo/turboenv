class TurboEnvError(Exception):
    message = "An error occurred in TurboEnv."


class MissingEnvVariableError(TurboEnvError):
    message = "The specified environment variable is missing: {values}"

    def __init__(self, *values: str):
        self.values = ', '.join(values)
        message = self.message.format(values=self.values)
        super().__init__(message)


class ConditionalError(TurboEnvError):
    message = "A conditional check failed: {details}"

    def __init__(self, value: str, expected: str, condition: str):
        self.details = f"Expected {value} {condition} {expected}"
        message = self.message.format(details=self.details)
        super().__init__(message)
