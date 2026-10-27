import allure
import pytest

from src.clients.students_client import StudentClient

@allure.title('Получение списка студентов')
def test_get_students_list(student_client: StudentClient) -> None:
    response = student_client.get_students_list()
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert isinstance(data.get('students'), list)

    for student in data['students']:
        assert isinstance(student, dict)
        assert isinstance(student['id'], int)
        assert isinstance(student['status'], int)