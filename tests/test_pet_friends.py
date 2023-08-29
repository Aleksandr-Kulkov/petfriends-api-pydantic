from api.api import PetFriends
from settings import valid_email, valid_password
import os
import pytest
from serializers.orders import RequestPostPetWithoutPhoto, ResponsePostPetWithoutPhoto, RequestGetAllPets
from pydantic import ValidationError

pf = PetFriends()


@pytest.fixture(autouse=True)
def get_key(email=valid_email, password=valid_password):
    """Фикстура проверяет, что запрос API ключа возвращает статус 200 и в результате содержится слово key,
    и возвращает API ключ."""

    #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.get_api_key(email, password)
    assert status == 200, 'Запрос выполнен неуспешно'
    assert 'key' in result, 'В запросе не передан ключ авторизации'
    return result


def test_pydantic_add_new_pet_without_photo_without_age(get_key, name='Deyk', animal_type='dog'):
    """Валидируем обязательность параметра age в запросе на создание питомца без фото."""
    data = {"auth_key": get_key, "name": name, "animal_type": animal_type}
    try:
        RequestPostPetWithoutPhoto(**data)
    except ValidationError as e:
        print(e.json())


def test_pydantic_add_new_pet_without_photo_without_animal_type(get_key, name='Deyk', age=5):
    """Валидируем обязательность параметра animal_type в запросе на создание питомца без фото."""
    data = {"auth_key": get_key, "name": name, "age": age}
    try:
        RequestPostPetWithoutPhoto(**data)
    except ValidationError as e:
        print(e.json())


def test_pydantic_add_new_pet_without_photo_without_name(get_key, animal_type='dog', age=5):
    """Валидируем обязательность параметра name в запросе на создание питомца без фото."""
    data = {"auth_key": get_key, "animal_type": animal_type, "age": age}
    try:
        RequestPostPetWithoutPhoto(**data)
    except ValidationError as e:
        print(e.json())


def test_pydantic_add_new_pet_without_photo_without_auth_key(name='Deyk', animal_type='dog', age=5):
    """Валидируем обязательность параметра auth_key в запросе на создание питомца без фото."""
    data = {name: 'Deyk', "animal_type": animal_type, "age": age}
    try:
        RequestPostPetWithoutPhoto(**data)
    except ValidationError as e:
        print(e.json())


def test_pydantic_response_add_new_pet_without_photo_with_valid_data(get_key, name='Deyk', animal_type='dog', age=5):
    """Валидируем параметры ответа. Проверяем, что запрос на создание питомца без фото с валидными данными
    возвращает статус 200 и имя созданного питомца соответствует ожидаемому."""

    #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Валидируем параметры ответа.
    try:
        ResponsePostPetWithoutPhoto(**result)
    except ValidationError as e:
        print(e.json())
    else:
        # Сверяем полученный ответ с ожидаемым результатом.
        assert status == 200
        assert result['name'] == name


def test_pydantic_response_add_new_pet_without_photo_with_str_age(get_key, name='Deyk', animal_type='dog', age='five'):
    """Валидируем тип int параметра age в ответе на запрос на создание питомца без фото со строковым значением age."""

    #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    # Валидируем параметры ответа.
    try:
        ResponsePostPetWithoutPhoto(**result)
    except ValidationError as e:
        print(e.json())


def test_pydantic_get_all_pets_without_auth_key(filter=''):
    """Валидируем обязательность параметра auth_key в запросе на получение списка всех питомцев."""
    data = {"filter": filter}
    try:
        RequestGetAllPets(**data)
    except ValidationError as e:
        print(e.json())


def test_pydantic_get_all_pets_without_filter(get_key):
    """Валидируем необязательность параметра filter в запросе на получение списка всех питомцев.
    Проверяем, что запрос списка всех питомцев возвращает статус 200
    и в результате содержится не пустой массив питомцев."""
    data = {"auth_key": get_key}
    try:
        RequestGetAllPets(**data)
    except ValidationError as e:
        print(e.json())
    else:
        #  Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
        status, result = pf.get_list_of_pets(get_key)

        # Сверяем полученный ответ с ожидаемым результатом.
        assert status == 200
        assert len(result['pets']) > 0
