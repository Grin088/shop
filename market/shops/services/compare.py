from config.settings import MAX_COMP_LIST_LEN
from shops.models import Offer


def compare_list_check(session, id_offer) -> None:
    """Добавление/удаление id товаров в список сравнения "comp_list" в сессии. """

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


def sort_category(comp_list: set) -> dict:
    """Сортировка списка сравнения по категориям товара"""

    category_offer_dict = {}
    offer_category = Offer.objects.filter(pk__in=comp_list).values("product__category_id__name", "id")

    for item in offer_category:
        if category_offer_dict.get(item["product__category_id__name"]):
            category_offer_dict[item["product__category_id__name"]].append(item["id"])
        else:
            category_offer_dict[item["product__category_id__name"]] = [item["id"]]

    return category_offer_dict


def compare_list_add(list_offer) -> None:
    # список всех категорий которые встречаются в сравниваемых переложений
    # list_offer = category_offer_dict[category]
    list_property = list(set(Offer.objects.filter(pk__in=list_offer).values_list("product__property__name", flat=True)))
    if None in list_property:
        list_property.remove(None)

    quveryset_offers = Offer.objects.filter(pk__in=list_offer).values("product__name", "price", "id",
                                                                      "product__preview", "product__category_id__name",)

    # Генерация словаря для сравнения
    list_compar = []
    for item_i in quveryset_offers:
        list_compar.append(
            {"name": item_i["product__name"], "price": item_i["price"], "preview": item_i["product__preview"],
             "id": item_i["id"],
             "category": item_i["product__category_id__name"],
             "property": {}})
        for property_i, value_i in Offer.objects.filter(pk=item_i["id"]).values_list("product__property__name",
                                                                                     "product__productproperty__value", ):
            if value_i is not None:
                list_compar[-1]["property"][property_i] = [value_i, False]

    # Добавление свойств если отсутствует в списке
    for property_i in list_property:
        for item_i in list_compar:
            if property_i not in item_i["property"]:
                item_i["property"][property_i] = ["-", False]

    # Сравнение списка свойств
    for property_i in list_property:
        save = list_compar[0]["property"][property_i]
        for item_i in list_compar:
            if save != item_i["property"][property_i]:
                break
        else:
            for item_i in list_compar:
                item_i["property"][property_i][1] = True

    for item_i in list_compar:
        item_i["property"] = sorted(item_i["property"].items())

    return list_compar