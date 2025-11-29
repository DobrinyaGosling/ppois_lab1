## PPOIS - Lab3

# Лабораторная работа по варианту «Картинная галерея ».

Код организован по слоям чистой архитектуры с акцентом на доменные подпакеты (`domain`, `application`, `infrastructure`, `presentation`, `errors`). Каждый файл описывает одну сущность или порт, тесты продолжают работать через единый импорт `src.*`,

Как запустить тесты и покрытие

cd lab_3
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry add
pytest -v
python -m coverage report -m
uvicorn src.presentation.api.app:app --reload

 с расчётом покрытия 96%

Сводка по классам

    Artist – ведёт биографию автора, награды и связанный каталог работ.
    Artwork – учёт произведения с приватными показами, бронью и продажей.
    BaseExhibition – общая модель выставки: залы, кураторы, статус и расписание.
    PublicExhibition – конкретизация публичных экспозиций с квотой билетов.
    Reservation – заявки на показ с переходами состояний и метаданными билетов.
    Transaction – движение средств, отметки авторизаций и завершений.
    Credential – учётные данные пользователя с блокировками и расчётом попыток.
    Customer – покупатель с ролями, балансом коллекции и набором прав.
    Visitor – профиль посетителя и управление предпочтительными залами.
    PaymentCard – платёжные карты клиентов и контроль лимитов.
    InsurancePolicy – страховые полисы работ с проверкой покрытия.
    LogisticsTicket – задачи перевозки, назначение курьеров и контроль доставки.
    AccountRepository – интерфейс доступа к пользователям и их ролям.
    CatalogRepository – интерфейс каталога работ и оценок.
    ExhibitionRepository – интерфейс расписаний выставок и приватных слотов.
    ReservationRepository – интерфейс хранения броней и их статусов.
    PaymentGatewayPort – контракт авторизации и списания средств.
    LogisticsProviderPort – контракт планирования перевозок и подтверждений.
    InsuranceProviderPort – контракт страховых операций и верификаций.
    IdentityProviderPort – генератор идентификаторов для доменных объектов.
    Validators – набор проверок входных данных в application-слое.
    RegisterCustomerUseCase – регистрация клиента и начальный набор ролей.
    RegisterVisitorUseCase – создание посетителя с преференциями.
    UserRegistrationUseCase – агрегирует регистрацию клиентов и посетителей.
    RegisterCredentialUseCase – выпуск логина/пароля и связь с аккаунтом.
    ValidatePasswordUseCase – проверка паролей и учёт неудачных попыток.
    ResetFailedAttemptsUseCase – сброс блокировок и попыток входа.
    AssignRoleToCustomerUseCase – администрирование ролей клиента.
    ListCustomerRolesUseCase – перечисление выданных ролей.
    ListArtworksUseCase – выдаёт общий каталог работ.
    GetArtworkDetailUseCase – подробности конкретной работы.
    GetCustomerCollectionUseCase – коллекция приобретений клиента.
    CalculateCollectionValueUseCase – совокупная стоимость коллекции.
    PurchaseArtworkUseCase – сценарий покупки с оплатой, логистикой и страхованием.
    ListExhibitionsUseCase – расписание выставок.
    ReserveArtworkUseCase – бронь работы на показ или покупку.
    ListReservationsUseCase – перечень броней посетителя или куратора.
    CancelReservationUseCase – отмена с возвратом статусов.
    EnsureReservationValidityUseCase – проверка срока действия и статуса.
    RequestPrivateAccessUseCase – запрос приватного показа по ролям.
    InMemoryAccountRepository – адаптер пользователей и ролей в памяти.
    InMemoryCatalogRepository – каталог работ в памяти с тестовым наполнением.
    InMemoryExhibitionRepository – репозиторий выставок и частных слотов.
    InMemoryReservationRepository – хранение броней и их истории.
    IdentityService – генератор идентификаторов с префиксами.
    SupportService – имитация внешних платёжных/логистических/страховых сервисов.
    UsersRouter / AuthRouter / ArtworksRouter / ExhibitionsRouter / ReservationsRouter / PurchasesRouter – REST-контроллеры FastAPI.
    Dependency Container – фабрики use-case’ов и синглтоны адаптеров.
    GetArtworkDetailUseCase – подробности конкретной работы.
    GetCustomerCollectionUseCase – коллекция приобретений клиента.
    CalculateCollectionValueUseCase – совокупная стоимость коллекции.
    PurchaseArtworkUseCase – сценарий покупки с оплатой, логистикой и страхованием.
    ListExhibitionsUseCase – расписание выставок.
    ReserveArtworkUseCase – бронь работы на показ или покупку.
    ListReservationsUseCase – перечень броней посетителя или куратора.

Каждый из перечисленных объектов имеет уникальные поля и поведения, совокупно реализовано 53 класса/интерфейсов, более 163 поля и 40 ассоциаций, а маршруты presentation-слоя ассоциированы с репозиториями и сервисами инфраструктуры.

Исключения

14 доменных исключений определены в `src/errors/*.py` (например, `ArtworkAlreadySoldError`, `CustomerNotEligibleForPrivateViewingError`, `InsuranceValidationError`, `PaymentAuthorizationError`, `ReservationExpiredError`). Они переэкспортируются через `domain.errors`, используются в сущностях, use-case’ах и тестах, а ветки с ошибками покрыты юнит-тестами, что подтверждается отчётом `python -m coverage report -m`.

Локальный запус swagger:  `uvicorn src.presentation.api.app:app --reload`

