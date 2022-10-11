from .data_fetch import Requester
from .local_settings import EVENTS_API_URL, SUBEVENTS_API_URL
from .local_settings import PARTICIPANTS_API_URL, PARTICIPANT_API_URL, MATCHES_API_URL, MATCH_API_URL
from .local_settings import EVENT_API_URL

requester = Requester()

def test_get_events():
    req = requester.requesting(EVENTS_API_URL, pk="1")
    assert req[0]['pk'] == 1


def test_get_event():
    req = requester.requesting(EVENT_API_URL, pk="1")
    assert req == [{
        "pk": 1,
        "name": "Первенство Пензенской области по тхэквондо",
        "description": "Первенство Пензенской области по тхэквондо среди кадетов и юниоров",
        "date_finish": "2022-01-05",
        "date_begin": "2021-12-30",
        "country": "Россия",
        "city": "Пенза",
        "status": "Идет",
        "admin_id": 1,
        "system_id": 1,
        "sport_type_id": 1
        }
    ]


def test_get_subevents():
    req = requester.requesting(SUBEVENTS_API_URL, pk="1")
    assert req[0] == {"pk": 1, "name": "Кадеты. Весовая категория  -41кг",
                      "description": "Поединки среди кадетов весовой категории -41кг",
                      "event_id": 1}


def test_get_participants():
    req = requester.requesting(PARTICIPANTS_API_URL, pk="1")
    assert req[0] == {"pk": 1,
                      "name": "Ларин Дмитрий Константинович",
                      "country": "Россия",
                      "city": "Пенза",
                      "progress": "1/4",
                      "result": "1/4",
                      "subevent_id": 1}


def test_get_participant():
    req = requester.requesting(PARTICIPANT_API_URL, pk="1")
    assert req[0] == {"pk": 1,
                      "name": "Ларин Дмитрий Константинович",
                      "country": "Россия",
                      "city": "Пенза",
                      "progress": "1/4",
                      "result": "1/4",
                      "subevent_id": 1}


def test_get_matches():
    req = requester.requesting(MATCHES_API_URL, pk="1")
    assert req[0] == {"pk": 4,
                      "number": 1,
                      "date": "2022-01-03",
                      "first_participant": "Ларин Дмитрий Константинович",
                      "second_participant": "Смирнов Олег Григорьевич",
                      "score": "8:5"}


def test_get_match():
    req = requester.requesting(MATCH_API_URL, pk="4")
    assert req == {"pk": 4,
                   "number": 1,
                   "date": "2022-01-03",
                   "first_participant": "Ларин Дмитрий Константинович",
                   "second_participant": "Смирнов Олег Григорьевич",
                   "score": "8:5"}
