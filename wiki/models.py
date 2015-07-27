from django.db import models
from wiki.utils.slugify import slugify


class Page(models.Model):
    slug = models.SlugField(max_length=30, blank=False, unique=True, db_index=True)
    title = models.CharField(max_length=30, editable=False)
    content = models.TextField()
    private = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True, editable=False)

    def __unicode__(self):
        return '%s' % self.title

    def __str__(self):
        return '%s' % self.title

    def get_title(self):
        return '%s' % self.slug.replace('_', ' ')

    def get_url(self):
        return '%s' % self.slug

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.slug)
            self.title = slugify(self.slug).replace('_', ' ').title()

        super(Page, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        ordering = ['-created']


class Link(models.Model):
    title = models.CharField(max_length=50, blank=False)
    url = models.CharField(max_length=500, blank=False)
    login_required = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'


class LinkGroup(models.Model):
    title = models.CharField(max_length=50, blank=False)
    links = models.ManyToManyField(Link)
    login_required = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = 'Link Group'
        verbose_name_plural = 'Link Groups'
