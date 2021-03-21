import mistune


# https://markdown-it.github.io/
# https://core.telegram.org/api/entities
# https://mistune.readthedocs.io/en/latest/advanced.html#use-renderers
class TGHtmlRenderer(mistune.HTMLRenderer):
    def linebreak(self):
        return '\n'

    def paragraph(self, text):
        return self.linebreak() + text + self.linebreak()

    def codespan(self, text):
        return f'<pre>{text}</pre>'

    def block_code(self, code, info=None):
        return self.codespan(code)

    def block_html(self, html):
        return self.block_code(html)

    def block_error(self, html):
        return self.block_code(html)

    def newline(self):
        return self.linebreak()

    def heading(self, text, level):
        return self.linebreak()+'#'*level + f' <b>{text}</b>' + self.linebreak()

    def inline_html(self, text):
        return text

    def thematic_break(self):
        return self.linebreak() + '-' * 10 + self.linebreak()

    def table(self, text):
        return text

    def table_head(self, text):
        return text

    def list(self, text, ordered, level, start=None):
        return text

    def list_item(self, text, level):
        return ' '*level**2 + f'- {text}' + self.linebreak()

    def block_quote(self, text):
        return '> ' + text

    def image(self, src, alt="", title=None):
        return self.link(src, text=title or alt or src)
