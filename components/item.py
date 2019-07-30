class Item:
    def __init__(self,
                 use_function=None,
                 targeting=None,
                 targeting_message=None,
                 quantity=1,
                 droppable=True,
                 **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.quantity = quantity
        self.droppable = droppable
        self.max_quantity = 99
        self.function_kwargs = kwargs