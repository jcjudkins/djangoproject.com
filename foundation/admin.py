from django.contrib import admin
from django.utils.translation import gettext as _

from . import models


@admin.register(models.Office)
class OfficeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Term)
class TermAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "office", "term")
    list_filter = ("office", "term")
    list_select_related = True
    raw_id_fields = ("account",)

    @admin.display(ordering="account__last_name")
    def full_name(self, obj):
        return obj.account.get_full_name()


class CoreAwardAdmin(admin.ModelAdmin):
    list_display = ["recipient", "cohort"]


admin.site.register(models.CoreAward, CoreAwardAdmin)
admin.site.register(models.CoreAwardCohort)
