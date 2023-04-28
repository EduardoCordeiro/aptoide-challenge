def calculate_discount(number_transactions: int) -> int:
    if number_transactions >= 1:
        return 5
    elif number_transactions >= 10:
        return 10
    else:
        return 0
