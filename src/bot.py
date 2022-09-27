
import functools  
import logging
from dotenv import load_dotenv
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    
)

# mie librerie:

load_dotenv()   

from uploads.image_upload import uploadImage
from database.db import database
from utility.make_text import bip_bop
from utility.handle_cit import (
    choice_aggiungo_cit, 
    choice_visualizzo_cit)

from utility.handle_post import (
    elimina_post, 
    visualizzo_post, 
    cambia_visibilita_post,                             
    choice_visualizzo_post, 
    indietro_visualizzo_post,
    aggiungo_post_titolo,
    aggiungo_post_copertina,
    aggiungo_post_fine,
    aggiungo_post_link,
    aggiungo_post_paragrafo)




GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPO"]
POST_FILE = os.environ["GITHUB_POST_FILE"]
CIT_FILE = os.environ["GITHUB_CIT_FILE"]
USER = os.environ["GITHUB_USER"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
USER_ID = os.environ["TELEGRAM_USER_ID"]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING, AGGIUNGO_POST,VISUALIZZO_POST,AGGIUNGO_CIT, VISUALIZZO_CIT = range(5)
print(CHOOSING)

reply_keyboard = [
    ["Aggiungo Post", "Visualizzo Post"],
    ["Aggiungo Cit", "Visualizzo Cit"],
    ["Lascia sta"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)


# ------------------------------------START--------------------------#
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   
    if(update.message.from_user.id == int(USER_ID)):
        await update.message.reply_text(
        bip_bop()+"\nCiao duccio come la va"+bip_bop(),
        reply_markup=markup,
        )
        return "CHOOSING"
    else:
        
        await update.message.reply_text(
            bip_bop()+"Oh ma chi sei eh? Attaccati al cazzo va",reply_markup= None
        )
        return ConversationHandler.END

async def indietro_to_choosing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Va bene, cosa vuoi fare?"+bip_bop())
    return "CHOOSING"

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   
    if(update.message.from_user.id == int(USER_ID)):
        await update.message.reply_text(
        bip_bop()+"\nCiao duccio come la va"+bip_bop(),
        reply_markup=markup,
        )
        return "CHOOSING"
    else:
        
        await update.message.reply_text(
            bip_bop()+"Oh ma chi sei eh? Attaccati al cazzo va",reply_markup= None
        )
        return ConversationHandler.END

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(bip_bop()+ bip_bop()+"...See You Space Cowboy..."+bip_bop()
        ,
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def main(token) -> None:

    
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()


    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            "CHOOSING": [
                MessageHandler(filters.Regex("^(Aggiungo Post)$"), functools.partial(aggiungo_post_titolo, new_post=new_post)),
                MessageHandler(filters.Regex("^Visualizzo Post$"), functools.partial(choice_visualizzo_post, data=data_post)),
                MessageHandler(filters.Regex("^Aggiungo Cit$"), choice_aggiungo_cit),
                MessageHandler(filters.Regex("^Visualizzo Cit$"), choice_visualizzo_cit),
                CommandHandler("menu", menu),
            ],
            "VISUALIZZO_POST": [
                CallbackQueryHandler(indietro_to_choosing, pattern="^indietro"),
                CallbackQueryHandler(functools.partial(visualizzo_post, data=data_post, notimage="./image/notimage.jpg"), pattern="^visualizza"),

                # ------
                 CommandHandler("menu", menu),
                MessageHandler(filters.Regex("^(Visualizzo Post | Visualizzo| Post|post | visualizzo)$"),functools.partial(choice_visualizzo_post, data=data_post)),
                ],
            "EDIT_POST":[
                CallbackQueryHandler(functools.partial(indietro_visualizzo_post, data=data_post), pattern="^indietro"),
              
                CallbackQueryHandler(functools.partial(elimina_post, data=data_post), pattern="^elimina"),
                CallbackQueryHandler( functools.partial(cambia_visibilita_post, data=data_post), pattern="^visibilita"),

                # ------MENU
                CommandHandler("menu", menu),
                MessageHandler(filters.Regex("^Visualizzo Post$"),functools.partial(choice_visualizzo_post, data=data_post)),
            ],
           
            "ADD_POST_PARAGRAFO":[
                CallbackQueryHandler(indietro_to_choosing, pattern="^indietro"),
                MessageHandler(filters.TEXT & ~filters.COMMAND,functools.partial(aggiungo_post_paragrafo)),

                # ------MENU
                 CommandHandler("menu", menu),
            ],
            "ADD_POST_COPERTINA":[
                CallbackQueryHandler(indietro_to_choosing, pattern="^indietro"),
                MessageHandler(filters.TEXT & ~filters.COMMAND,functools.partial(aggiungo_post_copertina)),

                # -----MENU
                 CommandHandler("menu", menu),
            ],
            "ADD_POST_LINK":[
                CallbackQueryHandler(indietro_to_choosing, pattern="^indietro"),
                MessageHandler(filters.Document.IMAGE | filters.Document.JPG | filters.PHOTO | filters.VIDEO | filters.Document.GIF | filters.Document.MP4 | filters.Document.VIDEO | filters.Regex("^(skip|niente|avanti|0)$") & ~filters.COMMAND,functools.partial(aggiungo_post_link)),
                
                # -----MENU
                CommandHandler("menu", menu),    
            ],
            "ADD_POST_END":[
                CallbackQueryHandler(indietro_to_choosing, pattern="^indietro"),
                MessageHandler(filters.TEXT & ~filters.COMMAND,functools.partial(aggiungo_post_fine, data=data_post)),

                
                # -----MENU
                CommandHandler("menu", menu),
            ],
            "EDIT_POST_PARAGRAFO":[

            ],
            "CIT":[
                MessageHandler(filters.Regex("^Aggiungo Cit$"), choice_aggiungo_cit),
                MessageHandler(filters.Regex("^Visualizzo Cit$"), choice_visualizzo_cit),
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Lascia sta$"), done)],
    )

    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":

    new_post={}

    
    data_post = database(GITHUB_TOKEN,REPO,POST_FILE,CIT_FILE,USER)

    main(TELEGRAM_TOKEN)