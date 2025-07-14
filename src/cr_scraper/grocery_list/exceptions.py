class GroceryElementError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NegativeQuantityError(GroceryElementError):
    def __init__(self, *args: object) -> None:
        self.msg = "Cannot create grocery with negative quantity"
        super().__init__(self.msg, *args)


class MismatchError(GroceryElementError):
    def __init__(self, *args: object) -> None:
        self.msg = "Objects are not of the same kind"
        super().__init__(*args)


class CannotConvertError(GroceryElementError):
    def __init__(self, *args: object) -> None:
        self.msg = "Unit cannot be converted"
        super().__init__(*args)
