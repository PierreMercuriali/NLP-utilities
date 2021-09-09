"""
    searchContexts.py 

    Extracts contexts a keyword appears in a set of TXT files, for each word in a user-defined list of keywords.
    Outputs a CSV (left context, keyword, right context, filename)
    Instructions: place .py file in folder alongside txt files and launch.

"""

import sys, io, re, tqdm
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

def quickAppendUnicode(content, fn):
    with io.open(fn, "a", encoding="utf-8") as f:
        f.write(content)
        
def quickSave(content, fn):
    with open(fn, "w") as f:
        f.write(content)
    print("\tcontent saved")
    
def preprocess(text):#removes lineskips
	return " ".join(text.split("\n"))

mypath      = u"./"
savepath	= u"./data/"

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


#list of user-defined keywords
full_list = ["extract honey", "break open", "use a hammer", "stone hammer", "hammer and anvil", "stone tool"]
offset = 40

print("searching contexts for", len(full_list), "keyword(s)...")
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
			try:
				quickAppendUnicode("\n"+left_context + "|" + keyword + "|" + right_context + "|" + filename, savepath+"concordances.csv")
			except:
				err = "append"
		
#try:
#	quickSaveUnicode("\n".join(concordances), savepath+"concordances.csv")
#except Exception as e: 
#	print("\t error saving txt")
#	print("\t", e)
