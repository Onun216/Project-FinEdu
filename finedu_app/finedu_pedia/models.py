from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_summernote.models import AbstractAttachment
from utils.images import resize_image
from utils.rands import slugify_new


class GlossaryItemAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900, True, 70)

        return super_save


class GlossaryPage(models.Model):
    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default="",
        null=False, blank=True, max_length=255
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisa estar marcado '
            'para a página ser exibida publicamente.'
        ),
    )
    content = models.TextField()

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('finedu_pedia:glossary-home')
        return reverse('finedu_pedia:glossary-page', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class GlossaryItemManager(models.Manager):
    def get_published(self):
        return self\
            .filter(is_published=True)\
            .order_by('-pk')
    

class GlossaryItem(models.Model):
    class Meta:
        verbose_name = 'GlossaryItem'
        verbose_name_plural = 'GlossaryItems'

    objects = GlossaryItemManager()

    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default="",
        null=False, blank=True, max_length=255
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para o post ser exibido publicamente.'
        ),
    )
    content = models.TextField()
    cover = models.ImageField(upload_to='glossary/%Y/%m/', blank=True, default='')
    cover_in_glossary_item_content = models.BooleanField(
        default=True,
        help_text='Se marcado, exibirá a capa dentro do post.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # user.post_set.all() -> query que vai buscar todos os posts do utilizador
    # Gera um erro porque a relação não é especificada, gerando um conflito.
    # Correcção: user.post_created_by.all()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='glossary_item_created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    # Correcção: user.post_updated_by.all()
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='glossary_item_updated_by'
    )
 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('finedu_pedia:glossary-home')
        return reverse('finedu_pedia:glossary-item', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900, True, 70)

        return super_save