from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from gpt4all import GPT4All

TOKEN = "8017567800:AAHVTeWII6WNjOcSOOTZ5ncZ01AHF3YQq10"
MODEL_PATH = "ggml-gpt4all-j.bin"

print("Загрузка модели...")
model = GPT4All(MODEL_PATH)
print("Модель загружена. Антон готов!")

chat_history = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Антон 🤖\n"
        "Просто напиши мне сообщение, и мы можем общаться как с другом."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text.strip()

    if user_id not in chat_history:
        chat_history[user_id] = []

    chat_history[user_id].append(f"Пользователь: {user_text}")
    prompt = "\n".join(chat_history[user_id]) + "\nАнтон:"

    try:
        response = model.generate(prompt, max_tokens=200)
    except:
        response = "Прости, что-то пошло не так."

    await update.message.reply_text(response)
    chat_history[user_id].append(f"Антон: {response}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Антон бот запущен ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
