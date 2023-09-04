from werkzeug.wrappers import Response
from jinja2 import Environment, FileSystemLoader


class TextPlainResponse(Response):
    mine_type = 'text/plain'

    def __init__(self, text):
        super().__init__(response=text, status=200, mimetype=self.mine_type)


class TextHTMLResponse(Response):
    mine_type = 'text/html'

    def __init__(self, context=None, template_path='', template_name=''):
        self.jinja = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=True
        )
        template = self.jinja.get_template(template_name)
        rendered_text = template.render(context=context)
        super().__init__(response=rendered_text, mimetype=self.mine_type)
