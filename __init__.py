def classFactory(iface):
    from .year_range_filter import YearRangeFilterPlugin
    return YearRangeFilterPlugin(iface) 