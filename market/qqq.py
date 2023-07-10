from __future__ import print_function
from jinja2 import Environment, FileSystemLoader
import locale
import gettext

domain = 'traslate'

current_locale = 'en_US'
print('Current locale: {}'.format(current_locale))

locale_path = 'locale/'
gnu_translations = gettext.translation(
    domain='translate',
    localedir=locale_path,
    languages=[current_locale],
    fallback=True
)
gnu_translations.install()

print(_('dddsfsdf'))
env = Environment(
    extensions=['jinja2.ext.i18n'],
    loader=FileSystemLoader('templates')
)
env.install_gettext_translations(gnu_translations, newstyle=True)

template = env.get_template('market/catalog/catalog.jinja2')
result = template.render()
print(result)
