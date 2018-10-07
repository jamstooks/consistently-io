from django.conf import settings

"""
    adds react paths to templates
"""


def react_vars(request):
    return {
        'main_js': settings.REACT_JS_PATH,
        'main_css': settings.REACT_CSS_PATH
    }


def github_avatar(request):

    if request.user.is_authenticated:
        base_url = "https://avatars0.githubusercontent.com/u/%s?s=40&v=4"
        github = request.user.social_auth.get(provider='github')
        return {
            'avatar': base_url % github.uid
        }
    return {'avatar': None}
