import allure
import pytest

from src.clients.students_client import StudentClient
from src.utils.assert_wrappers import (
    assert_is_instance, 
    assert_contains, 
    assert_status_code, 
    assert_eq,
)

@allure.title('Удаление существующего студента')
def test_delete_student(student_client: StudentClient, created_student: int) -> None:
    delete_response = student_client.delete_student(
        student_id=created_student,
    )

    assert_status_code(
        actual_value=delete_response.status_code,
        expected_value=200,
        allure_step='Проверка успешного статус-кода',
    )

    data = delete_response.json()

    assert_eq(
        actual_value=data['message'],
        expected_value="Student deleted successfully",
        allure_step='Проверка успешного удаления студента'
    )

    assert_contains(
        actual_value=data,
        expected_item='status',
        allure_step='Проверка присутствия ключа status в ответе'
    )

    assert_eq(
        actual_value=data['status'],
        expected_value=1,
        allure_step='Проверка значения ключа status'
    )

    get_response = student_client.get_student_by_id(
        student_id=created_student
    )

    assert_status_code(
        actual_value=get_response.status_code,
        expected_value=200,
        allure_step="Проверка статус-кода после удаления",
    )

    get_data = get_response.json()

    assert_eq(
        actual_value=get_data["message"],
        expected_value="Student not found",
        allure_step="Проверка сообщения об отсутствии студента",
    )

    assert_eq(
        actual_value=get_data["status"],
        expected_value=0,
        allure_step="Проверка статуса отсутствующего студента",
    )

@allure.title('Удаление несуществующего студента')
@pytest.mark.negative
@pytest.mark.xfail(
    reason='Баг №4: DELETE /student/{student_id} возвращает сообщение ' 
    'об успешном удалении для уже удалённого студента'
)
def test_delete_nonexistent_student(
    student_client: StudentClient,
    created_student: int,
) -> None:
    delete_response = student_client.delete_student(
        student_id=created_student,
    )

    assert_status_code(
        actual_value=delete_response.status_code,
        expected_value=200,
        allure_step='Проверка статус-кода первого удаления',
    )

    assert_eq(
        actual_value=delete_response.json()['status'],
        expected_value=1,
        allure_step='Проверка успешного первого удаления',
    )

    response = student_client.delete_student(
        student_id=created_student,
    )

    assert_status_code(
        actual_value=response.status_code,
        expected_value=200,
        allure_step='Проверка статус-кода удаления несуществующего студента',
    )

    data = response.json()

    assert_is_instance(data, dict)

    assert_contains(data, 'message')
    assert_contains(data, 'status')

    assert_eq(
        actual_value=data['message'],
        expected_value='Student not found',
        allure_step='Проверка сообщения об отсутствии студента',
    )

    assert_eq(
        actual_value=data['status'],
        expected_value=0,
        allure_step='Проверка статуса удаления несуществующего студента',
    )

    