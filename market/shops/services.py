from config.settings import MAX_COMP_LIST_LEN


def compare_list_check(session, id_offer) -> None:
    """Добавление/удаление id товаров в список сравнения "comp_list" в сессии."""

    value = session.get("comp_list", [])

    if value:
        if id_offer in value:
            value.remove(id_offer)
            session["comp_list"] = value

        else:
            if len(value) < MAX_COMP_LIST_LEN:
                value.append(id_offer)
                session["comp_list"] = value

    else:
        value.append(id_offer)
        session["comp_list"] = value
