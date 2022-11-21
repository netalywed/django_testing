import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course

# def test_example():
#     assert False, "Just test example"


@pytest.fixture()
def client():
    return APIClient()

@pytest.fixture()
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory

@pytest.fixture()
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


# Создание курса  1-й вариант +
# @pytest.mark.django_db
# def test_create_course(client):
#     course = course_factory(_quantity=1)
#     response = client.post(path='/courses/')
#     assert response.status_code == 200
#     data = response.json()
#     assert data[0][id] == course.id


# Проверка списка курсов +
@pytest.mark.django_db
def test_list_courses(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=10)
    #Act
    response = client.get(path='/courses/')
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)

# Создание курса 2-й вариант +
@pytest.mark.django_db
def test_add_course(client):
    count = Course.objects.count()
    response = client.post(path='/courses/', data={'id': 2, 'name': 'French'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

# обновление курса (работает, только если запускать отдельно) +-
@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=10)
    the_id = courses[0].id
    # response = client.get(path='/courses/') # необязательная проверка
    # assert response.status_code == 200
    # data = response.json()
    # assert data[0]["name"] == courses[0].name
    new_name = "French"
    response2 = client.patch(path=f'/courses/{the_id}/', data={'name': new_name})
    assert response2.status_code == 200

# удаление курса (возвращает ответ 204) (работает, только если запускать отдельно) +-
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    # response = client.get(path='/courses/') # необязательная проверка
    # assert response.status_code == 200
    # data = response.json()
    # assert data[0]["name"] == courses[0].name
    the_name = courses[0].name
    the_id = courses[0].id
    response2 = client.delete(path='/courses/1/', data={'id': the_id,'name': the_name})
    assert response2.status_code == 204

# Фильтрация +
@pytest.mark.django_db
def test_filter_by_course_id(client, course_factory):
    courses = course_factory(_quantity=10)
    courses_ids = [i.id for i in courses]
    for course_id in courses_ids:
        response = client.get(path=f'/courses/?id={course_id}')
        data = response.json()
        print('---------------------------------------------------')
        print(data)
        assert response.status_code == 200
        assert data[0]['id'] == course_id

# Фильтрация +
@pytest.mark.django_db
def test_filter_by_course_name(client, course_factory):
    courses = course_factory(_quantity=10)
    for course in courses:
        course_id = course.id
        course_name = course.name
        response = client.get(path=f'/courses/?id={course_id}')
        assert response.status_code == 200
        data = response.json()
        print('---------------------------------------------------')
        print(data)
        assert data[0]['name'] == course_name


    # нерабочий вариант
    # courses = course_factory(_quantity=10)
    # response = client.get(path='/courses/')
    # assert response.status_code == 200
    # data = response.json()
    # # проверка по фильтрации
    # for i, m in enumerate(data):
    #     assert m["id"] == courses[i].id
    #     assert m["name"] == courses[i].name

    #другой вариант
    # courses = course_factory(_quantity=10)
    # courses_ids = [i.id for i in courses]
    # for course_id in courses_ids:
    #     response = client.get(f'/courses/?id={course_id}')
    #     assert response.status_code == 200
    # data = response.json()
    # assert data[0]['id'] == course_id


