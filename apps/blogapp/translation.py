from modeltranslation.translator import translator, TranslationOptions

from apps.blogapp.models import Category


class CategoryTranslationOptions(TranslationOptions):
    """
    Перевод категории
    """
    fields = ('name',)


translator.register(Category, CategoryTranslationOptions)
