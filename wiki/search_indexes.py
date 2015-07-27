from haystack import indexes
from wiki.models import Page


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
