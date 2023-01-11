class model_creation_request:
    def __init__(
            self,
            model,
            params,
            d,
            n_classes,
    ):
        self.model = model
        self.params = params
        self.num_features = d
        self.num_classes = n_classes
