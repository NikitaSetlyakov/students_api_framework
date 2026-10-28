import logging

import allure
import requests

from config import TestConfig


logger = logging.getLogger(__name__)


class StudentRoutes:
    STUDENTS = '/student'
    STUDENTS_BY_ID = '/student/{student_id}'


class StudentClient:
    def __init__(self, config: TestConfig):
        self.config = config

    @allure.step('Отправка запроса на получение списка всех студентов')
    def get_students_list(self) -> requests.Response:
        logger.info('Получаем список студентов')

        response = requests.get(
            url=f'{self.config.BASE_URL}{StudentRoutes.STUDENTS}',
        )

        logger.info(f'Ответ: {response.status_code}, {response.text}')

        return response

    @allure.step('Отправка запроса на создание нового студента')
    def create_new_student(self, body: dict) -> requests.Response:
        logger.info(f'Создаём студента: {body}')

        response = requests.post(
            url=f'{self.config.BASE_URL}{StudentRoutes.STUDENTS}',
            json=body,
        )

        logger.info(f'Ответ: {response.status_code}, {response.text}')

        return response

    @allure.step('Отправка запроса на удаление студента')
    def delete_student(self, student_id: int) -> requests.Response:
        logger.info(f'Удаляем студента с ID {student_id}')

        response = requests.delete(
            url=f'{self.config.BASE_URL}{StudentRoutes.STUDENTS_BY_ID}'
            .format(student_id=student_id),
        )

        logger.info(f'Ответ: {response.status_code}, {response.text}')

        return response

    @allure.step('Отправка запроса на получение студента по ID')
    def get_student_by_id(self, student_id: int) -> requests.Response:
        logger.info(f'Получаем студента с ID {student_id}')

        response = requests.get(
            url=f'{self.config.BASE_URL}{StudentRoutes.STUDENTS_BY_ID}'
            .format(student_id=student_id),
        )

        logger.info(f'Ответ: {response.status_code}, {response.text}')

        return response

    @allure.step('Отправка запроса на изменение данных о студенте')
    def update_student_data(
        self,
        student_id: int,
        body: dict,
    ) -> requests.Response:
        logger.info(f'Обновляем студента с ID {student_id}: {body}')

        response = requests.put(
            url=f'{self.config.BASE_URL}{StudentRoutes.STUDENTS_BY_ID}'
            .format(student_id=student_id),
            json=body,
        )

        logger.info(f'Ответ: {response.status_code}, {response.text}')

        return response