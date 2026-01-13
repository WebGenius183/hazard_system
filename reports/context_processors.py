from django.contrib.auth.models import Group

def supervisor_flag(request):
    """
    Adds `is_supervisor` to all templates.
    """
    user = getattr(request, 'user', None)
    is_supervisor = False
    if user and user.is_authenticated:
        is_supervisor = user.groups.filter(name='Supervisor').exists()
    return {'is_supervisor': is_supervisor}
