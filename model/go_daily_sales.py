from dataclasses import dataclass

#from model.studente import Studente


@dataclass
class GoSales:
    Retailer_code: int
    Product_number: int
    Order_method_code: int
    Date: str
    Quantity: float
    Unit_price: float
    Unit_sale_price: float

    def __str__(self):
        return f"{self.Retailer_code} - {self.Product_number} - {self.Order_method_code}"

    def __eq__(self, other):
        return (self.Retailer_code, self.Order_method_code, self.Product_number) == (other.Retailer_code, self.Order_method_code, self.Product_number)


    def __hash__(self):
        return hash((self.Retailer_code, self.Order_method_code, self.Product_number))