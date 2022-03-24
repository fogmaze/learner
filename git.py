import json
import os
import sys
from tkinter import E
from turtle import up
from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile
from typing import List
import base64
from argparse import ArgumentParser
from os import path

MOBIO = True

config = False
with open('gitkey.json','r',encoding='utf-8') as config_f:
    config = json.load(config_f)

if not config:
    print('config file not found')


def splitBlank(str:str)->list:
    res = []
    inMark = False
    lastBlank = 0
    for i in range(len(str)):
        if str[i] == ' ' and not inMark:
            res.append(str[lastBlank:i].replace('"',''))
            lastBlank = i + 1
        elif str[i] == '"':
            if inMark:
                inMark = False
            else:
                inMark = True
        if i+1 == len(str):
            res.append(str[lastBlank:i+1].replace('"',''))
    return res

def format_dir(str)->str:
    if str[-1] != '/':
        return str + '/'
    return str

def openAndCreatePath(name,mode,encoding = 'defaut'):
    print(os.path.dirname(name))
    if not os.path.isdir(os.path.dirname(name)):
        os.makedirs(os.path.dirname(name))
    if encoding == 'defaut':
        return open(name,mode)
    else:
        return open(name,mode,encoding = encoding)

def getAllFileInDirGithub(repo:Repository,dirName:str)->List[ContentFile]:
    cnts = []
    try:
        cnts = repo.get_contents(dirName)
    except:
        print("it's new")
    ret = []
    while True:
        if len(cnts) == 0:
            break
        content = cnts.pop(0)
        if content.type == 'dir':
            [cnts.append(c) for c in repo.get_contents(content.path)]
        else:
            ret.append(content)
    return ret

    

def uploadDir2Github(repo:Repository,dirName):
    #dirName = format_dir(dirName)
    files = [path.join(dirName,f) for f in os.listdir(dirName)]
    while True:
        if len(files) == 0:
            break
        local_fileName =files.pop(0)
        if os.path.isdir(local_fileName):
            [files.append(path.join(local_fileName,f)) for f in os.listdir(local_fileName)]
            print('is dir:' + local_fileName)
            continue
        else:
            print('is file:' + local_fileName)
        print('uploading :'+local_fileName)
        uploadFile2Github(repo,local_fileName,local_fileName)


def uploadFile2Github(repo:Repository,filename:str,path_repo:str):
    path_repo = path_repo.replace('\\','/')
    old_content = False
    try:
        old_content = repo.get_contents(path_repo)
    except:
        print('new file in github:' + path_repo)
    if old_content:
        with open(filename,'r',encoding='utf-8') as fileLocal:
            repo.update_file(path=old_content.path,message="upload",content=fileLocal.read(),sha=old_content.sha)
    else:
        with open(filename,'r',encoding='utf-8') as fileLocal:
            repo.create_file(path=path_repo,message="upload",content=fileLocal.read())

def getRepo()->Repository:
    return Github(login_or_token=config['github_token']).get_repo(config['repo_name'])

def saveContent(content,dst_base_dir = './'):
    dst_base_dir = format_dir(dst_base_dir)
    with openAndCreatePath(dst_base_dir+content.path,'w',encoding='utf-8') as f:
        f.write(base64.b64decode(content.content).decode('utf8'))
    
def updateDir(repo:Repository,path_repo:str,GO_INSIDE_DIR = True):
    if not GO_INSIDE_DIR:
        contents = repo.get_contents(path_repo)
        for content in contents:
            if not content.type == 'dir':
                saveContent(content)
        return
    contents = getAllFileInDirGithub(repo,path_repo)
    for content in contents:
        saveContent(content)

def updateFile(repo,filename_repo,dst_base_dir = './'):
    dst_base_dir = format_dir(dst_base_dir)
    content = repo.get_contents(filename_repo)
    saveContent(content,dst_base_dir)


def command(argv):
    Arg = ArgumentParser()
    Arg.add_argument('-ud','--update',dest='update',nargs='+')
    Arg.add_argument('-s','--set',dest='set_up',nargs='+')
    Arg.add_argument('-ul','--upload',dest="upload",nargs='+')
    args = Arg.parse_args(argv)

    config = json.loads('{}')
    if os.path.isfile('gitkey.json'):
        try:
            f = open('gitkey.json','r',encoding='utf-8')
            config = json.load(f)
        finally:
            f.close()

    if not args.update == None:
        repo = getRepo()
        for mode_i in range(0,len(args.update),2):
            if args.update[mode_i] == 'dir':
                updateDir(repo,args.update[mode_i+1],config['base_dir'])
            if args.update[mode_i] == 'file' or args.update[mode_i] == 'f':
                updateFile(repo,args.update[mode_i+1],config['base_dir'])
            

    if not args.upload == None:
        repo = getRepo()
        for item in args.upload:
            if path.isdir(item):
                try:
                    uploadDir2Github(repo,item)
                except:
                    uploadDir2Github(repo,item)
                print('uploaded a dir:' + item)
            elif path.isfile(item):
                try:
                    uploadFile2Github(repo,path.join(config['base_dir'],item),item)
                except:
                    uploadFile2Github(repo,path.join(config['base_dir'],item),item)
                print('upload a file:' + item)
            else:
                print('not a file or dir:' + item)

    if not args.set_up == None:
        config = json.loads('{}')
        if os.path.isfile('gitkey.json'):
            try:
                old_configFile = open('gitkey.json','r',encoding='utf-8')
                config = json.load(old_configFile)
            finally:
                old_configFile.close()
        for opt_i in range(0,len(args.set_up),2):
            config[args.set_up[opt_i]] = args.set_up[opt_i+1]
        with open('gitkey.json','w',encoding='utf-8') as f:
            json.dump(config,f)


if __name__ == "__main__":
    argv = str(sys.argv)
    if len(sys.argv) < 2:
        MOBIO = True
        print('enter command:')
        argv = splitBlank(input())
    else:
        del argv[0]
    
    command(argv)


