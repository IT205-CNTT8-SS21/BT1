import logging
import os

# Cấu hình logging theo định dạng yêu cầu
logging.basicConfig(
    filename="momo_transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class InvalidAmountError(Exception):
    """Ngoại lệ xảy ra khi số tiền giao dịch nhỏ hơn hoặc bằng 0."""

    pass


class InsufficientBalanceError(Exception):
    """Ngoại lệ xảy ra khi số dư ví không đủ để thực hiện chuyển tiền."""

    pass


class Wallet:
    """Lớp quản lý số dư và các giao dịch của Ví MoMo."""

    def __init__(self):
        """Khởi tạo ví với số dư mặc định là 0 VNĐ."""
        self._balance = 0

    @property
    def balance(self):
        """Lấy số dư hiện tại của ví."""
        return self._balance

    def deposit(self, amount: float):
        """Nạp tiền vào ví.

        Args:
            amount (float): Số tiền cần nạp.

        Raises:
            InvalidAmountError: Nếu số tiền nạp <= 0.
        """
        if amount <= 0:
            logging.error(
                f"InvalidAmountError: Attempted to process {amount} VND."
            )
            raise InvalidAmountError("Số tiền giao dịch phải lớn hơn 0.")

        self._balance += amount
        logging.info(
            f"Deposit successful: +{amount} VND. "
            f"Current Balance: {self._balance}"
        )

    def transfer(self, phone: str, amount: float):
        """Chuyển tiền tới số điện thoại khác.

        Args:
            phone (str): Số điện thoại người nhận (10 chữ số).
            amount (float): Số tiền cần chuyển.

        Raises:
            InvalidAmountError: Nếu số tiền chuyển <= 0.
            InsufficientBalanceError: Nếu số tiền chuyển vượt quá số dư.
        """
        if amount <= 0:
            logging.error(
                f"InvalidAmountError: Attempted to process {amount} VND."
            )
            raise InvalidAmountError("Số tiền giao dịch phải lớn hơn 0.")

        if amount > self._balance:
            logging.error(
                f"InsufficientBalanceError: Attempted to transfer "
                f"{amount} VND with balance {self._balance} VND."
            )
            raise InsufficientBalanceError(
                "Giao dịch thất bại: Số dư của bạn không đủ."
            )

        # Cảnh báo giao dịch giá trị cao từ 10,000,000 VND
        if amount >= 10000000:
            logging.warning(
                f"High value transaction detected: {amount} VND to {phone}"
            )

        self._balance -= amount
        logging.info(
            f"Transfer successful: -{amount} VND to {phone}. "
            f"Current Balance: {self._balance}"
        )


def display_menu():
    """Hiển thị giao diện menu CLI của Ví MoMo."""
    print("\n========== VÍ MOMO GIẢ LẬP ==========")
    print("1. Nạp tiền vào ví")
    print("2. Chuyển tiền")
    print("3. Xem lịch sử giao dịch (Log)")
    print("4. Xem số dư hiện tại")
    print("5. Thoát chương trình")
    print("===============================================")


def handle_deposit(wallet: Wallet):
    """Xử lý luồng nghiệp vụ nạp tiền."""
    print("\n--- NẠP TIỀN VÀO VÍ ---")
    try:
        amount = float(input("Nhập số tiền cần nạp: "))
        wallet.deposit(amount)
        print(f"\nNạp tiền thành công: +{amount:,.0f} VND")
        print(f"Số dư hiện tại: {wallet.balance:,.0f} VND")
    except ValueError:
        logging.error("ValueError: Invalid numeric input for deposit.")
        print("\nLỗi: Vui lòng nhập số tiền hợp lệ.")
    except InvalidAmountError as e:
        print(f"\nLỗi: {e}")


def handle_transfer(wallet: Wallet):
    """Xử lý luồng nghiệp vụ chuyển tiền."""
    print("\n--- CHUYỂN TIỀN ---")
    phone = input("Nhập số điện thoại người nhận: ").strip()

    if len(phone) != 10 or not phone.isdigit():
        print("\nLỗi: Số điện thoại không đúng định dạng (phải gồm 10 số).")
        return

    try:
        amount = float(input("Nhập số tiền cần chuyển: "))
        wallet.transfer(phone, amount)
        print(f"\nChuyển tiền thành công tới số điện thoại {phone}.")
        print(f"Số tiền đã chuyển: {amount:,.0f} VND")
        print(f"Số dư còn lại: {wallet.balance:,.0f} VND")
    except ValueError:
        logging.error("ValueError: Invalid numeric input for transfer.")
        print("\nLỗi: Vui lòng nhập số tiền hợp lệ.")
    except (InvalidAmountError, InsufficientBalanceError) as e:
        print(f"\n{e}")
        if isinstance(e, InsufficientBalanceError):
            print(f"Số dư hiện tại: {wallet.balance:,.0f} VND")


def handle_show_logs():
    """Đọc và hiển thị nội dung file log giao dịch."""
    print("\n--- LỊCH SỬ GIAO DỊCH ---")
    log_file = "momo_transactions.log"
    if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
        print("Chưa có lịch sử giao dịch nào trong hệ thống.")
        return

    with open(log_file, "r", encoding="utf-8") as file:
        print(file.read().strip())


def handle_check_balance(wallet: Wallet):
    """Xử lý nghiệp vụ xem số dư hiện tại."""
    print("\n--- SỐ DƯ VÍ MOMO ---")
    print(f"Số dư hiện tại: {wallet.balance:,.0f} VND")
    logging.info(f"Balance checked. Current Balance: {wallet.balance}")


def main():
    """Hàm khởi chạy chính điều hướng ứng dụng CLI."""
    wallet = Wallet()

    while True:
        display_menu()
        choice = input("Chọn chức năng (1-5): ").strip()

        if choice == "1":
            handle_deposit(wallet)
        elif choice == "2":
            handle_transfer(wallet)
        elif choice == "3":
            handle_show_logs()
        elif choice == "4":
            handle_check_balance(wallet)
        elif choice == "5":
            print("\nCảm ơn bạn đã sử dụng dịch vụ")
            logging.info("System shutdown")
            break
        else:
            print("\nLỗi: Chức năng không hợp lệ. Vui lòng chọn từ 1 đến 5.")


if __name__ == "__main__":
    main()