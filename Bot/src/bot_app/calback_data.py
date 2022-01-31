from aiogram.utils.callback_data import CallbackData

sport_callback = CallbackData("sport", "pk")
event_callback = CallbackData("event", "pk", "sport_id")
subevent_callback = CallbackData("subevent", "pk", "sport_id", "ev_id")
participants_callback = CallbackData("participants", "pk", "sport_id", "ev_id")
participant_callback = CallbackData("participant", "pk", "sport_id", "ev_id", "sid")
event_stats_callback = CallbackData("stats", "pk", "sport_id")
event_subevents_callback = CallbackData("subevents", "pk", "sport_id")
matches_callback = CallbackData("matches", "pk", "sport_id", "ev_id")
match_callback = CallbackData("match", "pk", "sport_id", "ev_id", "sid")
sport_menu_callback = CallbackData("sport_menu", "sport_id")
sport_analyze_callback = CallbackData("sport_analyze", "sport_id")

