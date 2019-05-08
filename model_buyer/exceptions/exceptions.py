class OrderedModelNotFoundException(Exception):
    def __init__(self, model_id, status_code=404):
        message = "Not found ordered model {}".format(model_id)
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.status_code = status_code
