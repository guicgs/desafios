import json
import os
from subprocess import Popen

from decouple import config
from scrapy.utils.log import configure_logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext


TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")


def load_scraping_results() -> list:
    results_json_path = "./results/items.json"
    if (
            os.path.isfile(results_json_path)
            and os.path.getsize(results_json_path) > 0
        ):
            with open("./results/items.json") as file:
                return json.load(file)
    return []


def format_reddit_top_threads_text(results: list) -> str:
    message_text = "TOP REDDITS\n"
    for result in results:
        subreddit = result["subreddit_title"]
        message_text += "\n".join([
            "====================",
            f"<b>{subreddit.capitalize()}</b>\n",
        ])
        items = result["items"]
        if not items:
            message_text += "Não foi encontrado nenhum reddit com +5k de pontuação :(\n"
        else:
            for item in items:
                message_text += "\n".join([
                    "- Título",
                    f"<pre>{item['title']}</pre>",
                    "- Pontuação",
                    f"<pre>{item['score']}</pre>",
                    "- Link da fonte",
                    f"{item['source_url']}",
                    "- Link para os comentários",
                    f"{item['comments_url']}\n\n",
                ])
    return message_text


def send_reddit_top_threads(update: Update, context: CallbackContext) -> None:
    try:
        subreddits = context.args[0]
    except IndexError:
        update.message.reply_text(
            text="""Escreva pelo menos o nome de um subreddit. Exemplos:
            
            /NadaPraFazer cats
            /NadaPraFazer sports;worldnews
            """
        )
        raise IndexError

    scraper = Popen(["python3", "scraper_runner.py", f"--subreddits={subreddits}"])
    scraper.wait(timeout=10)

    results = load_scraping_results()

    message_text = format_reddit_top_threads_text(results)
    update.message.reply_text(text=message_text, parse_mode=ParseMode.HTML)


def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('NadaPraFazer', send_reddit_top_threads))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    configure_logging()
    main()
