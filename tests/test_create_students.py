from typing import Optional

import allure
import pytest

from src.utils.assert_wrappers import (
    assert_contains,
    assert_eq,
    assert_is_instance,
    assert_status_code,
)
from src.utils.builders.student_builder import StudentBuilder
from src.utils.helpers.student_assertions import assert_student_fields
from src.clients.students_client import StudentClient

pytestmark = [
    allure.feature("Создание данных о студенте"),
    allure.suite("Тесты на создание данных о студенте"),
]

@allure.title('Создание студента с валидными данными')
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_create_valid_student(
    student_client: StudentClient, 
    student_data: dict,
) -> None:
    response = student_client.create_new_student(body=student_data)

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

    assert_student_fields(
        student=student,
        expected_data=student_data,
    )

@allure.title('Создание студента с некорректными gender или status')
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
@pytest.mark.regression
@pytest.mark.xfail(
    reason='Баг #1: POST /student возвращает HTTP 200 ' 
    'при gender="" и status=null',
    strict=True,
)
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

@allure.title('Создание студента без обязательного поля')
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
@pytest.mark.regression
@pytest.mark.xfail(
    reason='Баг #2: POST /student возвращает 200 ' 
    'вместо 400 без обязательного поля',
    strict=True,
)
def test_create_student_without_required_field(
    student_client: StudentClient,
    student_data: dict,
    missing_field: str,
) -> None:
    body = student_data.copy()

    del body[missing_field]

    response = student_client.create_new_student(body=body)

    assert_status_code(
        actual_value=response.status_code,
        expected_value=400,
        allure_step='Проверка ошибочного статус-кода',
    )