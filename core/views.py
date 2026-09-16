import calendar
from datetime import date, timezone as dt_timezone
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.timezone import localtime
from django.http import HttpResponse
from django.urls import reverse
from .models import Session, Speaker, Subgroup



def home(request):
    next_session = (
        Session.objects
        .filter(start_time__gt=timezone.now())
        .prefetch_related("speakers")
        .order_by("start_time")
        .first()
    )

    return render(
        request,
        "core/home.html",
        {
            "next_session": next_session,
        },
    )

def calendar_feed(request):
    sessions = (
        Session.objects
        .filter(start_time__gt=timezone.now())
        .prefetch_related("speakers", "subgroups")
        .order_by("start_time")
    )

    def escape_ical(value):
        if not value:
            return ""

        return (
            str(value)
            .replace("\\", "\\\\")
            .replace(";", "\\;")
            .replace(",", "\\,")
            .replace("\r\n", "\\n")
            .replace("\n", "\\n")
            .replace("\r", "\\n")
        )

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Neurosciensemble//Study Circle//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Neurosciensemble — Study Circle",
        "X-WR-TIMEZONE:Europe/Paris",
    ]

    for session in sessions:
        start_utc = session.start_time.astimezone(dt_timezone.utc)
        end_utc = session.end_time.astimezone(dt_timezone.utc)

        speakers = ", ".join(
            speaker.name
            for speaker in session.speakers.all()
        )

        description_parts = []

        if session.description:
            description_parts.append(session.description)

        if speakers:
            description_parts.append(
                f"Speakers: {speakers}"
            )

        description_parts.append(
            f"Session type: {session.get_session_type_display()}"
        )

        if session.meeting_link:
            description_parts.append(
                f"Google Meet: {session.meeting_link}"
            )

        session_url = request.build_absolute_uri(
            reverse("session_detail", args=[session.pk])
        )

        description_parts.append(
            f"Session page: {session_url}"
        )

        description = "\n\n".join(description_parts)

        lines.extend([
            "BEGIN:VEVENT",
            f"UID:session-{session.pk}@neurosciensemble.org",
            f"DTSTAMP:{timezone.now().astimezone(dt_timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{start_utc.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTEND:{end_utc.strftime('%Y%m%dT%H%M%SZ')}",
            f"SUMMARY:{escape_ical(session.title)}",
            f"DESCRIPTION:{escape_ical(description)}",
            f"LOCATION:{escape_ical(session.room)}",
            f"URL:{session_url}",
            "END:VEVENT",
        ])

    lines.append("END:VCALENDAR")

    response = HttpResponse(
        "\r\n".join(lines) + "\r\n",
        content_type="text/calendar; charset=utf-8",
    )

    response["Content-Disposition"] = (
        'inline; filename="neurosciensemble.ics"'
    )

    return response



def programme(request):
    today = localtime().date()

    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))

        if month < 1 or month > 12:
            raise ValueError

    except (TypeError, ValueError):
        year = today.year
        month = today.month

    if month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = month - 1
        previous_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # ---------------------------------------------------------
    # CALENDAR
    # ---------------------------------------------------------

    cal = calendar.Calendar(firstweekday=0)
    month_weeks = cal.monthdatescalendar(year, month)

    all_sessions = (
    Session.objects
    .prefetch_related("speakers", "subgroups")
    .order_by("start_time")
)   

    sessions_by_date = {}

    for session in all_sessions:

        local_date = localtime(session.start_time).date()

        sessions_by_date.setdefault(
            local_date,
            []
        ).append(session)


    calendar_weeks = []

    for week in month_weeks:

        calendar_week = []

        for day in week:

            calendar_week.append({
                "date": day,
                "is_current_month": day.month == month,
                "is_today": day == today,
                "sessions": sessions_by_date.get(day, []),
            })

        calendar_weeks.append(calendar_week)


    # ---------------------------------------------------------
    # UPCOMING SESSIONS
    # ---------------------------------------------------------

    upcoming_sessions = (
        all_sessions
        .filter(start_time__date__gte=today)
        .order_by("start_time")[:5]
    )


    # ---------------------------------------------------------
    # PREVIOUS SESSIONS
    # ---------------------------------------------------------

    previous_sessions = (
        all_sessions
        .filter(start_time__date__lt=today)
        .order_by("-start_time")[:5]
    )


    return render(
        request,
        "core/programme.html",
        {
            "calendar_weeks": calendar_weeks,

            "upcoming_sessions": upcoming_sessions,
            "previous_sessions": previous_sessions,

            "month_name": date(
                year,
                month,
                1
            ).strftime("%B"),

            "year": year,

            "previous_month": previous_month,
            "previous_year": previous_year,

            "next_month": next_month,
            "next_year": next_year,
        },
    )


def session_detail(request, pk):
    session = get_object_or_404(Session, pk=pk)

    return render(
        request,
        "core/session_detail.html",
        {"session": session},
    )


def members(request):
    members = Speaker.objects.all()

    return render(
        request,
        "core/members.html",
        {
            "members": members,
        },
    )


def member_detail(request, slug):
    member = get_object_or_404(
        Speaker,
        slug=slug,
    )

    sessions = member.sessions.all()

    return render(
        request,
        "core/member_detail.html",
        {
            "member": member,
            "sessions": sessions,
        },
    )
def subgroups(request):
    subgroups = Subgroup.objects.select_related(
        "head"
    ).prefetch_related(
        "members"
    )

    return render(
        request,
        "core/subgroups.html",
        {
            "subgroups": subgroups,
        },
    )


def subgroup_detail(request, slug):
    subgroup = get_object_or_404(
        Subgroup.objects.select_related("head").prefetch_related("members"),
        slug=slug,
    )

    sessions = subgroup.sessions.prefetch_related("speakers", "subgroups")

    return render(
        request,
        "core/subgroup_detail.html",
        {
            "subgroup": subgroup,
            "sessions": sessions,
        },
    )

def contact(request):
    return render(request, "core/contact.html")