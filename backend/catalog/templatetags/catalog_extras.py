from django import template
from urllib.parse import urlencode

register = template.Library()

@register.filter
def dict_get(d: dict, key):
    if not d:
        return 0
    return d.get(key, 0)

def _build_query(mode: str, query: str, tag_ids: list[int]) -> str:
    params = []
    if mode:
        params.append(("mode", mode))
    if query:
        params.append(("q", query))
    for tid in tag_ids:
        params.append(("tag", str(tid)))
    qs = urlencode(params)
    return f"?{qs}" if qs else "?"

@register.simple_tag
def add_tag_url(selected_tag_ids, tag_id, mode="or", q=""):
    # selected_tag_ids can be set/list of ints
    ids = list(selected_tag_ids) if selected_tag_ids else []
    tid = int(tag_id)
    if tid not in ids:
        ids.append(tid)
    return _build_query(mode, q, ids)

@register.simple_tag
def remove_tag_url(selected_tag_ids, tag_id, mode="or", q=""):
    ids = list(selected_tag_ids) if selected_tag_ids else []
    tid = int(tag_id)
    ids = [x for x in ids if int(x) != tid]
    return _build_query(mode, q, ids)

@register.simple_tag
def clear_filters_url(q=""):
    # If you want to also clear q, call without q.
    # By default we keep q if passed.
    return _build_query(mode="", query=q, tag_ids=[])
