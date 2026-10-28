import allure
import pytest

from src.clients.students_client import StudentClient
from src.utils.assert_wrappers import (
    assert_contains,
    assert_is_instance,
    assert_status_code,
    assert_eq,
)

@allure.title('Обновление существующего студента')
@pytest.mark.xfail(
    reason='Баг #5: PUT /student/{student_id} возвращает поле '
    'student.status строкой вместо числа.'
)
def test_update_student(
    student_client: StudentClient,
    created_student: int,
    updated_student_data: dict,
) -> None:
    response = student_client.update_student_data(
        student_id=created_student,
        body=updated_student_data,
    )

    assert_status_code(
        actual_value=response.status_code,
        expected_value=200,
        allure_step='Проверка статус-кода обновления студента',
    )

    data = response.json()

    assert_is_instance(data, dict)

    assert_eq(
        actual_value=data['message'],
        expected_value='Student updated successfully',
        allure_step='Проверка сообщения об успешном обновлении',
    )

    assert_contains(data, 'status')

    assert_eq(
        actual_value=data['status'],
        expected_value=1,
        allure_step='Проверка успешного статуса операции обновления',
    )

    assert_contains(data, 'student')
    student = data['student']

    assert_eq(
        actual_value=student['id'],
        expected_value=created_student,
        allure_step='Проверка сохранения ID студента',
    )

    assert_eq(
        actual_value=student['name'],
        expected_value=updated_student_data['name'],
        allure_step='Проверка обновлённого имени студента',
    )

    assert_eq(
        actual_value=student['email'],
        expected_value=updated_student_data['email'],
        allure_step='Проверка обновлённого email студента',
    )

    assert_eq(
        actual_value=student['gender'],
        expected_value=updated_student_data['gender'],
        allure_step='Проверка обновлённого gender студента',
    )

    assert_eq(
        actual_value=student['status'],
        expected_value=updated_student_data['status'],
        allure_step='Проверка обновлённого status студента',
    )
