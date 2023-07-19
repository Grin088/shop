from typing import Dict, Union

from django.conf import settings
from shops.models import Offer

ListCompare = list[Dict[str, Union[str, float, Dict[str, list[str, bool]], int,]]]


def compare_list_check(session, id_offer) -> None:
    """Добавление/удаление id товаров в список сравнения "comp_list" в сессии. """

    value = session.get("comp_list", [])
    if value:
        if id_offer in value:
            value.remove(id_offer)
            session["comp_list"] = value

        else:
            if len(value) < settings.MAX_COMP_LIST_LEN:
                value.append(id_offer)
                session["comp_list"] = value

    else:
        value.append(id_offer)
        session["comp_list"] = value


def splitting_into_groups_by_category(comp_list: list[int]) -> (dict[str, list[int]], list[(str, int)]):
    """Разбивание списка сравнения по категориям товара"""

    category_offer_dict = {}
    offer_category = Offer.objects.filter(pk__in=comp_list).values("product__category_id__name", "id")

    for item in offer_category:
        if category_offer_dict.get(item["product__category_id__name"]):
            category_offer_dict[item["product__category_id__name"]].append(item["id"])
        else:
            category_offer_dict[item["product__category_id__name"]] = [item["id"]]

    category_count_product = sorted([(name, len(count)) for name, count in category_offer_dict.items()],
                                  key=lambda x: x[1], reverse=True)

    return category_offer_dict, category_count_product


def _get_a_complete_list_of_property_names(list_offer: list[int]) -> list[str]:
    """Получение списка всех встречающихся названий свойств продуктов в списке сравнения"""

    list_name_property = list(set(Offer.objects.filter(pk__in=list_offer)
                                  .values_list("product__property__name", flat=True)))

    if None in list_name_property:
        list_name_property.remove(None)

    return sorted(list_name_property)


def _generating_a_comparison_dictionary(list_offer: list[int]) -> ListCompare:
    """Генерация словаря для сравнения свойств прод"""

    list_compar = []
    quveryset_offers = Offer.objects.filter(pk__in=list_offer).values("product__name",
                                                                      "price",
                                                                      "id",
                                                                      "product__preview",
                                                                      "product__category_id__name",
                                                                      ).order_by("id")

    for item_i in quveryset_offers:
        list_compar.append({"name": item_i["product__name"],
                            "price": item_i["price"],
                            "preview": item_i["product__preview"],
                            "id": item_i["id"],
                            "category": item_i["product__category_id__name"],
                            "property": {}},
                           )
        for property_i, value_i in Offer.objects.filter(pk=item_i["id"])\
                .values_list("product__property__name",
                             "product__productproperty__value",
                             ):
            if value_i is not None:
                list_compar[-1]["property"][property_i] = [value_i, False]

    return list_compar


def _adding_missing_properties(list_property: list[str],
                               list_compare: ListCompare) -> ListCompare:
    """"Добавление отсутствующих свойств к продуктам в список сравнения"""

    for property_i in list_property:
        for item_i in list_compare:
            if property_i not in item_i["property"]:
                item_i["property"][property_i] = ["-", False]

    return list_compare


def _comparison_of_product_properties(list_compare: ListCompare, list_property: list[str]) -> ListCompare:
    """Сравнение свойств продуктов в списке сравнения"""

    for property_i in list_property:
        save = list_compare[0]["property"][property_i]
        for item_i in list_compare:
            if save != item_i["property"][property_i]:
                break
        else:
            for item_i in list_compare:
                item_i["property"][property_i][1] = True

    return list_compare


def comparison_lists_and_properties(list_offer: list[int]) -> (ListCompare, list[str]):
    """Генерация списка сравнения и списка свойств продуктов"""

    list_compare = _generating_a_comparison_dictionary(list_offer)
    list_property = _get_a_complete_list_of_property_names(list_offer)
    list_compare = _adding_missing_properties(list_property, list_compare)
    list_compare = _comparison_of_product_properties(list_compare, list_property)

    return list_compare, list_property


# def get_comparepage(session):
