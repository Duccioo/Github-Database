# link x
# bold x
# italic x
# undeline x
# code inline


# MARKDOWN V2 TELEGRAM
# *bold \*text*
# _italic \*text_
# __underline__
# ~strikethrough~
# ||spoiler||
# *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
# [inline URL](http://www.example.com/)
# [inline mention of a user](tg://user?id=123456789)
# `inline fixed-width code`
# ```
# pre-formatted fixed-width code block
# ```
# ```python
# pre-formatted fixed-width code block written in the Python programming language
# ```


def convert_link_01(string, start=0 , string_modify="", string_finale=""):
    # markdonw: [inline URL](http://www.example.com/)
    # hml: <a href="http://www.example.com/">inline URL</a>
    string_mezzo=""
    if(string_modify!=""):
        string_mezzo= string_modify
    else:
        string_mezzo= string
    indice = 0
    url = ""
    inline_url =""
    while (indice < len(string_mezzo)):       
        if(string_mezzo[indice] =="["):
            # print("invio questo", string_mezzo[(indice+1):] )
            string_finale,url, inline_url, string_mezzo  = convert_link_01(string=string,start=0,string_modify= string_mezzo[(indice+1):], string_finale=string_finale)
        
            if(url!=""):
                string_finale,url, inline_url, string_m = convert_link_01(string_mezzo,start=0, string_modify="", string_finale=string_finale)
                return string_finale,"fine", "", ""
                
        elif(string_mezzo[indice]=="]"):
            inline_url= string_mezzo[:(indice)]
        
            if(string_mezzo[indice+1]=="(" and string_mezzo[(indice+1):].find(")")):
            
                url=string_mezzo[(indice+2):(string_mezzo[(start):].find(")"))]
                html_complete="<a href='"+url+"'>"+inline_url+"</a>"
                new_string = string.replace("["+inline_url+"]("+url+")", html_complete)
                return( new_string, url, inline_url,new_string,)

        indice= indice+1
    return(string_finale,url, inline_url, string_mezzo)

def convert_link(string):
    final_string_yea = convert_link_01(string)
    if(final_string_yea[0]==""):
        return final_string_yea[3]
    else:
        return final_string_yea[0]
                            
                            
def convert_prototype(string="", markdown_start="", markdonw_end="", html_start="<>", html_end = "</>"):
    
    
    if(markdonw_end== markdown_start):
        final_string=""
        new_string= string.split(markdown_start)
        
        for index,word in enumerate(new_string):
            
            if(index == (len(new_string)-1)):
                final_string = final_string+word
            else:  
                if(index%2 == 0 ):
                    # pari
                    final_string=final_string+ word+html_start
                else:   
                    final_string= final_string+word+html_end
        return final_string


    for index,letter in enumerate(string):
        if(letter==markdown_start):
            if(string[(index+1):].find(markdonw_end)!= -1):
                bold_text=string[(index+1):][:(string[(index+1):].find(markdonw_end))]
                return string.replace(markdown_start+bold_text+markdonw_end,html_start +bold_text+html_end)
    return(string)

                          
                    
def convert_bold(string):
    # markdown = *bold text*
    # html = <b>bold</b>
    return (convert_prototype(string,"*","*","<b>","</b>"))
    
def convert_italic(string):
    # markdown= _italic \*text_
    # html = <i>italic</i>, <em>italic</em> 
    return (convert_prototype(string,"_","_","<em>","</em>"))

def convert_underline(string):
    # markdown:  __underline__
    # html:  <u>underline</u>, <ins>underline</ins>
    return (convert_prototype(string,"__","__","<u>","</u>"))


def convert_everything(string):
    return (convert_link(convert_bold(convert_italic(convert_underline(string)))))

