import pytest
from faker import Faker

from config import TestConfig
from src.clients.students_client import StudentClient

@pytest.fixture(scope='session')
def config() -> 'TestConfig':
    return TestConfig()

@pytest.fixture
def student_client(config: TestConfig) -> StudentClient:
    return StudentClient(config=config)

@pytest.fixture
def fake() -> 'Faker':
    return Faker()