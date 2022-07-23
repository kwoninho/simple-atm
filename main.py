import unittest


class Bank():

    def __init__(self):
        self._accounts = dict()

    def _validate_pin(self, pin: str):
        if len(pin) != 4 or not pin.isdigit():
            raise Exception("invalid pin format")

        return pin

    def open_account(self, card_num: str, pin: str, balance: int = 0):
        self._accounts[card_num] = {"pin": pin, "balance": balance}

    def get_account(self, card_num: str, pin: str):
        if card_num not in self._accounts:
            raise Exception("account not found")

        account = self._accounts.get(card_num)

        if account["pin"] != self._validate_pin(pin):
            raise Exception("invalid pin")

        return account

    def get_balance(self, card_num: str, pin: str):
        account = self.get_account(card_num, pin)
        return str(account["balance"])

    def deposit(self, card_num: str, pin: str, amount: int):
        account = self.get_account(card_num, pin)

        if amount <= 0:
            raise Exception("wrong transaction")

        account["balance"] += amount
        return account["balance"]

    def withdraw(self, card_num: str, pin: str, amount: int):
        account = self.get_account(card_num, pin)

        if amount > 0:
            raise Exception("wrong transaction")

        if (account["balance"] + amount) < 0:
            raise Exception("Insufficient account balance")

        account["balance"] += amount
        return account["balance"]


class AtmController():
    def __init__(self, bank: Bank, balance: int):
        self.bank = bank
        self.balance = balance

    def _validate_card_num(self, card_num: str):

        if len(card_num) != 19:
            raise Exception("invalid card number")

        number_parts = card_num.split("-")

        if len(number_parts) != 4:
            raise Exception("invalid card number")

        for number_part in number_parts:
            if len(number_part) != 4 or not number_part.isdigit():
                raise Exception("invalid card number")

        return card_num

    def check_balance(self, card_num: str, pin: str):
        try:
            return self.bank.get_balance(self._validate_card_num(card_num), pin)
        except Exception as e:
            return str(e)

    def deposit_and_withdrawal(self, card_num: str, pin: str, amount: int):
        try:
            if amount < 0:
                if (self.balance + amount) < 0:
                    return "Insufficient ATM balance"

                result = self.bank.withdraw(self._validate_card_num(card_num), pin, amount)
            else:
                result = self.bank.deposit(self._validate_card_num(card_num), pin, amount)

            self.balance += amount
            return str(result)
        except Exception as e:
            return str(e)

    def get_atm_balance(self):
        return str(self.balance)


class TestSimpleAtm(unittest.TestCase):

    def setUp(self) -> None:
        self.test_bank = Bank()
        self.test_bank.open_account("1111-1111-1111-1111", "1111", 0)
        self.test_bank.open_account("2222-2222-2222-2222", "2222", 50)
        self.test_bank.open_account("1111-2222-3333-4444", "1234", 500)
        self.atm_controller = AtmController(self.test_bank, 100)

    def test_validate_card_number(self):
        self.assertEqual(self.atm_controller.check_balance("1111111111111111", ""), "invalid card number")
        self.assertEqual(self.atm_controller.check_balance("1111-1111-1111-111", ""), "invalid card number")
        self.assertEqual(self.atm_controller.check_balance("1111-1111-11111111", ""), "invalid card number")
        self.assertEqual(self.atm_controller.check_balance("1111-1111-1111-11111", ""), "invalid card number")
        self.assertEqual(self.atm_controller.check_balance("1111-1111-1111", ""), "invalid card number")
        self.assertEqual(self.atm_controller.check_balance("1111-1111-1111-abcd", ""), "invalid card number")

    def test_check_balance(self):
        self.assertEqual(self.atm_controller.check_balance("1111-1111-1111-1111", "abc1"), "invalid pin format")
        self.assertEqual(self.atm_controller.check_balance("1111-1111-1111-1111", "111"), "invalid pin format")
        self.assertEqual(self.atm_controller.check_balance("1111-1111-1111-1111", "2222"), "invalid pin")
        self.assertEqual(self.atm_controller.check_balance("1111-1111-1111-4444", "4444"), "account not found")
        self.assertEqual(self.atm_controller.check_balance("1111-1111-1111-1111", "1111"), "0")
        self.assertEqual(self.atm_controller.check_balance("2222-2222-2222-2222", "2222"), "50")
        self.assertEqual(self.atm_controller.check_balance("1111-2222-3333-4444", "1234"), "500")

    def test_deposit_and_withdrawal(self):
        self.assertEqual(self.atm_controller.deposit_and_withdrawal("1111-1111-1111-1111", "1111", 50), "50")
        self.assertEqual(self.atm_controller.get_atm_balance(), "150")

        self.assertEqual(self.atm_controller.deposit_and_withdrawal("1111-1111-1111-1111", "1111", -50), "0")
        self.assertEqual(self.atm_controller.get_atm_balance(), "100")

        self.assertEqual(self.atm_controller.deposit_and_withdrawal("2222-2222-2222-2222", "2222", -51),
                         "Insufficient account balance")

        self.assertEqual(self.atm_controller.deposit_and_withdrawal("1111-2222-3333-4444", "1234", 500), "1000")
        self.assertEqual(self.atm_controller.get_atm_balance(), "600")

        self.assertEqual(self.atm_controller.deposit_and_withdrawal("1111-2222-3333-4444", "1234", -700),
                         "Insufficient ATM balance")

        self.assertEqual(self.atm_controller.deposit_and_withdrawal("2222-2222-2222-2222", "2222", 1050), "1100")
        self.assertEqual(self.atm_controller.get_atm_balance(), "1650")

        self.assertEqual(self.atm_controller.deposit_and_withdrawal("1111-2222-3333-4444", "1234", -700), "300")
        self.assertEqual(self.atm_controller.get_atm_balance(), "950")


if __name__ == '__main__':
    unittest.main()