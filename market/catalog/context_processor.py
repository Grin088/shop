from catalog.models import Catalog


def get_categories(request) -> dict:
    """Контекстный процессор для каталога и поиска товара"""
    search = request.GET.get('query')
    catalogs = Catalog.objects.all()
    list_catalog = list()
    list_catalog_parent = list()
    for catalog in catalogs:
        if catalog.parent:
            list_catalog_parent.append(catalog.parent)
        else:
            list_catalog.append(catalog)
    if search:
        request.session.set_expiry(180)
        request.session['search'] = search
    return {'list_category': list_catalog,
            'list_category_parent': list_catalog_parent,
            'categories': catalogs}
