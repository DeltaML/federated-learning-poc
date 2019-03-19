class InvalidModelException(Exception):
    def __init__(self, model_type, status_code=400):
        message = "Invalid model type {}".format(model_type)
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.status_code = status_code
