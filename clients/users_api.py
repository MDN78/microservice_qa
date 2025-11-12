from requests import Response

from clients.base_session import BaseSession
from config import Server


class UsersApi:
    """
    Клиент с методами на каждую ручку микросервиса.
    Класс принимает переменную окружения и создает сессию с вшитым baseurl для выбранного окружения.
    """

    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).app)

    def get_user(self, user_id: int) -> Response:
        """
        Метод получения пользователя по id
        :param user_id: пользователя
        :return: Ответ от сервера в виде объекта Response
        """
        return self.session.get(f'/api/users/{user_id}')

    def get_users(self, params: dict = None) -> Response:
        """
        Метод получения всех пользователей
        :param params:
        :return: Ответ от сервера в виде объекта Response
        """
        return self.session.get('/api/users/', params=params)

    def create_user(self, json: dict) -> Response:
        """
        Метод создания пользователя
        :param json: словарь с данными пользователя
        :return: Ответ от сервера в виде объекта Response
        """
        return self.session.post('/api/users/', json=json)

    def update_user(self, user_id: int, json: dict) -> Response:
        """
        Метод обновления данных пользователя
        :param user_id: пользователь
        :param json: изменяемый параметр в виде словаря
        :return: Ответ от сервера в виде объекта Response
        """
        return self.session.patch(f'/api/users/{user_id}', json=json)

    def delete_user(self, user_id: int) -> Response:
        """
        Метод удаления пользователя
        :param user_id: идентификационный номер пользователя
        :return: Ответ от сервера в виде объекта Response
        """
        return self.session.delete(f'/api/users/{user_id}')

    def get_app_status(self) -> Response:
        """
        Метод получения статуса приложения
        :return: Ответ от сервера в виде объекта Response
        """
        return self.session.get('/status')

    def create_user_wrong_method(self, json: dict) -> Response:
        """
        Метод для негативных проверок создания пользователя некорректными методами
        :param json: данные пользователя
        :return: Ответ от сервера в виде объекта Response
        """
        return self.session.patch("/api/users/", json=json)
