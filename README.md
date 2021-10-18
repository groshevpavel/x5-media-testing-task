# x5-testing

Необходимо разработать API сервис простой системы начисления и списания баллов выбранному пользователю. 

Для упрощения, аутентификацию и авторизацию разрабатывать не требуется.

### Основные требования:
Каждый пользователь имеет в системе свой уникальный идентификатор и баланс баллов.
- API позволяет получить баланс баллов конкретного пользователя.
- API позволяет начислить баллы конкретному пользователю.
- API позволяет списать баллы у конкретного пользователя.
- API позволяет перевести баллы от одного пользователя к другому.

Код сервиса должен быть размещен на Github/Gitlab/Bitbucket.

#### Совсем круто, если:
- Сервис можно поднять локально со всеми зависимостями через, например, docker-compose up.
- API документирован и представляет контракт для клиентов.


## Решение
### Реализация
Используется FastAPI

### Запуск
```bash
docker-compose up
```
### Описание API
http://localhost/docs

### Примеры
#### Добавление пользователя и назначение ему баланса баллов
```bash
curl --location --request POST 'localhost/v1/users/add' \
--header 'Content-Type: application/json' \
--data-raw '{
    "bonus_points": 1000,
    "firstname": "Pavel",
    "lastname": "Groshev"
}'
```
Ответ
```json
{
    "id": 1,
    "firstname": "Pavel",
    "lastname": "Groshev",
    "bonus_points": 1000
}
```
#### Получение данных пользователя
```bash
curl --location --request GET 'localhost/v1/users/1'
```
Ответ
```json
{
  "id": 1,
  "firstname": "Pavel",
  "lastname": "Groshev",
  "bonus_points": 1000
}
```

#### Установить пользователю бонусные баллы
```bash
curl --location --request PUT 'localhost/v1/users/1/bonuses/1500'
```
Ответ
```json
{
  "id": 1,
  "bonus_points": 1000
}
```

#### Получить количество бонусных баллов у пользователя по его userid
```bash
curl --location --request GET 'localhost/v1/users/1/bonuses'
```
Ответ
```json
{
  "id": 1,
  "bonus_points": 1000
}
```

#### Списать у пользователя баллы
```bash
curl --location --request DELETE 'localhost/v1/users/1/bonuses/300'
```
Ответ
```json
{
  "id": 1,
  "bonus_points": 900
}
```

#### Переместить баллы одного пользователя другому пользователю
```bash
curl --location --request POST 'localhost/v1/users/1/bonuses/transfer' \
--header 'Content-Type: application/json' \
--data-raw '{
    "recipient_id": 2,
    "bonuses_amount": 50
}'
```
Ответ
```json
{
  "donor_id": 1,
  "donor_balance": 850
}
```
