import requests
import pytest

from src.clients.students_client import StudentClient

def test_get_students_list(student_client: StudentClient):
    response = get_student_list