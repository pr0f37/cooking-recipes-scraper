class GroceryElementError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NegativeQuantityError(GroceryElementError):
    def __init__(self, *args: object) -> None:
        self.msg = "Cannot create grocery with negative quantity"
        super().__init__(self.msg, *args)
