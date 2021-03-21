import sys
import traceback

from telegram import ParseMode
from telegram.utils.helpers import mention_html
from tgmarkdown.config import Config


def handle_error(update, context):
    if update.effective_message:
        text = f"Произошла ошибка:\n{str(context.error)}\nРазработчик вкурсе, разберемся."
        update.effective_message.reply_text(text, parse_mode=None)
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    payload = ""
    if update.effective_user:
        payload += f' with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}'
    if update.poll:
        payload += f' with the poll id {update.poll.id}.'
    text = f"Hey.\n The error <code>{context.error}</code> happened{payload}. The full traceback:\n\n<code>{trace}" \
           f"</code>"
    context.bot.send_message(Config.ADMIN_UID, text, parse_mode=ParseMode.HTML)
    raise