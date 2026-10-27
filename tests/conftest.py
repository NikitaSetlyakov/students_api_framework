import pytest

from config import TestConfig
from src.clients.students_client import StudentClient

@pytest.fixture
def config() -> 'TestConfig':
    return TestConfig()

@pytest.fixture
def student_client(config: TestConfig) -> StudentClient:
    return StudentClient(config=config)