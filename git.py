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

def init():
    flags = [
        'github_token',
        'repo_name',
        'base_dir',
        'ignore_files',
        'ignore_dir'
    ]
    with open('gitkey.json','r',encoding='utf-8') as config_f:
        global config
        config = json.load(config_f)
    for flag in flags:
        if not flag in config:
            config[flag] = '' 

init()

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
    if not os.path.isdir(os.path.dirname(name)):
        print(os.path.dirname(name))
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
            if not content.name in config['ignore_dir']:
                [cnts.append(c) for c in repo.get_contents(content.path)]
        else:
            print('find file {} on github'.format(content.name))
            ret.append(content)
    return ret

    

def uploadDir2Github(repo:Repository,dirName):
    #dirName = format_dir(dirName)
    if path.basename(dirName) in config:
        return
    files = [path.join(dirName,f) for f in os.listdir(dirName)]
    while True:
        if len(files) == 0:
            break
        local_fileName =files.pop(0)
        if os.path.isdir(local_fileName):
            [files.append(path.join(local_fileName,f)) for f in os.listdir(local_fileName)]
            continue
        uploadFile2Github(repo,local_fileName,local_fileName)


def uploadFile2Github(repo:Repository,filename:str,path_repo:str):
    path_repo = path_repo.replace('\\','/')
    old_content = False
    print('uploading:' + filename)
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

def saveContent(content:ContentFile,dst_base_dir = './'):
    dst_base_dir = format_dir(dst_base_dir)
    if content.name in config['ignore_files']:
        return
    with openAndCreatePath(dst_base_dir+content.path,'w',encoding='utf-8') as f:
        try:
            f.write(base64.b64decode(content.content).decode('utf8'))
        except:
            print('cannot decode by utf-8')
            f.write(base64.b64decode(content.content))
    
def updateDir(repo:Repository,path_repo:str,GO_INSIDE_DIR = True):
    if path.basename(path_repo) in config['ignore_dir']:
        return
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
    print('downloading:' + filename_repo)
    dst_base_dir = format_dir(dst_base_dir)
    content = repo.get_contents(filename_repo)
    saveContent(content,dst_base_dir)


def command(argv):
    Arg = ArgumentParser()
    Arg.add_argument('-ud','--update',dest='update',nargs='+')
    Arg.add_argument('-s','--set',dest='set_up',nargs='+')
    Arg.add_argument('-ul','--upload',dest="upload",nargs='+')
    args = Arg.parse_args(argv)

    if not args.update == None:
        repo = getRepo()
        for item in args.update:
            if path.isdir(item):
                updateDir(repo,item)
            elif path.isfile(item):
                updateFile(repo,item)
            else:
                print('not a file or dir:' + item)

    if not args.upload == None:
        repo = getRepo()
        for item in args.upload:
            if path.isdir(item):
                uploadDir2Github(repo,item)
            elif path.isfile(item):
                uploadFile2Github(repo,path.join('./',item),item)
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


