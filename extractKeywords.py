"""
    extractKeywords.py 
    Extracts a list of keywords from a set of txt files.
    Keyword extraction based on RAKE.
    Instructions: place .py file in folder alongside txt files and launch. 
"""

import sys, io, re
from os import listdir,mkdir
from os.path import isfile, join

def quickLoad(fn):
	with io.open(fn, "r" ,encoding="utf-8") as f:
		r = f.readlines()
	return "".join(r)
def quickSaveUnicode(content, fn):
    with io.open(fn, "w", encoding="utf-8") as f:
        f.write(content)
    print("\tcontent saved")
def quickSave(content, fn):
    with open(fn, "w") as f:
        f.write(content)
    print("\tcontent saved")
    
def preprocess(text):#removes lineskips, add a stopword to keep proper splitting
	return " and ".join(text.split("\n"))
	
def keywords_candidates(text):
	global stopwords
	nop = re.sub(r'[^\w\s]','',text)#remove punctuation
	bag = nop.split(" ")
	res = []
	current_expression = ''
	for word in bag:#complicated splitting to keep expressions of several words intact
		if word.lower() in stopwords:
			if not(current_expression)=="": 
				res.append(current_expression)
			current_expression = ""
		else:
			current_expression = current_expression + " " + word
	return res
	
stopwords = "i,me,my,myself,we,our,ours,ourselves,you,your,yours,yourself,yourselves,he,him,his,himself,she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom,this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,a,an,the,and,but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during,before,after,above,below,to,from,up,down,in,out,on,off,over,under,again,further,then,once,here,there,when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than,too,very,s,t,can,will,just,don,should,now,".split(",")

mypath      = u"./"
savepath	= u"./data/"

try: 
    mkdir(savepath) 
except OSError as error: 
    print(error)  
onlyfiles   = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles   = [f for f in onlyfiles if f[-3:]=='txt']

for filename in onlyfiles:
    print("*", filename)
    text = preprocess(quickLoad(filename))
    keywords = keywords_candidates(text)
    
try:
    quickSaveUnicode("\n".join(keywords), savepath+"keywords.txt")
except Exception as e: 
    print("\t error saving txt")
    print("\t", e)
