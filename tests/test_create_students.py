import allure
import pytest

from faker import Faker
from src.clients.students_client import StudentClient
from src.utils.builders.student_builder import StudentBuilder
from src.utils.assert_wrappers import assert_is_instance, assert_contains, assert_status_code, assert_eq

@pytest.mark.positive
@allure.title('Создание студента с валидными данными')
def test_create_valid_student(student_client: StudentClient, fake: Faker) -> None:
    fake_email = fake.email()
    gender = 'male'
    fake_name = f'{fake.first_name()} {fake.last_name()}'
    fake_phone = fake.numerify(text="+7999#######")
    status = 1
    
    response = student_client.create_new_student(
        body=StudentBuilder.create_student(
            email=fake_email,
            gender=gender,
            name=fake_name,
            phone_no=fake_phone,
            status=status
        )
    )

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

    assert_contains(data, 'message')

    assert_eq(
        actual_value=data['message'],
        expected_value='Student created successfully',
        allure_step='Проверка сообщения об успешном создании студента',
    )

    assert_contains(data, 'student')

    student = data['student']

    assert_is_instance(
        actual_value=student,
        expected_type=dict,
        allure_step='Проверка типа объекта student',
    )

    assert_contains(student, 'email')

    assert_eq(
        actual_value=student['email'],
        expected_value=fake_email,
        allure_step='Проверка email созданного студента',
    )

    assert_contains(student, 'gender')

    assert_eq(
        actual_value=student['gender'],
        expected_value=gender,
        allure_step='Проверка пола созданного студента',
    )

    assert_contains(student, 'name')

    assert_eq(
        actual_value=student['name'],
        expected_value=fake_name,
        allure_step='Проверка имени созданного студента',
    )

    assert_contains(student, 'phone_no')

    assert_eq(
        actual_value=student['phone_no'],
        expected_value=fake_phone,
        allure_step='Проверка телефона созданного студента',
    )

    assert_contains(student, 'status')

    assert_eq(
        actual_value=student['status'],
        expected_value=status,
        allure_step='Проверка статуса созданного студента',
    )

