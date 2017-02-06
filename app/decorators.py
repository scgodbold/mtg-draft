from flask import flash, redirect, url_for
from flask import request, render_template
from functools import wraps


def announce(ExceptionType, destination='home'):
    '''Decorate a view function with this to catch exceptions
    and turn them into flashed messages for the end user

    uses url_for to determine view to redirect to, defaults to home

    Usage:
        @announce(TypeError)
        @announce(ValueError, destination='logout')
    '''
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ExceptionType as e:
                print('caught it! {}'.format(e.message))
                flash(e.message)
                return redirect(url_for(destination))
        return decorator_function
    return decorator

def templated(template=None):
    '''Decorates a View function and will take a returned dictionary
    and render a template with the values in it. If no template name is
    provided it will try to intelligently determine which template you wanted

    Usage:
        @templated()
        @templated(template='template.html')
    '''
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorator_function
    return decorator
