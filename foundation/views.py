from datetime import datetime

from django.http import Http404
from django.shortcuts import redirect
from django.views import generic

from . import models, redirects


class MeetingMixin:
    date_field = "date"
    model = models.Meeting


class MeetingArchiveIndex(MeetingMixin, generic.ArchiveIndexView):
    pass


class MeetingArchiveYear(MeetingMixin, generic.YearArchiveView):
    make_object_list = True


class MeetingArchiveMonth(MeetingMixin, generic.MonthArchiveView):
    pass


class MeetingArchiveDay(MeetingMixin, generic.DayArchiveView):
    pass


class MeetingDetail(MeetingMixin, generic.DateDetailView):
    context_object_name = "meeting"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("leader")
            .prefetch_related(
                "grants_approved",
                "individual_members_approved",
                "corporate_members_approved",
                "business",
                "action_items",
                "board_attendees",
                "non_board_attendees",
            )
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        meeting = context_data["object"]
        context_data["ongoing_business"] = meeting.business.filter(
            business_type=models.Business.ONGOING
        )
        context_data["new_business"] = meeting.business.filter(
            business_type=models.Business.NEW
        )
        return context_data


class CoreDevelopers(generic.ListView):
    queryset = models.CoreAwardCohort.objects.prefetch_related("recipients").order_by(
        "-cohort_date"
    )


def minutes_redirect(request, year, month, day, slug):
    minutes_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%b-%d").date()
    year, month, day = minutes_date.timetuple()[:3]
    if (year, month, day) not in redirects.MINUTES_DATES:
        raise Http404
    return redirect(
        f"{redirects.MINUTES_BASE_URL}{year}/{year}-{month:02}-{day:02}.md",
        permanent=True,
    )
