# task-service

Простой REST-сервис на Spring Boot со списком задач и настроенным CI:
сборка/тесты (Maven CI), проверка стиля кода (Checkstyle) и статический анализ (SpotBugs).

## Стек

- Java 17, Spring Boot 3.3.4
- Spring Web, Spring Boot Test
- Maven

## Эндпойнт

`GET /api/tasks` — возвращает список задач в формате JSON.

```bash
curl http://localhost:8080/api/tasks
```

## Локальный запуск

```bash
mvn spring-boot:run
```

## Тесты

```bash
mvn verify
```

## CI/CD

В `.github/workflows/` настроены три independent workflow, запускаются на каждый push и PR в `main`:

- **maven-ci.yml** — сборка и тесты (`mvn verify`).
- **checkstyle.yml** — проверка стиля кода (`mvn checkstyle:checkstyle`), результаты аннотируются прямо в PR.
- **spotbugs.yml** — статический анализ на потенциальные ошибки (`mvn spotbugs:spotbugs`), отчёт публикуется как аннотации в PR и как artifact.

Правила Checkstyle — в файле `checkstyle.xml` в корне репозитория (облегчённый набор правил: неиспользуемые импорты, скобки, пробелы, длина строки).
