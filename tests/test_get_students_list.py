import allure

from src.clients.students_client import StudentClient
from src.utils.assert_wrappers import (
    assert_contains,
    assert_is_instance,
    assert_status_code,
)

@allure.title('Получение списка студентов')
def test_get_students_list(student_client: StudentClient) -> None:
    response = student_client.get_students_list()

    assert_status_code(
        actual_value=response.status_code,
        expected_value=200,
        allure_step='Проверка успешного статус-кода',
    )

    data = response.json()

    assert_is_instance(
        actual_value=data,
        expected_type=dict,
        allure_step='Проверка типа тела ответа',
    )

    assert_contains(data, 'students')

    students = data['students']

    assert_is_instance(
        actual_value=students,
        expected_type=list,
        allure_step='Проверка типа списка студентов',
    )

    for student in students:
        assert_is_instance(
            actual_value=student,
            expected_type=dict,
            allure_step='Проверка типа объекта студента',
        )

        assert_contains(student, 'id')
        assert_contains(student, 'status')

        assert_is_instance(
            actual_value=student['id'],
            expected_type=int,
            allure_step='Проверка типа ID студента',
        )

        assert_is_instance(
            actual_value=student['status'],
            expected_type=int,
            allure_step='Проверка типа статуса студента',
        )