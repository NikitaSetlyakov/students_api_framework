from typing import Optional

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

@pytest.mark.parametrize(
    'email, gender, name, phone_no, status',
    [
        pytest.param(
            'ivan@example.com',
            '',
            'Ivan Ivanov',
            '+79990001122',
            1,
            id='empty-gender',
        ),
        pytest.param(
            'ivan@example.com',
            'male',
            'Ivan Ivanov',
            '+79990001122',
            None,
            id='null-status',
        ),
    ],
)
@pytest.mark.negative
@pytest.mark.xfail(
    reason='Баг #1: POST /student возвращает HTTP 200 при gender="" и status=null'
)
@allure.title('Создание студента с некорректными gender или status')
def test_create_student_with_invalid_data(
    student_client: StudentClient,
    email: str,
    gender: str,
    name: str,
    phone_no: str,
    status: Optional[int],
) -> None:
    body = StudentBuilder.create_student(
        email=email,
        gender=gender,
        name=name,
        phone_no=phone_no,
        status=status,
    )

    response = student_client.create_new_student(body=body)

    assert_status_code(
        actual_value=response.status_code,
        expected_value=400,
        allure_step='Проверка ошибочного статус-кода',
    )

@pytest.mark.parametrize(
    'missing_field',
    [
        pytest.param('email', id='missing-email'),
        pytest.param('gender', id='missing-gender'),
        pytest.param('name', id='missing-name'),
        pytest.param('phone_no', id='missing-phone'),
        pytest.param('status', id='missing-status'),
    ],
)
@pytest.mark.negative
@pytest.mark.xfail(
    reason='Баг #2: POST /student возвращает 200 вместо 400 без обязательного поля',
)
@allure.title('Создание студента без обязательного поля')
def test_create_student_without_required_field(
    student_client: StudentClient,
    fake: Faker,
    missing_field: str,
) -> None:
    body = StudentBuilder.create_student(
        email=fake.email(),
        gender='male',
        name=f'{fake.first_name()} {fake.last_name()}',
        phone_no=fake.numerify(text='+7999#######'),
        status=1,
    )

    del body[missing_field]

    response = student_client.create_new_student(body=body)

    assert_status_code(
        actual_value=response.status_code,
        expected_value=400,
        allure_step='Проверка ошибочного статус-кода',
    )