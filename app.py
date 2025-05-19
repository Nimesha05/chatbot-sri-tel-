import os 
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.environ["hf_tokan"] = os.getenv("hf_tokan")
os.environ["LANGCAHIN_API_KEY"] = os.getenv("LANGCAHIN_API_KEY")
os.environ["LANGCAHIN_PROJECT"] = os.getenv("LANGCAHIN_PROJECT")
os.environ["LANGCAHIN_TRACING_V2"] = "true"
groq_api_key = os.getenv("groq_api_key")

def setup_llm_chain(topic="technology"):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful and friendly assistant for Randiya Production, "
         "an agriculture-based company located in Sri Lanka. The company is led by CEO Nimesha Wijesinghe. "
         "You must directly answer user messages in a friendly, concise, and professional tone, without explaining your thinking process."),
            ("user", "topic: {topic}")
        ]
    )
    llm = ChatGroq(
        model= "gemma2-9b-it",
        api_key=groq_api_key
    )
    OUTPUT_PARSER = StrOutputParser()
    chain = prompt | llm | OUTPUT_PARSER
    return chain
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your friendly assistant. How can I help you today?")

    topic = "technology"
    joke = setup_llm_chain(topic).invoke({"topic": topic}).strip()
    await update.message.reply_text(joke)

async def handle_masseg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    bot_username = context.bot.username

    if '@' in msg:
        # Remove the bot's username from the message
        msg = re.sub('', '', msg).strip()
        if msg:
            await update.message.reply_text("Generating response...")
            topic = msg
            chain = setup_llm_chain(topic)
            result = chain.invoke({"topic": topic})
            await update.message.reply_text(result.strip())
        else:
            await update.message.reply_text("Please mention me in your message to get a response.")

def main():
    token = os.getenv("Telegram_Api_Key")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_masseg))
    app.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
     main()
