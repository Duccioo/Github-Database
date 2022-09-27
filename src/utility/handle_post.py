
from uuid import uuid4
from database.db import database
from utility.make_text import make_beautiful_html, bip_bop
from uploads.image_upload import uploadImage
from utility.markdown_html import convert_everything



from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)


# funzione per visualizzare tutti post
async def choice_visualizzo_post(update: Update, context: ContextTypes.DEFAULT_TYPE, data) -> int:
    i=0
    keyboard =[]
    for element in data.post:
        key_element=[]
        if(element["visibile"]== True):
            key_element.append(InlineKeyboardButton("✅"+element["titolo"]+"\n", callback_data="visualizza "+str(i)))  
        else:
            key_element.append(InlineKeyboardButton("❎"+element["titolo"]+"\n", callback_data="visualizza "+str(i)))  
        keyboard.append(key_element)
        i=i+1
    key_element=[]
    key_element.append(InlineKeyboardButton("INDIETRO", callback_data="indietro"))
    keyboard.append(key_element)
    keyboard_message_tutti_post= InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
      bip_bop()+" ecco a te tutti i post memorizzati "+bip_bop(),
        reply_markup=keyboard_message_tutti_post,
    )
      
    return "VISUALIZZO_POST"

# funzione per visualizzare tutti i post quando torno indietro
async def indietro_visualizzo_post(update: Update, context: ContextTypes.DEFAULT_TYPE, data) -> int:
    query = update.callback_query
    await query.answer()
    await query.delete_message()
    i=0
    keyboard =[]
    for element in data.post:
        key_element=[]
        if(element["visibile"]== True):
            key_element.append(InlineKeyboardButton("✅"+element["titolo"]+"\n", callback_data="visualizza "+str(i)))  
        else:
            key_element.append(InlineKeyboardButton("❎"+element["titolo"]+"\n", callback_data="visualizza "+str(i)))  
        keyboard.append(key_element)
        i=i+1
    key_element=[]
    key_element.append(InlineKeyboardButton("INDIETRO", callback_data="indietro"))
    keyboard.append(key_element)
    keyboard_message_tutti_post= InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
     bip_bop()+" ecco a te tutti i post memorizzati "+bip_bop(),
        reply_markup=keyboard_message_tutti_post,
    )
    return "VISUALIZZO_POST"

# funzione per visualizzare 1 post
async def visualizzo_post(update: Update, context: ContextTypes.DEFAULT_TYPE, data : database, notimage) -> int:
    query = update.callback_query
    await query.answer()
    index=int(query.data.split(" ")[1])
    keyboard = [
                    [
                        InlineKeyboardButton("*️⃣modifica", callback_data="modifica "+str(index)),
                        InlineKeyboardButton("❌elimina", callback_data="elimina "+str(index)),
                    ]
                ]
    key_element = []
    if(data.post[index]["visibile"]== True):
        key_element.append(InlineKeyboardButton("✅visibile", callback_data="visibilita "+str(index)))
    else:
        key_element.append(InlineKeyboardButton("❎non visibile", callback_data="visibilita "+str(index)))
    keyboard.append(key_element)
    key_element=[]
    key_element.append(InlineKeyboardButton("↩️indietro", callback_data="indietro "+str(index)))
    keyboard.append(key_element)
    reply_markup = InlineKeyboardMarkup(keyboard)
    info = data.post[int(index)]

    await query.delete_message()
    await query.message.reply_text(make_beautiful_html(info["copertina"],info["titolo"],info["paragrafo"],info["link_titolo"],info["immagini"],info["data"]), parse_mode=constants.ParseMode("HTML"),reply_markup=reply_markup)
    
    return "EDIT_POST"

async def cambia_visibilita_post(update: Update, context: ContextTypes.DEFAULT_TYPE, data: database) -> int:
 
    query = update.callback_query
    await query.answer()
    index=int(query.data.split(" ")[1])
    data.change_visibilita_post(index=int(index))
    data.upload(file="post")
    keyboard = [
                    [
                        InlineKeyboardButton("*️⃣modifica", callback_data="modifica "+str(index)),
                        InlineKeyboardButton("❌elimina", callback_data="elimina "+str(index)),
                    ]
                ]
    key_element = []
    if(data.post[index]["visibile"]== True):
        key_element.append(InlineKeyboardButton("✅visibile", callback_data="visibilita "+str(index)))
    else:
        key_element.append(InlineKeyboardButton("❎non visibile", callback_data="visibilita "+str(index)))
    keyboard.append(key_element)
    key_element=[]
    key_element.append(InlineKeyboardButton("↩️indietro", callback_data="indietro "+str(index)))
    keyboard.append(key_element)
                    
    reply_markup = InlineKeyboardMarkup(keyboard)
    info = data.post[int(index)]


    await query.edit_message_text( make_beautiful_html(info["copertina"],info["titolo"],info["paragrafo"],info["link_titolo"],info["immagini"],info["data"]),parse_mode="HTML",reply_markup=reply_markup)

    return "EDIT_POST"





async def elimina_post(update: Update, context: ContextTypes.DEFAULT_TYPE, data:database) -> int:

    query = update.callback_query
    await query.answer()
    index=int(query.data.split(" ")[1])
    
    data.post.pop(index)
    data.upload(file="post")

    await query.delete_message()
    i=0
    keyboard =[]
    for element in data.post:
        key_element=[]
        if(element["visibile"]== True):
            key_element.append(InlineKeyboardButton("✅"+element["titolo"]+"\n", callback_data="visualizza "+str(i)))  
        else:
            key_element.append(InlineKeyboardButton("❎"+element["titolo"]+"\n", callback_data="visualizza "+str(i)))  
        keyboard.append(key_element)
        i=i+1
    key_element=[]
    key_element.append(InlineKeyboardButton("INDIETRO", callback_data="indietro"))
    keyboard.append(key_element)
    keyboard_message_tutti_post= InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
       bip_bop()+"ecco a te tutti i post memorizzati"+bip_bop(),
        reply_markup=keyboard_message_tutti_post,
    )
    return "VISUALIZZO_POST"
    
    
    
    return "EDIT_POST"


async def aggiungo_post_titolo(update: Update, context: ContextTypes.DEFAULT_TYPE,new_post) -> int:
    new_post={}
    keyboard =[]
    key_element=[]
    key_element.append(InlineKeyboardButton("↩️indietro", callback_data="indietro"))
    keyboard.append(key_element)
    reply_markup = InlineKeyboardMarkup(keyboard)
        
    await update.message.reply_text(bip_bop()+"Ottimo!\nInviami il titolo"+bip_bop(),reply_markup=reply_markup)

    return "ADD_POST_PARAGRAFO"

async def aggiungo_post_paragrafo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
  
    keyboard =[]
    key_element=[]
    key_element.append(InlineKeyboardButton("↩️indietro", callback_data="indietro"))
    keyboard.append(key_element)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data["new_post"]={
        "titolo":"",
        "copertina":"",
        "paragrafo":[],
        "link":""
    }
    context.user_data["new_post"]["titolo"] = update.message.text


    await update.message.reply_text("Ottimo"+bip_bop()+"il titolo quindi è: "+context.user_data["new_post"]["titolo"]+"!\n~~~~~~~~~~~~~\nInviami il paragrafo"+bip_bop(),reply_markup=reply_markup)

    return "ADD_POST_COPERTINA"

async def aggiungo_post_copertina(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
   
    keyboard =[]
    key_element=[]
    key_element.append(InlineKeyboardButton("↩️indietro", callback_data="indietro"))
    keyboard.append(key_element)
    reply_markup = InlineKeyboardMarkup(keyboard)
    p= update.message.text_markdown_v2.split(".\n\n")
    
    for element in p:
        context.user_data["new_post"]["paragrafo"].append(convert_everything( element.replace("\\","")))
        print("paragrafo-->",( element.replace("\\","")))


    await update.message.reply_text(bip_bop()+"ottimo il testo quindi è: \n"+update.message.text_markdown_v2_urled+"\n\~\~\~\~\~\~\~\~\~\~\~\~ \nInviami l'immagine copertina",reply_markup=reply_markup,parse_mode="MarkdownV2")

    return "ADD_POST_LINK"

async def aggiungo_post_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard =[]
    key_element=[]
    key_element.append(InlineKeyboardButton("↩️indietro", callback_data="indietro"))
    keyboard.append(key_element)
    reply_markup = InlineKeyboardMarkup(keyboard)
    print(update.message.text)

    if (update.message.text != None):
        text = update.message.text
        context.user_data["new_post"]["copertina"] = False
        await update.message.reply_text("Ottimo l'immagine di copertina"+bip_bop() +"è: nessuna!\n~~~~~~~~~~~~~\nInviami il link all'articolo"+bip_bop(),reply_markup=reply_markup)
    else:
        # except:
        print("no text")
        try:
            photo_file = await update.message.document.get_file()
            print(photo_file)
        except:
            photo_file = await update.message.photo.get_file()
        photo_bit= await photo_file.download_as_bytearray()
        image_list_name=  context.user_data["new_post"]["titolo"].split(" ")
        image_name= ""
        for word in image_list_name:
            image_name +=word+"-"
        image_name =  image_name[:-1]
        context.user_data["new_post"]["copertina"] = uploadImage(photo_file.file_path,image_name)
        await update.message.reply_text(bip_bop()+"ottimo l'immagine di copertina" +bip_bop() +"è:"+context.user_data["new_post"]["copertina"]+"\n~~~~~~~~~~~~~\nInviami il link all'articolo",reply_markup=reply_markup)
    return "ADD_POST_END"

async def aggiungo_post_fine(update: Update, context: ContextTypes.DEFAULT_TYPE,data:database) -> int:
    
    keyboard =[]
    key_element=[]
    key_element.append(InlineKeyboardButton("↩️indietro", callback_data="indietro"))
    keyboard.append(key_element)
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = update.message.text
    if(text=="niente" or text=="0" or text=="skip"):
        context.user_data["new_post"]["link"] = False
    else:
        context.user_data["new_post"]["link"] = update.message.text
    
    titolo= context.user_data["new_post"]["titolo"]
    paragrafo= context.user_data["new_post"]["paragrafo"]
    copertina= context.user_data["new_post"]["copertina"]
    link= context.user_data["new_post"]["link"] 
    await update.message.reply_text("Ottimo"+bip_bop()+"!\nCREAZIONE DEL POST IN CORSO.....\n")
    
    data.add_post(titolo,link,paragrafo,copertina,visibile=False)
    data.upload(file="post")

    await update.message.reply_text("BIP BOP BIP... POST creato\nOCCHIO, è ancora 'non visibile'"+bip_bop())
    return "CHOOSING"






