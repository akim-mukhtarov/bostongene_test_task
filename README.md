# Тестовое задание для Bostongene

Сервис вычисления MD5 хэшей для файлов


## Описание

1. Backend - необходимо реализовать минимальное REST API (FastAPI) в связке с очередью (Celery, можно использовать стандартную связку Celery+Redis+RabbitMQ), минимальной базой данных (Postgres + sqlalchemy для взаимодействия) и файлом логов с программно-реализованной последовательной записью. В API должны быть реализованы эндпоинты для загрузки файла и для доступа к результатам в базе.
Порядок действий API:
    *  API принимает на вход файл
    *  Файл отправляется в очередь (реализовать механизм Promise: создаем id хранения в API, возвращаем его после того, как положили файл в очередь (вместе с id))
    *  Worker забирает данные из очереди, вычисляет MD5 хеш, записывает результат в базу с id, созданным как Promise, в конце исполнения результат должен быть записан в файл логов.
    *  Файл логов - обычный файл в папке, которая монтируется к контейнерам worker-ов. Необходимо реализовать механизм последовательного взаимодействия worker-ов с файлом (например при помощи семафора).

2. Frontend - минимальное веб приложение, в котором можно загрузить файл и в ответ получить id. Также должно присутствовать поле, в котором можно получить результат по id.


## Детали реализации

### База данных
Задачу вычисления MD5 хэша описывает следующая схема:
```
                                    Table "public.md5_tasks"
 Column  |       Type        | Collation | Nullable |                  Default
---------+-------------------+-----------+----------+--------------------------------------------
 task_id | integer           |           | not null | nextval('md5_tasks_task_id_seq'::regclass)
 status  | taskstatus        |           | not null |
 result  | character varying |           |          |
Indexes:
    "md5_tasks_pkey" PRIMARY KEY, btree (task_id)
```
Поля `status` и `result` дублируют поля таблицы, создаваемой `celery` при использовании `SQLAlchemy` в качестве `result_backend`. 
В теории, возможно забирать результаты напрямую из `celery`, не создавая собственных таблиц. 
Однако, `celery` возвращает статус `PENDING` для задач, отсутствующих в очереди. Чтобы определить, действительно ли задача 
присутствует в очереди, используется таблица выше: запись в базе создается перед отправкой задачи в очередь. 
В эту таблицу `worker` затем записывает статус и результаты вычисления. 

### Синхронизация доступа к файлу логов
Использовал механизм `file locking` (функция `lockf` пакета `fcntl` с флагами `LOCK_EX` + `LOCK_NB`). В случае, если другой процесс захватил блокировку, бросается исключение, попытку записи повторяю позже через некоторый интервал времени (`task.retry`).

### Контейнеризация
Приложение поднимается с помощью docker-compose.
Компоненты `worker` и `api` используют один Dockerfile, но разные команды запуска (в docker-compose для `worker` прописан `entrypoint`, который перезаписывает `cmd`). Так объем репозитория получился меньше, однако `worker` тянет за собой зависимости `api`.
 
