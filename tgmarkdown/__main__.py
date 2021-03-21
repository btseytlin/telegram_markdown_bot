import telegram
from telegram.ext import Updater, MessageHandler, Filters
import mistune
import sys
import logging

from tgmarkdown.config import Config
from tgmarkdown.error_handler import handle_error
from tgmarkdown.renderer import TGHtmlRenderer




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


def make_markdown(update, context):
    markdown = mistune.create_markdown(renderer=TGHtmlRenderer(escape=False), plugins=['strikethrough'])
    entities = update.message.parse_entities()
    text = parse_entities_to_html(update.message.text, entities)
    update.message.reply_text(markdown(text),
                              parse_mode=telegram.ParseMode.HTML,
                              disable_web_page_preview=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    updater = Updater(Config.TG_API_TOKEN)

    updater.dispatcher.add_handler(MessageHandler(Filters.text, callback=make_markdown))
    updater.dispatcher.add_error_handler(handle_error)

    if Config.HEROKU_NAME and Config.PORT:
        logging.info('Starting webhook on port %s', Config.PORT)
        updater.start_webhook(listen="0.0.0.0",
                              port=Config.PORT,
                              url_path='bot')
        updater.bot.setWebhook(f'https://{Config.HEROKU_NAME}.herokuapp.com/bot')
    else:
        updater.start_polling()
        updater.idle()
