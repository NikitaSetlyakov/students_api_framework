import allure
import pytest

from src.clients.students_client import StudentClient
from src.utils.assert_wrappers import (
    assert_is_instance, 
    assert_contains, 
    assert_status_code, 
    assert_eq,
)

@allure.title('Проверка получения студента по ID')
def test_get_student_by_id(
    student_client: StudentClient,
    created_student: int,
    student_data: dict,
) -> None:
    student_id = created_student

    response = student_client.get_student_by_id(student_id=student_id)

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
    assert_contains(student, 'gender')
    assert_contains(student, 'name')
    assert_contains(student, 'phone_no')
    assert_contains(student, 'status')
    assert_contains(student, 'email')

    assert_eq(
        actual_value=student['id'],
        expected_value=student_id,
        allure_step='Проверка ID полученного студента',
    )   

    assert_eq(
        actual_value=student['email'],
        expected_value=student_data['email'],
        allure_step='Проверка email полученного студента',
    )

    assert_eq(
        actual_value=student['gender'],
        expected_value=student_data['gender'],
        allure_step='Проверка gender полученного студента',
    )

    assert_eq(
        actual_value=student['name'],
        expected_value=student_data['name'],
        allure_step='Проверка name полученного студента',
    )

    assert_eq(
        actual_value=student['phone_no'],
        expected_value=student_data['phone_no'],
        allure_step='Проверка phone_no полученного студента',
    )

    assert_eq(
        actual_value=student['status'],
        expected_value=student_data['status'],
        allure_step='Проверка status полученного студента',
    )

@allure.title('Получение студента по ID после удаления')
@pytest.mark.negative
@pytest.mark.xfail(
    reason='Баг #3: Получение удалённого студента' 
    ' по ID возвращает HTTP 200 OK.'
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
        allure_step='Проверка статуса ошибки в теле ответа',
    )