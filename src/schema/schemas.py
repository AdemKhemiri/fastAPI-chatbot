def indivisual_serial(chat_log)-> dict:
    return {
        "id": str(chat_log["_id"]),
        "user_id": chat_log["user_id"],
        "date": chat_log["date"],
        "logs": chat_log["logs"]
    }


def list_serial(chat_logs: list) -> list:
    return [indivisual_serial(log) for log in chat_logs ]
