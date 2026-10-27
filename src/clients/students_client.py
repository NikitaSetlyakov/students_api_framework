import requests

from config import TestConfig 

class StudentRoutes:
    STUDENTS = '/student'
    STUDENTS_BY_ID = '/student/{student_id}'
    
class StudentClient:
    def __init__(self, config: TestConfig):
        self.config = config

    def get_students_list(self) -> requests.Response:
        response = requests.get(
            url=f'{self.config.BASE_URL}{StudentRoutes.STUDENTS}',
        )
        return response
    
    def create_new_student(self, body: dict) -> requests.Response:
        response = requests.post(
            url=f'{self.config.BASE_URL}{StudentRoutes.STUDENTS}', json=body,
        )
        return response
    
    def delete_student(self, student_id: int) -> requests.Response:
        response = requests.delete(
            url=f'{self.config.BASE_URL}{StudentRoutes.STUDENTS_BY_ID}'
            .format(student_id=student_id)
        )
        return response
    
    def get_student_by_id(self, student_id: int) -> requests.Response:
        response = requests.get(
            url=f'{self.config.BASE_URL}{StudentRoutes.STUDENTS_BY_ID}'
            .format(student_id=student_id)
        )
        return response

    def update_student_data(self, student_id: int, body: dict) -> requests.Response:
        response = requests.put(
            url=f'{self.config.BASE_URL}{StudentRoutes.STUDENTS_BY_ID}'
            .format(student_id=student_id), json=body,
        )
        return response