
import re
from html import escape

import markdown
import nh3
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = {
    "p", "br", "hr",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "strong", "em", "del", "blockquote",
    "ul", "ol", "li",
    "pre", "code",
    "table", "thead", "tbody", "tr", "th", "td",
    "a", "img",
}

ALLOWED_ATTRIBUTES = {
    "a": {"href", "title"},
    "img": {"src", "alt", "title"},
    "th": {"align"},
    "td": {"align"},
}

ALLOWED_URL_SCHEMES = {"http", "https", "mailto"}

# Protect LaTeX expressions while Markdown is being processed.
MATH_PATTERN = re.compile(
    r"(\$\$.*?\$\$|\$[^$\n]+?\$|\\\[.*?\\\]|\\\(.*?\\\))",
    re.DOTALL,
)


@register.filter
def render_markdown(value):
    if not value:
        return ""

    protected_math = []

    def protect(match):
        protected_math.append(match.group(0))
        return f"MATHPLACEHOLDER{len(protected_math) - 1}END"

    source = MATH_PATTERN.sub(protect, value)

    html = markdown.markdown(
        source,
        extensions=["extra", "sane_lists", "toc"],
    )

    clean_html = nh3.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes=ALLOWED_URL_SCHEMES,
        clean_content_tags={"script", "style", "iframe", "object"},
    )

    # Restore math as escaped text so it cannot inject HTML.
    for index, expression in enumerate(protected_math):
        clean_html = clean_html.replace(
            f"MATHPLACEHOLDER{index}END",
            escape(expression),
        )

    return mark_safe(clean_html)
