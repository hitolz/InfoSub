import opentracing
from flask import g
from functools import wraps


def tracer_decorator(span_name, pay_load=None):
    def _decorator(func):
        @wraps(func)
        def create_span(*args, **kwargs):
            span = g.get("tracer_span")
            if not span:
                new_span = opentracing.tracer.start_span(func.__name__)
            else:
                new_span = opentracing.tracer.start_span(func.__name__, child_of=span)
            new_span.log_event(span_name, payload=pay_load)
            g.tracer_span = new_span
            result = func(*args, **kwargs)
            if span:
                g.tracer_span = span
            new_span.finish()
            return result
        return create_span
    return _decorator


def current_span():
    return g.get("tracer_span", None)

