import logging
import os

# Cấu hình logging theo đúng định dạng yêu cầu của đề bài
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


def deposit(wallet: dict, amount: float):
    """Nạp tiền vào ví.

    Args:
        wallet (dict): Lịch sử và thông tin ví hiện tại.
        amount (float): Số tiền cần nạp.
    """
    if amount <= 0:
        logging.error(
            f"InvalidAmountError: Attempted to process {amount} VND."
        )
        raise InvalidAmountError("Số tiền giao dịch phải lớn hơn 0.")

    wallet["balance"] += amount
    logging.info(
        f"Deposit successful: +{amount} VND. "
        f"Current Balance: {wallet['balance']}"
    )


def transfer(wallet: dict, phone: str, amount: float):
    """Chuyển tiền tới số điện thoại khác.

    Args:
        wallet (dict): Thông tin ví người gửi.
        phone (str): Số điện thoại người nhận.
        amount (float): Số tiền cần chuyển.
    """
    if amount <= 0:
        logging.error(
            f"InvalidAmountError: Attempted to process {amount} VND."
        )
        raise InvalidAmountError("Số tiền giao dịch phải lớn hơn 0.")

    if amount > wallet["balance"]:
        logging.error(
            f"InsufficientBalanceError: Attempted to transfer "
            f"{amount} VND with balance {wallet['balance']} VND."
        )
        raise InsufficientBalanceError(
            "Giao dịch thất bại: Số dư của bạn không đủ."
        )

    # Cảnh báo giao dịch giá trị cao từ 10,000,000 VND
    if amount >= 10000000:
        logging.warning(
            f"High value transaction detected: {amount} VND to {phone}"
        )

    wallet["balance"] -= amount
    logging.info(
        f"Transfer successful: -{amount} VND to {phone}. "
        f"Current Balance: {wallet['balance']}"
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


def handle_deposit(wallet: dict):
    """Xử lý luồng nghiệp vụ nạp tiền."""
    print("\n--- NẠP TIỀN VÀO VÍ ---")
    try:
        amount = float(input("Nhập số tiền cần nạp: "))
        deposit(wallet, amount)
        print(f"\nNạp tiền thành công: +{amount:,.0f} VND")
        print(f"Số dư hiện tại: {wallet['balance']:,.0f} VND")
    except ValueError:
        logging.error("ValueError: Invalid numeric input for deposit.")
        print("\nLỗi: Vui lòng nhập số tiền hợp lệ.")
    except InvalidAmountError as e:
        print(f"\nLỗi: {e}")


def handle_transfer(wallet: dict):
    """Xử lý luồng nghiệp vụ chuyển tiền."""
    print("\n--- CHUYỂN TIỀN ---")
    phone = input("Nhập số điện thoại người nhận: ").strip()

    if len(phone) != 10 or not phone.isdigit():
        print("\nLỗi: Số điện thoại không đúng định dạng (phải gồm 10 số).")
        return

    try:
        amount = float(input("Nhập số tiền cần chuyển: "))
        transfer(wallet, phone, amount)
        print(f"\nChuyển tiền thành công tới số điện thoại {phone}.")
        print(f"Số tiền đã chuyển: {amount:,.0f} VND")
        print(f"Số dư còn lại: {wallet['balance']:,.0f} VND")
    except ValueError:
        logging.error("ValueError: Invalid numeric input for transfer.")
        print("\nLỗi: Vui lòng nhập số tiền hợp lệ.")
    except (InvalidAmountError, InsufficientBalanceError) as e:
        print(f"\n{e}")
        if isinstance(e, InsufficientBalanceError):
            print(f"Số dư hiện tại: {wallet['balance']:,.0f} VND")


def handle_show_logs():
    """Đọc và hiển thị nội dung file log giao dịch."""
    print("\n--- LỊCH SỬ GIAO DỊCH ---")
    log_file = "momo_transactions.log"
    if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
        print("Chưa có lịch sử giao dịch nào trong hệ thống.")
        return

    with open(log_file, "r", encoding="utf-8") as file:
        print(file.read().strip())


def handle_check_balance(wallet: dict):
    """Xử lý nghiệp vụ xem số dư hiện tại."""
    print("\n--- SỐ DƯ VÍ MOMO ---")
    print(f"Số dư hiện tại: {wallet['balance']:,.0f} VND")
    logging.info(f"Balance checked. Current Balance: {wallet['balance']}")


def main():
    """Hàm khởi chạy chính điều hướng ứng dụng CLI."""
    # Dùng Dictionary đại diện cho Ví (Đúng kiến thức Session 11-12)
    wallet = {"balance": 0.0}

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