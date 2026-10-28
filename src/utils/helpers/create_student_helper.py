from typing import Any

from src.utils.assert_wrappers import (
    assert_contains,
    assert_eq,
    assert_is_instance,
)


def assert_student_fields(
    student: dict[str, Any],
    expected_data: dict[str, Any],
) -> None:
    expected_fields = {
        "email": expected_data["email"],
        "gender": expected_data["gender"],
        "name": expected_data["name"],
        "phone_no": expected_data["phone_no"],
        "status": expected_data["status"],
    }

    assert_is_instance(
        actual_value=student,
        expected_type=dict,
        allure_step="Проверка типа объекта student",
    )

    for field_name, expected_value in expected_fields.items():
        assert_contains(
            student,
            field_name,
        )

        assert_eq(
            actual_value=student[field_name],
            expected_value=expected_value,
            allure_step=f"Проверка значения поля '{field_name}'",
        )