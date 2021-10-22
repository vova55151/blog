from modeltranslation.translator import translator, TranslationOptions

from apps.menu.models import Menu


class TranslationOptions(TranslationOptions):
    """
    Перевод меню
    """
    fields = ('name',)


translator.register(Menu, TranslationOptions)
