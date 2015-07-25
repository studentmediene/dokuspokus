from django.db import models
from slugify import slugify


class Page(models.Model):
    slug = models.SlugField(max_length=30, blank=False, unique=True, db_index=True)
    content = models.TextField()
    private = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True, editable=False)

    def __unicode__(self):
        return '%s' % self.slug

    def __str__(self):
        return '%s' % self.slug.replace('_', ' ')

    def get_url(self):
        return '%s' % self.slug

    def is_published(self):
        return self.publish

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.slug)

        super(Page, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        ordering = ['-created']