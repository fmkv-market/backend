from myapp.application.exception.cart import CarQuantityMustBePositive, SuchItemNotInCart

type item_id = int
type item_quantity = int

class Cart:
    def __init__(self, user_id: int, total: float, id: int | None = None, quantity: int = 0) -> None:
        self.user_id = user_id
        self.id = id
        self.quantity = quantity
        self.total = total
        self.items: dict[item_id, item_quantity] = {}

    def add_item(self, id: int, quantity: int, price: float) -> None:
        if id in self.items:
            self.items[id] += quantity
        else:
            self.items[id] = quantity
        self.total += quantity * price

    def remove_item(self, id: int, price: float, quantity: int = 1) -> None:
        if id not in self.items:
            raise SuchItemNotInCart
        elif self.items[id] - quantity < 0:
            raise CarQuantityMustBePositive
        self.items[id] -= quantity
        self.total -= price * quantity
        if self.items[id] == 0:
            del self.items[id]


    def __repr__(self) -> str:
        return f"Cart(user_id={self.user_id}, id={self.id})"

