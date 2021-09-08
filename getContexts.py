"""
    getContexts.py 

    Extracts contexts a keyword appears in a set of TXT files, for each word in a list of keywords.
    Outputs a CSV (left context, keyword, right context, filename)
    Instructions: place .py file in folder alongside txt files and launch.

"""

import sys, io, re, tqdm
from os import listdir,mkdir
from os.path import isfile, join
from rake_nltk import Rake
import nltk

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
p = "()[],.;?!:_\"\'°′-=+*–#%$"
try: 
    mkdir(savepath) 
except OSError as error: 
    print(error)  
onlyfiles   = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles   = [f for f in onlyfiles if f[-3:]=='txt']



print("loading texts...")
texts = []
full_corpus = ""
for filename in tqdm.tqdm(onlyfiles):
	texts.append(preprocess(quickLoad(filename)))
	full_corpus+=texts[-1]

print("extracting keywords...")
full_list = []
MLENGTH = 3
r = Rake(stopwords = sw, punctuations = p, min_length=2, max_length=MLENGTH)
for t in tqdm.tqdm(texts):
    r.extract_keywords_from_text(t)
    full_list+=r.get_ranked_phrases()
    
def good_expression(w):#getting rid of small words and strange words
	if len(w)<4:
		return False
	else:
		if w.count(" ")>0:
			if sum([len(e) for e in w.split()])/w.count(" ") < 3: #if on average words are smaller than 4
				return False
	return True
full_list = [w for w in full_list if good_expression(w)] 
full_list = sorted(list(set(full_list)))

print("extracting keyword contexts...")
concordances = []
offset = 40
for keyword in tqdm.tqdm(full_list):
	for text_index in range(len(texts)):
		filename = onlyfiles[text_index]
		text = texts[text_index]
		left_context = ""
		right_context = ""
		err = ""
		occs = []
		try:
			occs = [m.start() for m in re.finditer(" "+keyword+" ", text)]
		except:
			occs  = []
		for occ in occs:
			try:
				left_context = text[occ-offset:occ]
			except:
				err = "left"
			try: 
				right_context = text[occ+len(keyword)+1:occ+offset+len(keyword)] 
			except:
				err = "right"
			concordances.append(left_context + "|" + keyword + "|" + right_context + "|" + filename)
		
try:
	quickSaveUnicode("\n".join(concordances), savepath+"concordances.csv")
except Exception as e: 
	print("\t error saving txt")
	print("\t", e)
