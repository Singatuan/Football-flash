import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
TEAM_ID = 33  # Example: Manchester United

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Type /live to get current score.")

async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://v3.football.api-sports.io/fixtures?team={TEAM_ID}&live=all"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()

    if data["response"]:
        match = data["response"][0]
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        score = match["goals"]
        text = f"⚽ {home} {score['home']} - {score['away']} {away}"
    else:
        text = "No live matches found."

    await update.message.reply_text(text)

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("live", live))
    app.run_polling()
