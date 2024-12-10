import subprocess
from telegram.ext import CommandHandler
from telegram.ext._application import Application

from utils import get_bot_token


async def parking(update, context):
    args = context.args
    await update.message.reply_text("Buscando posicion en la lista del parking")
    parking_command = ["python", "main.py", "parking"]
    # parking_command.append(args[0]) if args else parking_command
    subprocess.run(parking_command)


async def ester(update, context):
    args = context.args
    ester_command = ["python", "main.py", "ester"]
    await update.message.reply_text("Extrayendo indice €STER")
    # ester_command.append(args[0]) if args else ester_command
    subprocess.run(ester_command)


async def start(update, context):
    await update.message.reply_text("Bot iniciado correctamente")


def main():
    token = get_bot_token()
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("parking", parking, has_args=False))
    application.add_handler(CommandHandler("ester", ester, has_args=False))
    print("Listening...")
    application.run_polling(1.0)


main()
