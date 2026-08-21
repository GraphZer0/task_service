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

---

## Как опубликовать репозиторий на GitHub

Эти файлы были собраны локально (без доступа к GitHub из текущей среды), поэтому создание репозитория и первый push нужно сделать вручную:

1. Создайте новый **публичный** репозиторий на GitHub (без README/`.gitignore`/лицензии — они уже есть здесь), например `task-service`.
2. Распакуйте архив и выполните в папке проекта:

   ```bash
   cd task-service
   git init
   git add .
   git commit -m "Initial commit: task REST service with CI/CD"
   git branch -M main
   git remote add origin https://github.com/<ваш-логин>/task-service.git
   git push -u origin main
   ```

3. Откройте вкладку **Actions** в репозитории — все три workflow (`Maven CI`, `Checkstyle`, `SpotBugs`) запустятся автоматически на push в `main`.
4. Чтобы увидеть аннотации в PR, создайте отдельную ветку, внесите изменение и откройте Pull Request в `main` — `checkstyle.yml` и `spotbugs.yml` оставят комментарии-аннотации прямо на строках кода при наличии замечаний.
5. Если какой-то workflow окрасится в красный:
   - **Maven CI** — обычно ошибка компиляции или упавший тест, смотрите лог шага "Build and test with Maven".
   - **Checkstyle** — сборка отчёта не должна падать (severity выставлен как `warning`, `failOnViolation=false`), но если шаг всё же красный, проверьте лог `mvn checkstyle:checkstyle`.
   - **SpotBugs** — аналогично, отчёт генерируется без падения сборки (`failOnError=false`); если красный — смотрите, не упала ли компиляция на шаге "Compile sources".

Дополнительно можно включить **Require status checks to pass before merging** в Settings → Branches, указав все три workflow как обязательные.
