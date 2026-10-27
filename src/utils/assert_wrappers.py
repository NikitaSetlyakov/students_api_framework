from typing import Any, Optional

import allure

def assert_eq(
    actual_value: Any,
    expected_value: Any,
    allure_step: str = 'Сравнение ожидаемого результата с фактическим',
    error_msg: Optional[str] = None,
) -> None:
    with allure.step(allure_step):
        assert actual_value == expected_value, error_msg or (
            f"Значения не равны: "
            f"ожидалось {expected_value}, "
            f"получено {actual_value}"
        )

def assert_is_instance(
    actual_value: Any,
    expected_type: type,
    allure_step: str = 'Проверка типа значения',
    error_msg: Optional[str] = None,
) -> None:
    with allure.step(allure_step):
        assert isinstance(actual_value, expected_type), error_msg or (
            f"Неверный тип: ожидался {expected_type}, "
            f"получен {type(actual_value)}. "
            f"Значение: {actual_value}"
        )

def assert_contains(
    actual_value: Any,
    expected_item: Any,
    allure_step: str = 'Проверка присутствия элемента',
    error_msg: Optional[str] = None,
) -> None:
    with allure.step(allure_step):
        assert expected_item in actual_value, error_msg or (
            f"Элемент {expected_item} отсутствует в {actual_value}"
        )

def assert_status_code(
    actual_value: int,
    expected_value: int,
    allure_step: str = 'Проверка статуса ответа',
    error_msg: Optional[str] = None,
) -> None:
    with allure.step(allure_step):
        assert actual_value == expected_value, error_msg or (
            f"Неверный статус-код: ожидался {expected_value}, "
            f"получен {actual_value}"
        )