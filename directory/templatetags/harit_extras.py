from urllib.parse import quote

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ICONS = {
    "solar": '<rect x="12" y="20" width="76" height="44" rx="3"/><path d="M12 35h76M12 50h76M31 20v44M50 20v44M69 20v44M50 64v16M35 80h30"/>',
    "heater": '<rect x="30" y="14" width="40" height="52" rx="6"/><path d="M40 26h20M40 36h20M40 46h20M25 80c4-6 12-6 16 0s12 6 16 0 12-6 16 0"/>',
    "wind": '<path d="M50 46 L50 84 M38 84h24"/><circle cx="50" cy="40" r="5"/><path d="M50 35 Q56 18 48 10 M55 43 Q72 46 78 38 M45 43 Q30 52 30 62"/>',
    "rain": '<path d="M50 14 Q72 42 72 58 a22 22 0 1 1 -44 0 Q28 42 50 14Z"/><path d="M42 60 a8 8 0 0 0 8 8"/>',
    "ev": '<rect x="20" y="34" width="44" height="34" rx="5"/><path d="M64 44h10l8 8v16h-18M28 68v8M56 68v8M40 42l-6 12h10l-6 12"/>',
    "battery": '<rect x="22" y="30" width="56" height="40" rx="5"/><path d="M80 42v16M32 50h12M60 44v12M54 50h12"/>',
    "biogas": '<circle cx="50" cy="54" r="26"/><path d="M50 28v-8M40 22h20M42 50a8 8 0 0 1 16 0c0 6-8 6-8 12"/><circle cx="50" cy="68" r="1.5"/>',
    "compost": '<path d="M28 40h44l-5 40H33Z"/><path d="M36 30c4-8 24-8 28 0M50 52v16M42 58l8-6 8 6"/>',
    "roof": '<path d="M18 52 L50 22 L82 52 M28 46v32h44V46"/><path d="M40 78V60h20v18"/>',
    "grey": '<path d="M26 26h48v20a24 24 0 0 1 -48 0Z"/><path d="M36 60 q4 8 0 14 M50 62 q4 8 0 14 M64 60 q4 8 0 14"/>',
}


@register.simple_tag
def cat_icon(key):
    paths = ICONS.get(key, ICONS["solar"])
    return mark_safe(f'<span class="ic"><svg viewBox="0 0 100 100">{paths}</svg></span>')


@register.simple_tag
def wa_link(number, message=""):
    base = f"https://wa.me/{number}"
    if message:
        base += "?text=" + quote(message)
    return mark_safe(base)


@register.filter
def clean_phone(value):
    return "".join(ch for ch in str(value) if ch.isdigit() or ch == "+")
