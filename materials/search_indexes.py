__author__ = 'igor'
from materials.models import Item
from haystack import indexes


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    main_group_slug = indexes.CharField(model_attr='main_group__slug')
    main_group_title = indexes.CharField(model_attr='main_group__title')
    year_release = indexes.DateField(model_attr='year_release')
    countries = indexes.MultiValueField()
    genres = indexes.MultiValueField()
    title = indexes.CharField(model_attr='title')
    main_image = indexes.CharField(model_attr='main_image__url')
    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Item

    def prepare_countries(self, obj):
       return [country.name for country in obj.countries.all()]

    def prepare_genres(self, obj):
        return [genre.title for genre in obj.genres.all()]