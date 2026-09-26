from abc import ABC, abstractmethod


# Task 1: Payment Method Hierarchy

class PaymentMethod(ABC):

    @abstractmethod
    def get_details(self) -> str:
        pass

    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass


class RazorpayCardPayment(PaymentMethod):

    def __init__(self, card_number, card_holder, expiry_date):
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiry_date = expiry_date

    def get_details(self):
        return f"Razorpay Card - {self.card_holder}, ****{self.card_number[-4:]}, {self.expiry_date}"

    def pay(self, amount):
        print(f"Paid {amount} using Razorpay Card.")
        return True


class RazorpayUPIPayment(PaymentMethod):

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def get_details(self):
        return f"Razorpay UPI - {self.upi_id}"

    def pay(self, amount):
        print(f"Paid {amount} using Razorpay UPI.")
        return True


class StripeCardPayment(PaymentMethod):

    def __init__(self, card_number, card_holder, expiry_date):
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiry_date = expiry_date

    def get_details(self):
        return f"Stripe Card - {self.card_holder}, ****{self.card_number[-4:]}, {self.expiry_date}"

    def pay(self, amount):
        print(f"Paid {amount} using Stripe Card.")
        return True


class StripeUPIPayment(PaymentMethod):

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def get_details(self):
        return f"Stripe UPI - {self.upi_id}"

    def pay(self, amount):
        print(f"Paid {amount} using Stripe UPI.")
        return True


# Task 2: Payment Method Factory

class FactoryPaymentMethod(ABC):

    factory = {}

    @classmethod
    def get_payment_object(cls, method_type, **kwargs):
        if method_type in cls.factory:
            return cls.factory[method_type](**kwargs)
        else:
            raise ValueError(f"Payment type '{method_type}' not supported.")


class RazorpayFactory(FactoryPaymentMethod):

    factory = {
        "card": RazorpayCardPayment,
        "upi": RazorpayUPIPayment
    }


class StripeFactory(FactoryPaymentMethod):

    factory = {
        "card": StripeCardPayment,
        "upi": StripeUPIPayment
    }


# Task 3: Aggregator Hierarchy

class Aggregator(ABC):

    def __init__(self, name, processing_fee):
        self.name = name
        self.processing_fee = processing_fee

    @abstractmethod
    def call_get_payment_object(self, method_type, amount, **kwargs):
        pass


class RazorpayAggregator(Aggregator):

    def __init__(self):
        super().__init__("Razorpay", 0.02)
        self.factory = RazorpayFactory

    def call_get_payment_object(self, method_type, amount, **kwargs):
        payment_obj = self.factory.get_payment_object(method_type, **kwargs)

        final_amount = amount * (1 + self.processing_fee)

        print(f"Gateway: {self.name}")
        print(f"Amount: {amount}")
        print(f"Processing fee: {self.processing_fee * 100}%")
        print(f"Final amount: {final_amount}")

        return payment_obj.pay(final_amount)


class StripeAggregator(Aggregator):

    def __init__(self):
        super().__init__("Stripe", 0.029)
        self.factory = StripeFactory

    def call_get_payment_object(self, method_type, amount, **kwargs):
        payment_obj = self.factory.get_payment_object(method_type, **kwargs)

        final_amount = amount * (1 + self.processing_fee)

        print(f"Gateway: {self.name}")
        print(f"Amount: {amount}")
        print(f"Processing fee: {self.processing_fee * 100}%")
        print(f"Final amount: {final_amount}")

        return payment_obj.pay(final_amount)


# Task 4: Aggregator Factory

class AggregatorFactory:

    factory = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator
    }

    @classmethod
    def get_aggregator_object(cls, aggregator_name):
        if aggregator_name in cls.factory:
            return cls.factory[aggregator_name]()
        else:
            raise ValueError(
                f"Aggregator '{aggregator_name}' not supported."
            )


# Task 5: CLI Client Workflow

def main():

    print("Multi-Gateway Payment Processing Engine")

    try:
        aggregator_name = input(
            "Select Aggregator (stripe/razorpay): "
        ).lower().strip()

        if aggregator_name not in AggregatorFactory.factory:
            raise ValueError("Invalid aggregator.")

        method_type = input(
            "Select Method (card/upi): "
        ).lower().strip()

        if method_type not in ["card", "upi"]:
            raise ValueError("Invalid payment method.")

        amount = float(input("Enter Amount: "))

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if method_type == "card":
            card_number = input("Enter Card Number: ")
            card_holder = input("Enter Card Holder Name: ")
            expiry_date = input("Enter Expiry Date: ")

            kwargs = {
                "card_number": card_number,
                "card_holder": card_holder,
                "expiry_date": expiry_date
            }

        else:
            upi_id = input("Enter UPI ID: ")

            kwargs = {
                "upi_id": upi_id
            }

        aggregator = AggregatorFactory.get_aggregator_object(
            aggregator_name
        )

        success = aggregator.call_get_payment_object(
            method_type,
            amount,
            **kwargs
        )

        if success:
            print("Payment Successful!")
        else:
            print("Payment Failed!")

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
