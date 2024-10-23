import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDModel(models.Model):
    """Provides a UUID primary key"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    """Singleton Model"""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        """
        When we call load method, an object will be
        loaded from a database or, if the object does
        not exist in a database, it will be created.
        When you save an instance of the model, it
        always has the same primary key, so there is
        only one record for this model in the database.
        Thus, in order to create a class responsible
        for site settings, we will create a class
        based on an abstract SingletonModel.
        """
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class CreatedByUserMixin(models.Model):

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        verbose_name=_("Created By"),
        help_text=_("User who created the record"),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):

    is_deleted = models.BooleanField(
        ("Is Deleted ?"), default=False, help_text=("Is Soft deleted ?")
    )

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        return self.save()


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created` and `modified` fields.
    """

    created = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified At"), auto_now=True)

    class Meta:
       abstract=True