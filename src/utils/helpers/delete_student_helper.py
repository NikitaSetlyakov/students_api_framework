from src.utils.assert_wrappers import (
    assert_contains,
    assert_eq
)

def assert_student_not_found(data: dict) -> None:
    assert_contains(data, "message")
    assert_contains(data, "status")

    assert_eq(
        actual_value=data["message"],
        expected_value="Student not found",
        allure_step="Проверка сообщения об отсутствии студента",
    )

    assert_eq(
        actual_value=data["status"],
        expected_value=0,
        allure_step="Проверка статуса отсутствующего студента",
    )