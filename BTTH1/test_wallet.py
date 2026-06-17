import unittest
from wallet import (
    deposit,
    transfer,
    InvalidAmountError,
    InsufficientBalanceError,
)


class TestWalletFunctions(unittest.TestCase):

    def test_deposit_success(self):
        """Kiểm tra nạp tiền đúng có tăng số dư không."""
        wallet = {"balance": 0.0}
        deposit(wallet, 500000)
        self.assertEqual(wallet["balance"], 500000)

    def test_transfer_insufficient_balance(self):
        """Kiểm tra hàm chuyển tiền có raise InsufficientBalanceError."""
        wallet = {"balance": 100000.0}
        with self.assertRaises(InsufficientBalanceError):
            transfer(wallet, "0987654321", 200000)

    def test_invalid_amount(self):
        """Kiểm tra xem có raise InvalidAmountError khi nạp tiền âm không."""
        wallet = {"balance": 0.0}
        with self.assertRaises(InvalidAmountError):
            deposit(wallet, -5000)


if __name__ == "__main__":
    unittest.main()