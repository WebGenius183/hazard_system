from django.contrib.auth.decorators import user_passes_test

def supervisor_required(view_func):
    return user_passes_test(
        lambda u: u.groups.filter(name='Supervisor').exists()
    )(view_func)

def is_supervisor(user):
    return user.groups.filter(name='Supervisor').exists()
