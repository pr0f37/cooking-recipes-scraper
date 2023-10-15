class GroceryElementError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NegativeQuantityError(GroceryElementError):
    def __init__(self, *args: object) -> None:
        self.msg = "Cannot create grocery with negative quantity"
        super().__init__(self.msg, *args)


class TermMismatchError(GroceryElementError):
    def __init__(self, *args: object) -> None:
        self.msg = "Two objects you are trying to sum up are not of the same kind"
        super().__init__(*args)
