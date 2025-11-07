## Построение минимального микросервиса с FastApi. branch "Main"

Применяемые механики:

- загрузка файла `users.json` в память сервера
- валидация данных файла при запуске сервера `uvicorn`
- обработка исключений с помощью `HTTPException`
- обработка разных типов исключений с помощью `HTTPException`
- вынос чувствительных данных в файл `.env`
- параметризация тестов `@pytest.mark.parametrize()`
- тестирование доступности сервера через модель `AppStatus` - установка простого флага, что база существует
- Использование библиотеки `fastapi-pagination` для базовой пагинации в эндпоинтах
  [fastapi-pagination](https://github.com/uriyyo/fastapi-pagination)

### Тесты:

- Получение пользователя
- Получение списка пользователей
- Проверка отсутствия дубликатов
- Негативные проверки
- Тесты пагинации
- Smoke тесты

## Добавление базы данных PostgreSQL. branch "database"

Реализованы новые тесты `test_methods`:

- [x] Тест на post: создание
- [x] Тест на delete: удаление
- [x] Тест на patch: изменение
- [x] Тест на 405 ошибку - неподдерживаемый метод
- [x] Тест на 422 ошибку - отправить модель без поля на создание
- [x] Тест 404 на удаленного пользователя

## Запуск микросервиса в Docker. branch 'docker'

- добавлен `Dockerfile`
- вынесены имя пользователя, пароль и имя базы данных в `.env` через использование переменных {DATABASE_USER},
  {POSTGRES_PASSWORD}
- настроен запуск контейнера с подключением к базе данных
- сборка и запуск производится одной командой
- добавлен файл `.dockerignore`

## Github-actions. Branch 'g_actions'

- Настроил деплой микросервиса с Github Actions.
- Обновил тесты  
   [События для запуска workflow](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#pull_request)  
   [Git и GitHub flow](https://medium.com/@yanminthwin/understanding-github-flow-and-git-flow-957bc6e12220)

### Шаги 

- Создать директории `.github` -> `workflows`
- Создать файл `test.yml`
    - Add parameters [github actions](https://github.com/actions/checkout),
    - Add [setup-python](https://github.com/actions/setup-python)

```yaml
- uses: actions/setup-python@v6
  with:
    python-version: '3.13'
```

- Commit and push code to Github
- Create pull_requests -> Actions
- Добавили логи к нашему wirkflow: [pytest result actions](https://github.com/pmeier/pytest-results-action) для этого в
   файл `test.yml` добавим:

```yaml
   - run: pytest tests --junit-xml=test-results.xml
```

- Добавить пароль в репозиторий - repository secret and variables options. `settings->secret and variables->actions`

### Добавлен новый workflows - release.yml для пуша в ветку 'main'  
- Добавили новый файл
- Добавили джобы `release` `deploy`
- Добавили разрешения:

```yaml
  permissions:
      contents: write
```
- Добавили GitHub token
```yaml
  env:
      H_TOKEN: ${{ github.token }}
```


### Запуск тестов локально:

Запуск Docker локально командой

```commandline
docker compose up -d
```

Запуск тестов командой

```commandline
pytest
```

Остановка Docker локально командой

```commandline
docker compose down
```

Завершить процессы postgres для освобождения порта - команда терминала:

```commandline
sudo pkill -9 postgres
```