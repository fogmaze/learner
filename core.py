import random
import os

WEIGHT_LESS_EACH = 3.0
TIME_LIMIT_EACH_REQUEST = 0.3

def my_rand(start,stop):
    s = random.random()
    return start + s * (stop-start)

def delEnter(s:str)->str:
    new_str = ''
    for c in s:
        if c != '\n' and c != '\r':
            new_str += c
    return new_str

def completePathFormat(s:str)->str:
    if s[len(s)-1] != '/':
        s+= '/'
    return s

def sumList(list:list)->float:
    sum = 0
    for item in list:
        sum += item
    return sum
    

class Err(Exception):pass

class Book:
    def delWord(self,index:int):
        extraWeight = WEIGHT_LESS_EACH - self.weighted[index]
        del self.items[index]
        #self.weighted = np.delete(self.weighted,index)
        del self.weighted[index]
        #self.weighted -= extraWeight / self.weighted.shape[0]
        self.weighted = [w-(extraWeight/len(self.weighted)) for w in self.weighted]

    @staticmethod
    def getAnsFromInternet(que,mode = 'preset'):
        raise Err('not defined')

    def add(self, que, ans=None) -> str:
        que = delEnter(que)
        for added_item in self.items:
            if que == added_item[0]:
                return None
        if ans:
            ans = delEnter(ans)
            self.items.append([que,ans])
            self.weighted.append(1.0)
            #self.weighted = np.append(self.weighted,1)
            return ans
        ans_got = self.getAnsFromInternet(que)
        self.items.append([que,delEnter(ans_got)])
        self.weighted.append(1.0)
        #Eself.weighted = np.append(self.weighted,1)
        return ans_got
        
    def __init__(self,root_path = './'):
        try:
            self.inited = True
            if root_path[len(root_path)-1] != '/':
                root_path += '/'
            if not os.path.isdir(root_path):
                self.createNewBookDir(root_path)
            self.FILE_ROOT = root_path
            fl_ques = open(self.FILE_ROOT+'que.txt','r',encoding='utf-8')
            fl_Anss = open(self.FILE_ROOT+'ans.txt','r',encoding='utf-8')
            fl_weighted = open(self.FILE_ROOT+'weighted.txt','r',encoding='utf-8')
            #li_w = list() 
            self.items = list()
            self.weighted = list()
            for que in fl_ques:
                ans = fl_Anss.readline()
                self.items.append([delEnter(que),delEnter(ans)])
                #li_w.append(float(fl_weighted.readline()))
                self.weighted.append(float(fl_weighted.readline()))
            #self.weighted = np.array(li_w)
        finally:
            fl_ques.close()
            fl_Anss.close()
            fl_weighted.close()

    def getUnfamiliarLength(self) -> int:
        return sumList([w for w in self.weighted if w > 1])

    def getRandWord(self):
        w_len = sumList(self.weighted)
        seak = my_rand(0,w_len)
        which = 0
        i = 0
        num = 0
        while(True):
            if seak-num < self.weighted[i]:
                which = i
                break
            num += self.weighted[i]
            i += 1
        self.weighted[which] = self.weighted[which] - WEIGHT_LESS_EACH
        #self.weighted += WEIGHT_LESS_EACH/float(w_len) 
        self.weighted = [(w + WEIGHT_LESS_EACH/float(w_len)) for w in self.weighted]
        return self.items[which][0],self.items[which][1],which

    def release(self):
        self.inited = False
        fl_ques = open(self.FILE_ROOT+'que.txt','w',encoding='utf-8')
        fl_Anss = open(self.FILE_ROOT+'ans.txt','w',encoding='utf-8')
        fl_weighted = open(self.FILE_ROOT+'weighted.txt','w',encoding='utf-8')

        for w in self.weighted:
            fl_weighted.write(str(w) + '\n')
        for each in self.items:
            if each[0][len(each[0])-1] != '\n':
                each[0] += '\n'
            if each[1][len(each[1])-1] != '\n':
                each[1] += '\n'
            fl_ques.write(each[0])
            fl_Anss.write(each[1])
        
        fl_weighted.close()
        fl_ques.close()
        fl_Anss.close()

    def releaseIfNeed(self):
        if self.inited:
            self.release()
            self.inited = False

    def __del__(self):
        if self.inited:
            print('class<getRandWord> releasing automatically')
            self.release()
    
    def createNewBookDir(self,path:str):
        if path[len(path)-1] != '/':
            path+= '/'
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(path+'que.txt','w'),open(path+'ans.txt','w'),open(path+'weighted.txt','w'):
            pass
    

