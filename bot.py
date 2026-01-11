from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext
)

# Guarda o último link enviado por cada usuário
user_links = {}

# /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Oi 👋🤖\n\n"
        "Me envie o link de um produto (Shopee, Mercado Livre, etc)\n"
        "e eu crio um anúncio prontinho pra você 🔥"
    )

# Recebe o link
def receive_link(update: Update, context: CallbackContext):
    link = update.message.text.strip()
    user_id = update.message.from_user.id

    user_links[user_id] = link

    keyboard = [
        [InlineKeyboardButton("🔥 Oferta Relâmpago", callback_data="relampago")],
        [InlineKeyboardButton("💥 Oferta Imperdível", callback_data="imperdivel")],
        [InlineKeyboardButton("✨ Anúncio Normal", callback_data="normal")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Escolha o tipo de anúncio 👇",
        reply_markup=reply_markup
    )

# Trata clique nos botões
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    link = user_links.get(user_id, "link não encontrado")

    if query.data == "relampago":
        text = (
            "🔥 Oferta Relâmpago\n\n"
            "💰 R$ 00,00*\n"
            f"👉 Confira no link abaixo:\n{link}\n\n"
            "*Valor sujeito a alteração sem aviso prévio.*"
        )

    elif query.data == "imperdivel":
        text = (
            "💥 Oferta Imperdível\n\n"
            "💰 R$ 00,00*\n"
            f"👉 Veja os detalhes no link:\n{link}\n\n"
            "*Valor sujeito a alteração sem aviso prévio.*"
        )

    else:
        text = (
            "✨ Produto em destaque\n\n"
            "💰 R$ 00,00*\n"
            f"👉 Acesse aqui:\n{link}\n\n"
            "*Valor sujeito a alteração sem aviso prévio.*"
        )

    query.edit_message_text(text)

def main():
    import os
    updater = Updater(os.getenv("BOT_TOKEN"), use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_link))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
