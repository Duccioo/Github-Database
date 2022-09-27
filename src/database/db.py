import requests
from requests.structures import CaseInsensitiveDict
import json
import uuid
from github import Github
from dotenv import load_dotenv
import os
from datetime import datetime, timezone, timedelta
import git


timezone_offset = +1.0  # ITALIA
tzinfo = timezone(timedelta(hours=timezone_offset))


load_dotenv()

GITHUB_TOKEN =os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPO")
POST_FILE = os.getenv("GITHUB_POST_FILE")
CIT_FILE = os.getenv("GITHUB_CIT_FILE")
USER = os.getenv("GITHUB_USER")

def download_file(file,  user, repo,branch= "main", auth= False):

    if (auth == False):
        url ='https://raw.githubusercontent.com/'+ user +"/" + repo + "/" + branch +"/"+ file
        r = requests.get(url, allow_redirects=True)
        if(r.content.decode('utf8') == '404: Not Found'):
            print("bop bip FILE"+file+ " not found")
            print("creating file.... bip bip")
            print("mhhh I dont have the permission to do that...")
            return -1
        else:
            data = json.loads(r.content.decode('utf8'))
            return data

    else:
        # headers = CaseInsensitiveDict()
        # headers["Authorization"] = "token " + auth
        # headers["Cache-Control"] =  "no-cache"
        # headers["Pragma"] = "no-cache"
        # # url ='https://raw.githubusercontent.com/'+ user +"/" + repo + "/" + branch +"/"+ file
        # r = requests.get(url, headers=headers)

        g = Github(auth)
        print(user+"/"+repo)
        repo = g.get_repo(user+"/"+repo)
        file = repo.get_contents(file, ref=branch)  # Get file from branch
        data = file.decoded_content.decode("utf-8")
        if( data == '404: Not Found'):

            # Se il file non esiste allora creo un file vuoto
            print("FILE"+file+ " not found bip bop")
            print("bop bop creating file")
            repo.create_file(file, "aggiornamento via script", "[]", branch)
            print(file+ ' CREATED')
            result = []
            return result
            
            
        else:
            # data = json.loads(r.content.decode('utf8'))
            # print("pspssp:",data)
            result = json.loads(data) # Get raw string data
            return result
    

def upload_file(file_to_write, repo, auth, content, file_to_open=False, branch='main', comment="upload with Duccio ;)"):
    g = Github(auth)
    repo = g.get_user().get_repo(repo)
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

    if file_to_open != False :
        with open(file_to_open, 'r') as file:
             content = file.read()

    git_file = file_to_write
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "aggiornamento via script", content, contents.sha, branch)
        print(git_file + ' UPDATED')
        return "UPDATED"
    else:
        repo.create_file(git_file, "aggiornamento via script", content, branch)
        print(git_file + ' CREATED')
        return "CREATED"


class database:
    def __init__(self, github_token, repo, post, cit, user):

        self.user = user
        self.auth = github_token
        self.path_to_post =post
        self.path_to_cit = cit
        self.repo = repo

        # manca il controllo 
        self.post = download_file(self.path_to_post,self.user,self.repo,auth=self.auth)
        self.cit = download_file(self.path_to_cit,self.user,self.repo,auth=self.auth)

    def upload(self, data=False,file="post" ,comment=False):
        if (data== False):
            if(file == "post"):
                data1=json.dumps(self.post,indent = 4, sort_keys=True)
            elif(file== "cit"):
                data1=json.dumps(self.cit,indent = 4, sort_keys=True)
        else:
            data1=data

        if(file == "post"):
            if(comment==False):
                upload_file(self.path_to_post,self.repo, self.auth,data1)
            else:
                upload_file(self.path_to_post,self.repo, self.auth,data1, comment=comment)
        elif(file == "cit"):
            if(comment==False):
                upload_file(self.path_to_cit,self.repo, self.auth,data1)
            else:
                upload_file(self.path_to_cit,self.repo, self.auth,data1, comment=comment)
        else:
            return -1
        
    def find_post(self,titolo="", id=False):
        if(id == False):
            for i in range(len(self.post)):
                if (str(self.post[i]["titolo"]) == str(titolo)):
                    return i
        else:
            for i in range(len(self.post)):
                if (int(self.post[i]["id"]) ==int( id)):
                    return i
        return -1
    
    
    def delete_post(self,titolo):
        # controllo che il post esista
        indice = self.find_post(titolo)
        if(indice== -1):
            return -1
        else:
            self.post.pop(indice)

    def delete_last_post(self):
        self.post.pop()
        
    def add_post(self,titolo,link,paragrafo,copertina=False,immagini=False,visibile=False, date= datetime.now(tz=tzinfo)):
        id= uuid.uuid4().int
        data=self.post
        # controllo se esiste gia' un file con quel nome
        exist = self.find_post(titolo)
        if(exist== -1):
          
            # Nome non trovato quindi aggiungo il post
            self.post.insert(1,{
                "id": id,
                "titolo": titolo,
                "link_titolo":link,
                "copertina": copertina,
                "paragrafo":paragrafo,
                "immagini": immagini,
                "visibile": visibile,
                "data":str(date.timestamp())
            })
          
          
            return self.post
        else:
            # se esiste già:
            return -1

    def change_visibilita_post(self,change_to=True,index=0,titolo="",auto=True):
        if(titolo != ""):
            index =self.find_post(titolo)

        if(index != -1):
            if(auto == True):
                if(self.post[index]["visibile"] == True):
                    
                    self.post[index]["visibile"]= False
                    return False
                else:
                    
                    self.post[index]["visibile"] = True
                    return True
            else:
                self.post[index]["visibile"] = change_to
                return change_to
        else:
            return -1
        




if __name__ == "__main__":
    data_post= database(GITHUB_TOKEN,REPO,POST_FILE,CIT_FILE,USER)
    data_post.add_post("3","asdsada","asdasdasdasda")
    data_post.upload(file="post")
    
    
    