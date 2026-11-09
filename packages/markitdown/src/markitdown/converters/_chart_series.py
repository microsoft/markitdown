"""Read a chart's series straight from its XML, across every plot group.

python-pptx exposes charts one plot group at a time, and ``chart.series`` only
walks the series of the first group. A chart that mixes types (bars with a
line on top, a second value axis, ...) keeps one <c:ser> per group. Reading the
part's XML gives us every series of every group, each with its own category
and value caches.
"""

from typing import Dict, List, Optional, Tuple

from pptx.oxml.ns import qn

# Children of <c:plotArea> that open a plot group and hold their own <c:ser>s.
PLOT_GROUP_TAGS = (
    "c:area3DChart",
    "c:areaChart",
    "c:bar3DChart",
    "c:barChart",
    "c:bubbleChart",
    "c:doughnutChart",
    "c:line3DChart",
    "c:lineChart",
    "c:ofPieChart",
    "c:pie3DChart",
    "c:pieChart",
    "c:radarChart",
    "c:scatterChart",
    "c:stockChart",
    "c:surface3DChart",
    "c:surfaceChart",
)

# (name, category label by point index, value by point index)
SeriesData = Tuple[str, Optional[Dict[int, str]], Optional[Dict[int, str]]]


def _int_val(element, name: str, default: int) -> int:
    child = element.find(qn(name))
    if child is None:
        return default
    try:
        return int(child.get("val"))
    except (TypeError, ValueError):
        return default


def _points(cache) -> Dict[int, str]:
    """{point index: text} for a <c:strCache>, <c:numCache> or literal."""
    points = {}
    if cache is None:
        return points
    for point in cache.findall(qn("c:pt")):
        value = point.find(qn("c:v"))
        if value is not None and value.text is not None:
            points[int(point.get("idx"))] = value.text
    return points


def _resolve(container) -> Optional[Dict[int, str]]:
    """Resolve a <c:cat>/<c:val>-style wrapper to {index: text}.

    The values normally live in a cache behind a reference (c:strRef /
    c:numRef). PowerPoint writes them inline (c:strLit / c:numLit) when it
    doesn't want to keep the range, so both shapes have to be read.
    """
    if container is None:
        return None
    for ref_tag, cache_tag in (("c:strRef", "c:strCache"), ("c:numRef", "c:numCache")):
        ref = container.find(qn(ref_tag))
        if ref is not None:
            points = _points(ref.find(qn(cache_tag)))
            if points:
                return points
    for lit_tag in ("c:strLit", "c:numLit"):
        points = _points(container.find(qn(lit_tag)))
        if points:
            return points
    return None


def _categories(series) -> Optional[Dict[int, str]]:
    for tag in ("c:cat", "c:xVal"):
        container = series.find(qn(tag))
        if container is None:
            continue

        # Multi-level categories: each <c:lvl> is one level of labels, ordered
        # outermost first, so the innermost one carries the per-point label.
        for multi_tag, cache_tag in (
            ("c:multiLvlStrRef", "c:multiLvlStrCache"),
            ("c:multiLvlStrLit", None),
        ):
            for multi in container.findall(qn(multi_tag)):
                if cache_tag is None:
                    levels = multi.findall(qn("c:lvl"))
                else:
                    cache = multi.find(qn(cache_tag))
                    levels = cache.findall(qn("c:lvl")) if cache is not None else []
                for level in reversed(levels):
                    points = _points(level)
                    if points:
                        return points

        points = _resolve(container)
        if points:
            return points
    return None


def _values(series) -> Optional[Dict[int, str]]:
    for tag in ("c:val", "c:yVal"):
        points = _resolve(series.find(qn(tag)))
        if points:
            return points
    return None


def _name(series, fallback_index: int) -> str:
    # <c:tx> wraps the name in a strRef/strLit, and the <c:v> we want sits
    # inside its cache, so search the subtree rather than the direct children.
    for value in series.find(qn("c:tx")).iter(qn("c:v")):
        if value.text:
            return value.text
    return f"Series {fallback_index + 1}"


def read_series(chart) -> List[SeriesData]:
    """Every series of every plot group in the chart.

    The order follows <c:order>, which numbers the series across the whole
    chart rather than per group, so the table keeps the series in the order
    the chart shows them.
    """
    chart_element = chart._chartSpace.find(qn("c:chart"))
    if chart_element is None:
        return []
    plot_area = chart_element.find(qn("c:plotArea"))
    if plot_area is None:
        return []

    groups = {qn(tag) for tag in PLOT_GROUP_TAGS}
    series_elements = []
    for group in plot_area:
        if group.tag in groups:
            series_elements.extend(group.findall(qn("c:ser")))

    # <c:order> decides where a series sits in the chart and is unique across
    # groups, unlike <c:idx> which repeats in every group.
    series_elements.sort(key=lambda ser: _int_val(ser, "c:order", 0))

    return [
        (_name(series, index), _categories(series), _values(series))
        for index, series in enumerate(series_elements)
    ]
