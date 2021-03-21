import telegram
from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext
import sys
import mistune

from tgmarkdown.config import Config

# https://markdown-it.github.io/
# https://core.telegram.org/api/entities
# https://mistune.readthedocs.io/en/latest/advanced.html#use-renderers
class MyRenderer(mistune.HTMLRenderer):
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

    def linebreak(self):
        return '\n'

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
        if ordered:
            return text
        return text

    def list_item(self, text, level):
        return self.linebreak() + ' '*level**2 + f'- {text}'

    def block_quote(self, text):
        return '> ' + text

    def image(self, src, alt="", title=None):
        return self.link(src, text=title or alt or src)


def parse_entities_to_html(message_text, entities, urled=False):
    if message_text is None:
        return None

    if not sys.maxunicode == 0xffff:
        message_text = message_text.encode('utf-16-le')

    processed_text = ''
    last_offset = 0

    for entity, text in sorted(entities.items(), key=(lambda item: item[0].offset)):
        if entity.type == 'text_link':
            insert = '<a href="{0}">{1}</url>'.format(entity.url, text)
        elif entity.type == 'mention':
            insert = '<a href="https://t.me/{0}">{1}</url>'.format(text.strip('@'), text)
        elif entity.type == 'url' and urled:
            insert = '<a href="{0}">{0}</url>'.format(text)
        elif entity.type == 'bold':
            insert = '<b>' + text + '</b>'
        elif entity.type == 'italic':
            insert = '<i>' + text + '</i>'
        elif entity.type == 'underline':
            insert = '<u>' + text + '</u>'
        elif entity.type == 'strikethrough':
            insert = '<s>' + text + '</s>'
        elif entity.type == 'code':
            insert = '<code>' + text + '</code>'
        elif entity.type == 'pre':
            insert = '<pre>' + text + '</pre>'
        else:
            insert = text
        if sys.maxunicode == 0xffff:
            processed_text += message_text[last_offset:entity.offset] + insert
        else:
            processed_text += message_text[last_offset * 2:entity.offset * 2].decode('utf-16-le') + insert

        last_offset = entity.offset + entity.length

    if sys.maxunicode == 0xffff:
        processed_text += message_text[last_offset:]
    else:
        processed_text += message_text[last_offset * 2:].decode('utf-16-le')
    return processed_text


def make_markdown(update: Update, context: CallbackContext) -> None:
    markdown = mistune.create_markdown(renderer=MyRenderer(), plugins=['strikethrough'])
    entities = update.message.parse_entities()
    text = parse_entities_to_html(update.message.text, entities)
    update.message.reply_text(markdown(text),
                              parse_mode=telegram.ParseMode.HTML,
                              disable_web_page_preview=True)


updater = Updater(Config.TG_API_TOKEN)

updater.dispatcher.add_handler(MessageHandler(filters=None, callback=make_markdown))

updater.start_polling()
updater.idle()
