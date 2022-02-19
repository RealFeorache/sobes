
import json


def valid_number(value) -> bool:
    """valid_int - Check if the value is a number.

    Args:
        value: Any value to check if it's a number

    Returns:
        bool: The value is a number
    """
    try:
        value = int(value)
        return True
    except:
        return False


class Product_Sale:
    """Placeholder for a product sale / transaction."""

    price = None
    index = None
    choice_number = None
    stock = None
    qty = None
    price = None
    for_payment = None


class VendingMachine:

    def __init__(self, filename: str) -> None:
        """__init__ - Initiate the Vending Machine's products.

        Args:
            filename (str): path to file with JSON db of products
        """
        self.input_filename = filename

        with open(self.input_filename) as infile:
            self.input_json = json.loads(infile.read())
            self.products = self.input_json["items"]

        self.number_of_products_available = len(
            [x for x in self.products if x["amount"] > 0])

    def print_available_products(self) -> None:
        print("The following products are available for purchase:")
        index = 0
        for product in self.products:
            print(f"{str(index+1)}) "+product["name"] +
                  " at price "+product["price"]+" - "+str(product["amount"])+"pcs")
            index += 1

    def get_product_choice(self) -> Product_Sale:

        product = Product_Sale()

        while product.choice_number is None:

            product.choice_number = input(
                "Choose the product you wish to procure\n")
            # check if the entered value is int
            if valid_number(product.choice_number):
                product.choice_number = int(product.choice_number)
            # check if the product number is available
            if product.choice_number not in range(0, self.number_of_products_available+1):
                product.choice_number = None
            # provide error
            if product.choice_number is None:
                print("You have to enter a number between 1 and " +
                      str(self.number_of_products_available))

        product.stock = self.products[product.choice_number-1]["amount"]
        product.index = product.choice_number-1

        while product.qty is None:
            product.qty = input(
                "Choose the amount of "+self.products[product.index]["name"]+" you wish to procure\n")

            # check if the entered value is int
            if valid_number(product.qty):
                product.qty = int(product.qty)
            # have sufficient stock
            if product.qty not in range(0, product.stock+1):
                product.qty = None
            # provide error
            if product.qty is None:
                print("You have to enter a number between 1 and " +
                      str(product.stock))

        product.price = float(
            self.products[product.index]["price"].lstrip("$"))
        product.for_payment = product.qty*product.price

        return product

    def get_payment(self, product_choice: Product_Sale) -> bool:
        print(f"Total for payment is {product_choice.for_payment}$.")

        payment = None
        while payment is None:
            print(f"Left to pay: {str(product_choice.for_payment)}$")
            payment = input("How much do you wish to pay?\n")
            # check if the entered value is int
            if valid_number(payment):
                payment = int(payment)
            # provide error
            if payment is None:
                print("Please enter a number!")
                continue
            # count change
            product_choice.for_payment -= payment
            payment = None
            # if the product was fully paid, break
            if product_choice.for_payment <= 0:
                break

        change = abs(product_choice.for_payment)
        print(f"Your change is {change}$")

        return change

    def stock_transaction(self, product_choice):
        self.products[product_choice.index]["amount"] -= product_choice.qty

    def update_availability(self):
        self.input_json["items"] = self.products
        with open(self.input_filename, "w") as outfile:
            json.dump(self.input_json, outfile, ensure_ascii=False, indent=4)

    def get_purchase(self):
        self.print_available_products()
        choice = self.get_product_choice()
        change = self.get_payment(choice)
        self.stock_transaction(choice)
        self.update_availability()


vendingMachine = VendingMachine("input.json")

while True:
    vendingMachine.get_purchase()

    choice = input(
        "Do you wish to make another purchase? (Y for Yes or anything else to refuse)\n")
    if choice != "Y":
        break