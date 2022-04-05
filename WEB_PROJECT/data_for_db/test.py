from requests import get, post, delete

# print(get('http://localhost:8080/api/jobs').json())
# print(get('http://localhost:8080/api/jobs/3').json())
# print(get('http://localhost:8080/api/jobs/25').json())
# print(post('http://localhost:8080/api/jobs/stroka').json())
#
# print(post('http://localhost:8080/api/news',
#            json={'title': 'Заголовок'}).json())
# #
# print(post('http://localhost:8080/api/jobs',
#            json={'team_leader': 1,
#                  'id': 5,
#                  'job': 'Some work',
#                  'work_size': 12,
#                  'collaborators': '1, 2, 3, 4'}).json())
# #
# print(delete('http://localhost:8080/api/news/999').json())
# новости с id = 999 нет в базе
#
# print(delete('http://localhost:8080/api/news/12').json())


# # correct request
# print(post('http://localhost:8080/api/jobs',
#            json={'team_leader': 1,
#                  'id': 9,
#                  'job': 'Some work',
#                  'work_size': 12,
#                  'collaborators': '1, 2, 3, 4'}).json())
#
# # такой id уже есть
# print(post('http://localhost:8080/api/jobs',
#            json={'team_leader': 1,
#                  'id': 5,
#                  'job': 'Some work',
#                  'work_size': 12,
#                  'collaborators': '1, 2, 3, 4'}).json())
#
# # отсутствует поле team_leader
# print(post('http://localhost:8080/api/jobs',
#            json={'id': 12,
#                  'job': 'Some work',
#                  'work_size': 12,
#                  'collaborators': '1, 2, 3, 4'}).json())
#
# # пропущено поле job
# print(post('http://localhost:8080/api/jobs',
#            json={'team_leader': 1,
#                  'id': 13,
#                  'work_size': 12,
#                  'collaborators': '1, 4, 5'}).json())
#
# # get-запрос на все работы
# print(get('http://localhost:8080/api/jobs').json())


# # корректный запрос
# print(delete('http://localhost:8080/api/jobs/8').json())
# # некорректные запросы
# print(delete('http://localhost:8080/api/jobs/25').json())
# print(delete('http://localhost:8080/api/jobs/qqq').json())
# print(delete('http://localhost:8080/api/jobs/100').json())
# # get-запрос на все работы
# print(get('http://localhost:8080/api/jobs').json())

#
# print(post('http://localhost:8080/api/register',
#            json={'name': 'test_m2.4',
#                  'email': 'm2.4_test@test',
#                  'hashed_password': 'lalala',
#                  }).json())
#
# print(post('http://localhost:8080/registration', json={'username': 'emi2288',
#                                                        'email': 'emi_test2@test',
#                                                        'password': '1234567890'}).json())
#
# print(post('http://localhost:8080/api/login', json={'username': 'miks',
#                                                        'email': 'test@test',
#                                                        'password': 'qwerty'}).json())

# print(delete('http://localhost:8080/api/users').json())
#
print(get('http://localhost:8080/api/users').json())
print(post('http://localhost:8080/api/login', json={'username': 'emi',
                                                       'email': 'test2@test',
                                                       'password': '1230'}).json())