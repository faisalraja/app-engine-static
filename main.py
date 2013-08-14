import logging
import os
import webapp2
from webapp2_extras import jinja2

# constants
IS_DEV = os.environ.get('SERVER_SOFTWARE').startswith('Dev')


class BaseHandler(webapp2.RequestHandler):
    """
        BaseHandler for all requests
    """
    is_generate = False

    def dispatch(self):
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            pass

    def link(self, page='/'):

        if not self.is_generate:
            page = '/dev%s' % page

        return page

    def jinja2_factory(self, app):
        j = jinja2.Jinja2(app)
        j.environment.globals.update({
            # Set global variables.
            'link': self.link,
        })
        return j

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=self.jinja2_factory, app=self.app)

    def render_template(self, filename, base_template="base.html", **kwargs):
        kwargs.update({
            'url': self.request.url,
            'path': self.request.path,
            'query_string': self.request.query_string,
            'is_dev': IS_DEV,
            'base_template': base_template,
        })

        self.response.write(self.jinja2.render_template(filename, **kwargs))


class DevHandler(BaseHandler):
    # Handles Shouts

    def get(self, page):
        # Abort when accessing from live site
        if not IS_DEV:
            self.abort(404)

        template = page

        if template.endswith('/'):
            template += 'index.html'
        elif not template.endswith('.html'):
            template += '.html'

        self.is_generate = self.request.headers.get('X-Generate') == '1'

        return self.render_template(template, **{'page': page})


app = webapp2.WSGIApplication(debug=IS_DEV, routes=[
    # Main Routes
    webapp2.Route(r'/dev<page:.*>', DevHandler, name='dev'),
])