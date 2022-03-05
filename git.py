import os
import sys
from github import Github
import base64


def getRepo()->Github:
    return Github(login_or_token='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').get_repo('fogmaze/learner')

def saveFile(file):
    if not os.path.isdir(os.path.dirname(file.path)) and os.path.dirname(file.path) != '':
        print(os.path.dirname(file.path))
        os.mkdir(os.path.dirname(file.path))
    with open(file.path,'w',encoding='utf-8') as f:
        f.write(base64.b64decode(file.content).decode('utf8'))

def DownloadFolder(repo,path:str):
    contents = repo.get_contents(path)
    for content in contents:
        saveFile(content)

if __name__ == '__main__':
    previous_arg = ''
    Arg = {}
    for arg in sys.argv:
        if arg == "-d":
            Arg['method'] = 'download'
        if previous_arg == '-d':
            Arg['download_path'] = arg
        previous_arg = arg

    repo =  getRepo()
    
    if Arg['method'] == 'download':
        DownloadFolder(repo,Arg['download_path'])
    
