from django.conf import settings

"""
    adds react paths to templates
"""


def react_vars(request):
    return {
        'main_js': settings.REACT_JS_PATH,
        'main_css': settings.REACT_CSS_PATH
    }
