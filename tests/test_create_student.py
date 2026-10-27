import requests
import pytest

from src.clients.students_client import StudentClient

def test_get_students_list(student_client: StudentClient):
    response = student_client.get_students_list()
    print(response)