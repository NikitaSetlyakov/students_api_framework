import allure
import pytest

from faker import Faker
from src.clients.students_client import StudentClient
from src.utils.builders.student_builder import StudentBuilder

def test_create_valid_user(student_client: StudentClient, fake: Faker) -> None:
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

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert data.get('message') == "Student created successfully"

    student = data.get('student')
    assert isinstance(student, dict)
    
    assert student['email'] == fake_email
    assert student['gender'] == gender
    assert student['name'] == fake_name
    assert student['phone_no'] == fake_phone
    assert student['status'] == status