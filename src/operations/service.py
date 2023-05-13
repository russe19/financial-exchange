def operation_data(operation):
    operation_dict = operation.first().Operation.__dict__
    side = operation_dict.get("side")
    status = operation_dict.get("status")
    count = operation_dict.get("count")
    currency_id = operation_dict.get("currency")
    user_first_id = operation_dict.get("username1")
    cost = operation_dict.get("cost")
    return operation_dict, side, status, count, currency_id, user_first_id, cost


def currency_data(currency):
    currency_dict = currency.first().Currency.__dict__
    currency_id = currency_dict.get("id")
    currency_name = currency_dict.get("name")
    currency_course = currency_dict.get("course")
    return currency_dict, currency_id, currency_name, currency_course


def user_data(user_first, username):
    user_first_dict = user_first.first().User.__dict__
    user_second_dict = username.__dict__
    u_first_balance = float(user_first_dict.get("balance"))
    u_first_id = float(user_first_dict.get("id"))
    u_second_balance = float(user_second_dict.get("balance"))
    u_second_id = float(user_second_dict.get("id"))
    return user_first_dict, user_second_dict, u_first_balance, u_first_id, u_second_balance, u_second_id
