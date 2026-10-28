from typing import Generator

import pytest
from faker import Faker

from config import TestConfig
from src.utils.assert_wrappers import assert_status_code
from src.clients.students_client import StudentClient
from src.utils.builders.student_builder import StudentBuilder

@pytest.fixture(scope='session')
def config() -> 'TestConfig':
    return TestConfig()

@pytest.fixture
def student_client(
    config: TestConfig,
) -> StudentClient:
    return StudentClient(config=config)

@pytest.fixture
def fake() -> 'Faker':
    return Faker()

@pytest.fixture
def student_data(
    fake: Faker,
) -> dict:
    return StudentBuilder.create_student(
        email=fake.email(),
        gender='male',
        name=f'{fake.first_name()} {fake.last_name()}',
        phone_no=fake.numerify(text='+7999#######'),
        status=1,
    )

@pytest.fixture
def updated_student_data(
    fake: Faker,
) -> dict:
    return StudentBuilder.update_student(
        email=fake.email(),
        gender='female',
        name=f'{fake.first_name()} {fake.last_name()}',
        status=0,
    )

@pytest.fixture
def created_student(
    student_client: StudentClient, 
    student_data: dict,
) -> Generator[int, None, None]:

    create_student = student_client.create_new_student(
        body=student_data
    )

    assert_status_code(
        actual_value=create_student.status_code,
        expected_value=200,
        allure_step='Проверка успешного статус-кода'
    )

    student_id = create_student.json()['student']['id']

    yield student_id

    delete_student = student_client.delete_student(
        student_id=student_id
    )

    assert_status_code(
        actual_value=delete_student.status_code,
        expected_value=200,
        allure_step='Проверка успешного статус-кода'
    )