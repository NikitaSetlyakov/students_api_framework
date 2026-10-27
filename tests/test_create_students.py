import allure
import pytest


from src.clients.students_client import StudentClient
from src.utils.builders.student_builder import StudentBuilder

def test_create_valid_user(student_client: StudentClient) -> None:
    fake_email 
    response = student_client.create_new_student(
        body=StudentBuilder.create_student(
            email=
        ))