from django import template

register = template.Library()

# Status value -> semantic tag kind (styled as Carbon tags in theme/carbon.scss)
STATUS_KINDS = {
    "atliktas": "success",
    "apmoketa": "success",
    "patvirtintas": "success",
    "laisvas": "success",
    "vykdomas": "progress",
    "registruotas": "progress",
    "naujas": "neutral",
    "neapmoketa": "warning",
    "laukia_daliu": "warning",
    "uzimtas": "warning",
    "atsauktas": "danger",
    "atsaukta": "danger",
    "mazas": "danger",
}


@register.filter
def status_kind(value) -> str:
    return STATUS_KINDS.get(str(value), "neutral")
