from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Office(models.Model):
    """
    An office held by a DSF Board member.

    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Term(models.Model):
    """
    A term in which DSF Board members served.

    """

    year = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.year


class BoardMember(models.Model):
    """
    A DSF Board member.

    """

    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    office = models.ForeignKey(Office, related_name="holders", on_delete=models.CASCADE)
    term = models.ForeignKey(
        Term, related_name="board_members", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.account.get_full_name()} ({self.office} - {self.term.year})"


class CoreAwardCohort(models.Model):
    """
    A cohort of individuals -- such as "Q1 2021" -- receiving the Django Core
    Developer title.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Name for the group being inducted, e.g. 'Q1 2021'"),
    )
    description = models.TextField(blank=True)
    cohort_date = models.DateField(
        help_text=_("Date this cohort was approved by the DSF Board"),
    )

    def __str__(self):
        return self.name


class CoreAward(models.Model):
    """An individual person awarded the Django Core Developer title."""

    cohort = models.ForeignKey(
        CoreAwardCohort,
        related_name="recipients",
        on_delete=models.CASCADE,
    )
    recipient = models.CharField(
        help_text=_("Recipient's name"), max_length=1023, unique=True
    )
    link = models.URLField(
        blank=True,
        null=True,
        help_text=_("Optional link for this recipient"),
    )
    description = models.TextField(
        blank=True,
        help_text=_(
            "Optional one-paragraph description/bio of why this person "
            "received the award"
        ),
    )

    class Meta:
        ordering = ["recipient"]

    def __str__(self):
        return self.recipient
