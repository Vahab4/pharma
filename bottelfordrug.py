import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import nest_asyncio

# Apply nest_asyncio to allow nested event loops (necessary in certain environments like Jupyter)
nest_asyncio.apply()

# Set up logging to catch errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to get RxCUI for a given drug name
def get_rxcui(drug_name):
    url = f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}"
    response = requests.get(url)
    data = response.json()
    try:
        return data["idGroup"]["rxnormId"][0]
    except (KeyError, IndexError):
        return None

# Function to get drug forms, strengths, and types using RxCUI
def get_prescriptions_by_rxcui(rxcui):
    url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/related.json?tty=SCD+SBD"
    response = requests.get(url)
    data = response.json()
    results = []
    try:
        concepts = data["relatedGroup"]["conceptGroup"]
        for group in concepts:
            for concept in group.get("conceptProperties", []):
                results.append({
                    "name": concept["name"],  # Full drug name with strength/form
                    "rxcui": concept["rxcui"],
                    "tty": concept["tty"]  # Term type (SCD = clinical, SBD = branded)
                })
        return results
    except Exception as e:
        return f"Error: {e}"

# Function to format a drug prescription in Latin
def format_latin_prescription(drug_full_name):
    """
    Example input: 'Acetaminophen 500 MG Oral Tablet'
    Example output:
        Rp.: Acetaminopheni 0.5
        D.t.d. №10 in tab.
        S. Take 1 tablet every 6 hours if needed for pain/fever.
    """
    # Basic parsing logic
    words = drug_full_name.split()
    try:
        latin_name = words[0] + "i"  # Crude Latinization, you can customize it
        dose = words[1]
        unit = words[2]
        form = words[-2].lower()[:3] + '.'  # Tab., Cap., Inj.
    except IndexError:
        return "Unable to parse drug name."

    return f"""Rp.: {latin_name} {dose}
D.t.d. №10 in {form}
S. Take 1 {form[:-1]} every 6 hours if needed for fever or pain.
"""

# Function to start the bot
async def start(update: Update, context):
    await update.message.reply_text("Welcome to the prescription bot! Please type a drug name.")

# Function to handle drug name input and return a prescription
async def get_prescription(update: Update, context):
    drug_name = update.message.text.strip()  # Get drug name from the user's message
    rxcui = get_rxcui(drug_name)

    if not rxcui:
        await update.message.reply_text(f"Drug '{drug_name}' not found.")
    else:
        prescriptions = get_prescriptions_by_rxcui(rxcui)
        if isinstance(prescriptions, str):
            await update.message.reply_text(prescriptions)
        elif not prescriptions:
            await update.message.reply_text("No prescription forms found.")
        else:
            await update.message.reply_text(f"\nLatin-style prescriptions for '{drug_name}':\n")
            for i, drug in enumerate(prescriptions[:5], 1):  # Limit output to 5 prescriptions
                prescription = format_latin_prescription(drug['name'])
                await update.message.reply_text(
                    f"{i}. {drug['name']} → Latin prescription:\n{prescription}\n{'-' * 50}")

# Main function to set up the bot
async def main():
    bot_token = '7616154635:AAEqBZQcreOTN7T_JHecixzLM88pC4K_QMw'  # Replace with your bot's token
    application = Application.builder().token(bot_token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))

    # Add message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_prescription))

    # Start the bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
