from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Guarda temporariamente o último link enviado por usuário
user_links = {}

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Oi 👋\n\n"
        "Me envie o link de um produto (Shopee, Mercado Livre, etc)\n"
        "e eu crio um anúncio pra você 🤖🔥"
    )

# Recebe o link
async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text.strip()
    user_id = update.message.from_user.id

    user_links[user_id] = link

    keyboard = [
        [InlineKeyboardButton("🔥 Oferta Relâmpago", callback_data="relampago")],
        [InlineKeyboardButton("💥 Oferta Imperdível", callback_data="imperdivel")],
        [InlineKeyboardButton("✨ Anúncio Normal", callback_data="normal")]
    ]

    await update.message.reply_text(
        "Escolha o tipo de anúncio 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Clique nos botões
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

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

    await query.edit_message_text(text)

def main():
    app = ApplicationBuilder().token("SEU_TOKEN_AQUI").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_link))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("🤖 CopyBot BR rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
