from dnk.models.character import Character, Employee


def test_employee_is_a_character_can_hold_customer_order(gender, ethnicity):
    employee = Employee(gender.value, ethnicity.value)
    assert isinstance(employee, Character)


def test_employee_can_hold_customer_order_and_default_is_none(
    gender, ethnicity
):
    employee = Employee(gender.value, ethnicity.value)

    assert employee.customer_order is None
