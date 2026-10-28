import allure
import pytest

from src.clients.students_client import StudentClient
from src.utils.helpers.student_assertions import (
    assert_student_not_found,
    assert_student_fields
)
from src.utils.assert_wrappers import (
    assert_is_instance, 
    assert_contains, 
    assert_status_code, 
    assert_eq,
)

@allure.title('Проверка получения студента по ID')
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.xfail(
    reason='Баг #7: GET /student/{id} иногда возвращает "Student not found"' 
    ' сразу после успешного POST /student',
)
def test_get_student_by_id(
    student_client: StudentClient,
    created_student: int,
    student_data: dict,
) -> None:
    response = student_client.get_student_by_id(student_id=created_student)

    assert_status_code(
        actual_value=response.status_code,
        expected_value=200,
        allure_step='Проверка успешного статус-кода'
    )

    data = response.json()

    assert_is_instance(data, dict)

    assert_contains(
        actual_value=data,
        expected_item='student',
        allure_step='Проверка наличия созданного студента в ответе',
    )

    student = data['student']

    assert_is_instance(
        actual_value=student,
        expected_type=dict,
        allure_step='Проверка типа объекта student',
    )

    assert_contains(student, 'id')

    assert_eq(
        actual_value=student['id'],
        expected_value=created_student,
        allure_step='Проверка ID полученного студента',
    )

    assert_student_fields(
        student=student,
        expected_data=student_data,
    )

@allure.title('Получение студента по ID после удаления')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.xfail(
    reason='Баг #3: Получение удалённого студента' 
    ' по ID возвращает HTTP 200 OK.',
    strict=True,
)
def test_get_deleted_student_by_id(
    student_client: StudentClient,
    student_data: dict,
) -> None:
    create_response = student_client.create_new_student(body=student_data)

    assert_status_code(
        actual_value=create_response.status_code,
        expected_value=200,
        allure_step='Проверка статус-кода создания студента',
    )

    student_id = create_response.json()['student']['id']

    delete_response = student_client.delete_student(student_id=student_id)

    assert_status_code(
        actual_value=delete_response.status_code,
        expected_value=200,
        allure_step='Проверка статус-кода удаления студента',
    )

    response = student_client.get_student_by_id(student_id=student_id)

    assert_status_code(
        actual_value=response.status_code,
        expected_value=404,
        allure_step='Проверка статус-кода получения удалённого студента',
    )

    data = response.json()

    assert_is_instance(
        actual_value=data,
        expected_type=dict,
        allure_step='Проверка типа тела ошибки',
    )

    assert_student_not_found(data)