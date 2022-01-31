from aiogram import types
from .local_settings import SPORTS_API_URL, EVENTS_API_URL, SUBEVENTS_API_URL, COUNT_SUBEVENTS_API_URL
from .local_settings import PARTICIPANTS_API_URL, PARTICIPANT_API_URL, MATCHES_API_URL, MATCH_API_URL
from .local_settings import EVENT_API_URL, COUNT_PARTICIPANTS_API_URL, SPORT_DATA_API_URL
from .calback_data import sport_callback, event_callback, subevent_callback, participant_callback, event_stats_callback
from .calback_data import event_subevents_callback, participants_callback, matches_callback, match_callback,\
    sport_menu_callback, sport_analyze_callback
from .keyboards import inline_kb
from .app import dp, bot
from .messages import WELCOME, HELP
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from .data_fetch import Requester


class IRequester:
    def request(self, url, pk=0):
        return "Default"


class AdapterRequester(IRequester):

    def __init__(self, req: Requester):
        self.req = req

    def request(self, url, pk=""):
        return self.req.requesting(url, pk)


req = Requester()
requester = AdapterRequester(req)


def request(req: IRequester, url, pk=""):
    return req.request(url, pk)


sports = request(requester, SPORTS_API_URL)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(WELCOME, reply_markup=inline_kb)


@dp.message_handler(commands='select_sport')
async def get_list_sport_types(message: types.Message):
    kb = InlineKeyboardMarkup()
    for sport in sports:
        button = InlineKeyboardButton(f"{sport['name']}", callback_data=sport_menu_callback.new(sport_id=sport["pk"]))

        kb.add(button)
    await message.reply("Выберите вид спорта", reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == 'select_sport')
async def button_list_sports(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    kb = InlineKeyboardMarkup()
    for sport in sports:
        button = InlineKeyboardButton(f"{sport['name']}", callback_data=sport_menu_callback.new(sport_id=sport["pk"]))
        kb.add(button)
    await bot.send_message(callback_query.from_user.id, "Выберите вид спорта", reply_markup=kb)


@dp.callback_query_handler(sport_menu_callback.filter())
async def sport_menu(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    kb = InlineKeyboardMarkup()
    sport_id = callback_data.get("sport_id")
    back_btn = InlineKeyboardButton("Вернуться назад", callback_data="select_sport")
    analyze_btn = InlineKeyboardButton("Анализ развития вида спорта",
                                       callback_data=sport_analyze_callback.new(sport_id=sport_id))
    events_btn = InlineKeyboardButton("Посмотреть события",
                                      callback_data=sport_callback.new(pk=sport_id))
    kb.add(analyze_btn)
    kb.add(events_btn)
    kb.add(back_btn)
    await bot.send_message(callback_query.from_user.id, "Выберите пункт меню", reply_markup=kb)


@dp.callback_query_handler(sport_analyze_callback.filter())
async def sport_analyze(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    kb = InlineKeyboardMarkup()
    sport_id = callback_data.get("sport_id")
    back_btn = InlineKeyboardButton("Вернуться назад",
                                    callback_data=sport_menu_callback.new(sport_id=sport_id))
    kb.add(back_btn)
    sport_data = request(requester, SPORT_DATA_API_URL, pk=sport_id)
    if sport_data == 0:
        await bot.send_message(callback_query.from_user.id, "Нет Данных", reply_markup=kb)
    else:
        result = f"Вид спорта: {sport_data['name']}\n" \
                 f"Общее количество событий: {sport_data['count_events']}\n" \
                 f"Количество событий в текущем году: {sport_data['count_events_cur_year']}\n" \
                 f"Количество событий в прошлом году: {sport_data['count_events_last_year']}\n" \
                 f"Среднее количество участников в одном событии в текущем году: " \
                 f"{sport_data['avg_participants_cur_year']}\n" \
                 f"Среднее количество участников в одном событии в прошлом году: " \
                 f"{sport_data['avg_participants_last_year']}"
        await bot.send_message(callback_query.from_user.id, result, reply_markup=kb)


@dp.callback_query_handler(sport_callback.filter())
async def button_sport(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    kb = InlineKeyboardMarkup()
    sport_id = callback_data.get("pk")
    events = request(requester, EVENTS_API_URL, pk=sport_id)
    back_btn = InlineKeyboardButton("Вернуться назад",
                                    callback_data=sport_menu_callback.new(sport_id=sport_id))
    kb.add(back_btn)
    if events == 0:
        await bot.send_message(callback_query.from_user.id, "Нет событий", reply_markup=kb)

    else:
        for event in events:
            button = InlineKeyboardButton(f"{event['name']}",
                                          callback_data=event_callback.new(pk=event["pk"],
                                                                           sport_id=sport_id))
            kb.add(button)
        await bot.send_message(callback_query.from_user.id, "Выберите событие", reply_markup=kb)


@dp.callback_query_handler(event_callback.filter())
async def show_event_menu(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    ev_id = callback_data.get("pk")
    sport_id = callback_data.get("sport_id")
    kb = InlineKeyboardMarkup()
    stats_btn = InlineKeyboardButton("Посмотреть статистику события",
                                     callback_data=event_stats_callback.new(pk=ev_id,
                                                                            sport_id=sport_id))
    list_subevents_btn = InlineKeyboardButton("Выбрать подкатегорию",
                                              callback_data=event_subevents_callback.new(pk=ev_id, sport_id=sport_id))
    back_btn = InlineKeyboardButton("Вернуться назад", callback_data=sport_callback.new(
        pk=sport_id))
    kb.add(stats_btn)
    kb.add(list_subevents_btn)
    kb.add(back_btn)
    await bot.send_message(callback_query.from_user.id, "Выберите пункт меню", reply_markup=kb)


@dp.callback_query_handler(event_stats_callback.filter())
async def show_event_stats(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    event_id = callback_data.get("pk")
    sport_id = callback_data.get("sport_id")
    event = request(requester, EVENT_API_URL, pk=event_id)
    result = f"Название: {event[0]['name']}\nОписание: {event[0]['description']}\nСтатус: {event[0]['status']}\n" \
             f"Дата начала: {event[0]['date_begin']}\nДата завершения: {event[0]['date_finish']}\n" \
             f"Количество участников: {requester.request(COUNT_PARTICIPANTS_API_URL, pk=event_id)['message']}"
    kb = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("Вернуться назад", callback_data=event_callback.new(pk=event_id,
                                                                                        sport_id=sport_id))
    kb.add(back_btn)
    await bot.send_message(callback_query.from_user.id, result, reply_markup=kb)


@dp.callback_query_handler(event_subevents_callback.filter())
async def show_subevent(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    kb = InlineKeyboardMarkup()
    ev_id = callback_data.get("pk")
    sport_id = callback_data.get("sport_id")
    subevents = requester.request(SUBEVENTS_API_URL, pk=ev_id)
    count = requester.request(COUNT_SUBEVENTS_API_URL, pk=ev_id)["message"]
    back_btn = InlineKeyboardButton("Вернуться назад",
                                    callback_data=event_callback.new(pk=ev_id,
                                                                     sport_id=sport_id))
    kb.add(back_btn)
    if subevents == 0:
        await bot.send_message(callback_query.from_user.id, "Нет подкатегорий", reply_markup=kb)
    else:
        for subevent in subevents:
            button = InlineKeyboardButton(f"{subevent['name']}",
                                          callback_data=subevent_callback.new(pk=subevent["pk"],
                                                                              ev_id=ev_id,
                                                                              sport_id=sport_id))
            kb.add(button)
        await bot.send_message(callback_query.from_user.id, f"Количество подкатегорий: {count}\n"
                                                            f"Выберите подкатегорию", reply_markup=kb)


@dp.callback_query_handler(subevent_callback.filter())
async def button_subevent(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    kb = InlineKeyboardMarkup()
    subevent_id = callback_data.get("pk")
    ev_id = callback_data.get("ev_id")
    sport_id = callback_data.get("sport_id")
    back_btn = InlineKeyboardButton("Вернуться назад",
                                    callback_data=event_subevents_callback.new(pk=ev_id,
                                                                               sport_id=sport_id))

    results_btn = InlineKeyboardButton("Посмотреть результаты матчей",
                                       callback_data=matches_callback.new(pk=subevent_id,
                                                                          sport_id=sport_id,
                                                                          ev_id=ev_id))
    participant_btn = InlineKeyboardButton("Посмотреть список участников",
                                           callback_data=participants_callback.new(pk=subevent_id,
                                                                                   sport_id=sport_id,
                                                                                   ev_id=ev_id))
    kb.add(results_btn)
    kb.add(participant_btn)
    kb.add(back_btn)
    await bot.send_message(callback_query.from_user.id, "Выберите пункт меню", reply_markup=kb)


@dp.callback_query_handler(participant_callback.filter())
async def show_data_of_participant(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    participant = requester.request(PARTICIPANT_API_URL, pk=callback_data.get("pk"))
    subevent_id = callback_data.get("sid")
    ev_id = callback_data.get("ev_id")
    sport_id = callback_data.get("sport_id")
    kb = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("Вернуться назад",
                                    callback_data=participants_callback.new(pk=subevent_id,
                                                                            ev_id=ev_id,
                                                                            sport_id=sport_id))
    kb.add(back_btn)
    result_str = f"Имя: {participant[0]['name']}\nСтрана: {participant[0]['country']}\n" \
                 f"Город: {participant[0]['city']}\n" \
                 f"Прогресс: {participant[0]['progress']}"
    await bot.send_message(callback_query.from_user.id, result_str, reply_markup=kb)


@dp.callback_query_handler(participants_callback.filter())
async def show_participants(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    participants = requester.request(PARTICIPANTS_API_URL, pk=callback_data.get("pk"))
    subevent_id = callback_data.get("pk")
    ev_id = callback_data.get("ev_id")
    sport_id = callback_data.get("sport_id")
    kb = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("Вернуться назад",
                                    callback_data=subevent_callback.new(pk=subevent_id,
                                                                        ev_id=ev_id,
                                                                        sport_id=sport_id))
    kb.add(back_btn)
    if participants == 0:
        await bot.send_message(callback_query.from_user.id,
                               "Нет участников",
                               reply_markup=kb)
    else:
        for participant in participants:
            button = InlineKeyboardButton(f"{participant['name']}",
                                          callback_data=participant_callback.new(pk=participant["pk"],
                                                                                 sid=subevent_id,
                                                                                 ev_id=ev_id,
                                                                                 sport_id=sport_id))
            kb.add(button)
        await bot.send_message(callback_query.from_user.id, "Нажмите на имя участника, чтобы посмотерть информацию о нем",
                               reply_markup=kb)


@dp.callback_query_handler(matches_callback.filter())
async def show_matches(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    subevent_id = callback_data.get("pk")
    ev_id = callback_data.get("ev_id")
    sport_id = callback_data.get("sport_id")
    matches = requester.request(MATCHES_API_URL, pk=subevent_id)
    kb = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("Вернуться назад",
                                    callback_data=subevent_callback.new(pk=subevent_id,
                                                                        ev_id=ev_id,
                                                                        sport_id=sport_id))
    kb.add(back_btn)
    if matches == 0:
        await bot.send_message(callback_query.from_user.id, "Нет матчей",
                               reply_markup=kb)
    else:
        for match in matches:
            button = InlineKeyboardButton(f"№{match['number']}: {match['first_participant']} vs "
                                          f"{match['second_participant']}",
                                          callback_data=match_callback.new(pk=match["pk"],
                                                                           sid=subevent_id,
                                                                           ev_id=ev_id,
                                                                           sport_id=sport_id))
            kb.add(button)
        await bot.send_message(callback_query.from_user.id, "Нажмите на матч, чтобы посмотерть информацию о нем",
                               reply_markup=kb)


@dp.callback_query_handler(match_callback.filter())
async def show_match(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query.id)
    match = requester.request(MATCH_API_URL, pk=callback_data.get("pk"))
    subevent_id = callback_data.get("sid")
    ev_id = callback_data.get("ev_id")
    sport_id = callback_data.get("sport_id")
    kb = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton("Вернуться назад",
                                    callback_data=matches_callback.new(pk=subevent_id,
                                                                       ev_id=ev_id,
                                                                       sport_id=sport_id))
    kb.add(back_btn)
    result = f"№ матча: {match['number']}\n" \
             f"{match['first_participant']} {match['score']} {match['second_participant']}\n" \
             f"Дата: {match['date']}"
    await bot.send_message(callback_query.from_user.id, result, reply_markup=kb)


@dp.message_handler(commands='help')
async def helping(message: types.Message):
    await message.reply(HELP, reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data == 'help')
async def button_help(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, HELP, reply_markup=inline_kb)
