"""
    keywordsAnalysis.py 

    Simple statistics on keywords within a list of txt files.
    Keyword extraction works with RAKE algorithm.
    Instructions: place .py file in folder alongside txt files and launch. 
"""

import sys, io, re, tqdm
from os import listdir,mkdir
from os.path import isfile, join
from rake_nltk import Rake


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
    
def preprocess(text):#removes lineskips
	return " ".join(text.split("\n"))

mypath      = u"./"
savepath	= u"./data/"
sw = "i,me,my,myself,we,our,ours,ourselves,you,your,yours,yourself,yourselves,he,him,his,himself,she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom,this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,a,an,the,and,but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during,before,after,above,below,to,from,up,down,in,out,on,off,over,under,again,further,then,once,here,there,when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than,too,very,s,t,can,will,just,don,should,now,".split(",")
p = "()[],.;?!:_\"\'°′-=+*–"
try: 
    mkdir(savepath) 
except OSError as error: 
    print(error)  
onlyfiles   = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles   = [f for f in onlyfiles if f[-3:]=='txt']

keywords_lists = []
full_list = []
for filename in onlyfiles:
    print("*", filename)
    text = preprocess(quickLoad(filename))
    r = Rake(stopwords = sw, punctuations = p, min_length=1, max_length=3)
    r.extract_keywords_from_text(text)
    full_list+=r.get_ranked_phrases()
    keywords_lists.append(r.get_ranked_phrases())
#   keywords = r.get_ranked_phrases_with_scores()   
full_list = list(set(full_list))#no repetitions

d = {}
for keyword in tqdm.tqdm(full_list):
	for i in range(len(keywords_lists)):
		if keyword in keywords_lists[i]:
			if keyword in d.keys():
				d[keyword]+=1
			else:
				d[keyword]=1
				
sorted_d = {k: v for k, v in reversed(sorted(d.items(), key=lambda item: item[1]))}				

try:
	quickSaveUnicode(str(sorted_d), savepath+"keywords.txt")
except Exception as e: 
	print("\t error saving txt")
	print("\t", e)
