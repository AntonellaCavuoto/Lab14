from dataclasses import dataclass


@dataclass()
class Order:
    order_id: int
    customer_id: int
    order_status: int
    order_date: str
    required_date: str
    shipped_date: str
    store_id: int
    staff_id: int

    def __hash__(self):
        return self.order_id

    def __eq__(self, other):
        return self.order_id == other.order_id

    def __str__(self):
        return f"{self.order_id}"
