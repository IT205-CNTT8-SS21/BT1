import unittest
from wallet import Wallet, InsufficientBalanceError, InvalidAmountError


class TestWallet(unittest.TestCase):
    """Lớp kiểm thử đơn vị cho các chức năng của Class Wallet."""

    def setUp(self):
        """Khởi tạo một instance Wallet mới trước mỗi ca kiểm thử."""
        self.wallet = Wallet()

    def test_deposit_success(self):
        """Kiểm tra việc nạp tiền hợp lệ có tăng số dư chính xác không."""
        self.wallet.deposit(500000)
        self.assertEqual(self.wallet.balance, 500000)

        self.wallet.deposit(10000)
        self.assertEqual(self.wallet.balance, 510000)

    def test_transfer_insufficient_balance(self):
        """Kiểm tra lỗi InsufficientBalanceError khi chuyển vượt số dư."""
        self.wallet.deposit(300000)
        with self.assertRaises(InsufficientBalanceError):
            self.wallet.transfer("0987654321", 500000)

    def test_invalid_amount(self):
        """Kiểm tra lỗi InvalidAmountError khi nạp/chuyển tiền số âm hoặc 0."""
        # Kiểm tra nạp tiền âm
        with self.assertRaises(InvalidAmountError):
            self.wallet.deposit(-100000)

        # Kiểm tra nạp số tiền bằng 0
        with self.assertRaises(InvalidAmountError):
            self.wallet.deposit(0)

        # Kiểm tra chuyển tiền âm
        self.wallet.deposit(100000)
        with self.assertRaises(InvalidAmountError):
            self.wallet.transfer("0987654321", -50000)


if __name__ == "__main__":
    unittest.main()