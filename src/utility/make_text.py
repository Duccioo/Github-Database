# funzione che restituisce una stringa formattata in modo appropriato in markdown
import random
from datetime import datetime
from utility.markdown_html import convert_everything

def make_beautiful_html(copertina, titolo, paragrafo, link, immagini, data):
    # Definiti:
    # -----copertina come un link ad un'immagine
    # -----titolo come un testo
    # -----paragrafo come un arrey di testo che può contenere link 
    # -----link come il primo link esterno  
    # -----immagini come un arrey di link
    # -----
    html=""
    # controllo se l'immagine di copertina è definita
    if(copertina== False):
        copertina_html= "NESSUNA IMMAGINE di COPERTINA"
    else:
        copertina_html= "<a href='"+copertina+"'>COPERTINA</a>"
    html += copertina_html+ "\n----------titolo----------\n"

    # controllo se il link è definito
    if(link== False):
        link="https://duccio.me/AAAAAAAAAAAAAAAAAAAiuto"

    titolo_html = "<a href='"+link+"'>"+"<b>"+titolo+"</b>"+"</a>"
    html += titolo_html + "\n----------paragrafo----------\n"

    # paragrafi
    for line in paragrafo:
        html+=convert_everything(line)+"\n      ~.~.~.~.~.~.        \n"

    # data di creazione
    try:
        html +="\n----------data----------\n"
        html+="<em>"+datetime.fromtimestamp(float(data)).strftime("%d/%m/%Y, %H:%M:%S")+"</em>"
    except:
        True

    
    # immagini
    if(immagini!= False):
        immagini_html= "<em>IMMAGINI:</em>"
        for imm in immagini:
            immagini_html += imm
        html+=immagini_html 

       
    return html





  
     
    

def bip_bop():

    rand=random.randrange(0,5)
    if(rand == 0):
        return " BIP BOP "
    elif(rand == 1):
        return " BOP PIP "
    elif(rand == 2):
        return " BUP BIP "
    elif(rand==3):
        return " BI BI BIP "
    elif(rand ==4):
        return " PIP BUP "



# <b>bold</b>, <strong>bold</strong> --grasseto
# <i>italic</i>, <em>italic</em> --corsivo
# <u>underline</u>, <ins>underline</ins> --sottolineato
# <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del> --linea spezzata
# <span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler> --spoiler
# <a href="http://www.example.com/">inline URL</a> --LINK




# <code>inline fixed-width code</code>
# <pre>pre-formatted fixed-width code block</pre>
# <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>



print(convert_everything("prova prova __prova__ hello *hi* _sottolineao_ metto anche un link [link](www.fattiicazzitua.com)"))