__author__ = 'igor'
from materials.models import Item
from haystack import indexes


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    main_group_slug = indexes.CharField(model_attr='main_group__slug')
    main_group_title = indexes.CharField(model_attr='main_group__title')
    year_release = indexes.DateField(model_attr='year_release')
    genres = indexes.MultiValueField()
    title = indexes.CharField(model_attr='title')
    original_image = indexes.CharField(model_attr='original_image')
    content_auto = indexes.EdgeNgramField(model_attr='title')
    slug = indexes.CharField(model_attr='slug')

    def get_model(self):
        return Item

    def prepare_genres(self, obj):
        return [genre.title for genre in obj.genres.all()]
