import regex
import sys
import pickle
sys.stdout.reconfigure(encoding='utf-8')
class GPTA:
    
    def __init__(self,text,vocap_size:int=0,ids:list=0):
        self.vocap_size=vocap_size
        self.num_size=self.vocap_size-256
        self.ids=ids
        self.text=text
        self.encode=[]
        self.final_vocap={}
        self.nlp()

    def nlp(self):
        pattern_tokens=r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
        with open(self.text,'rb') as f:
            file=f.read().decode('utf-8',errors='ignore')
            chunk_sentance=regex.findall(pattern_tokens,file)
            for i in chunk_sentance:
                self.encode.append(list(i.encode('utf-8')))
        return self.encode  
    ## this will merger two tokens togather and count how many time it occurs
    def get_state(self,indces):
        state={}
        for i in indces:
            for pair in zip(i,i[1:]):
                state[pair]=state.get(pair,0)+1
        return state
    ## this it look for machinge two tokens togather and if exists this matching swaich sthem with its idx
    def merge(self,ids,pair,idx):
        ids_sentence=[]
        for indces in ids:
            i=0
            sentece_tokne=[]
            while i < len(indces):
                if i< len(indces)-1 and indces[i]==pair[0] and indces[i+1]==pair[1]:
                    sentece_tokne.append(idx)
                    i+=2
                else:
                    sentece_tokne.append(indces[i])
                    i+=1

            ids_sentence.append(sentece_tokne)
        return ids_sentence
    ## this the same steps above but instead of doing it manlly i do this autmatucaly
    def tain_loop(self):
        for i in range(0,self.num_size):
            print(i)
            state=self.get_state(self.encode)
            if not state:
                break
            pair=max(state,key=state.get)
            idx=256+i
            self.encode=self.merge(self.encode,pair,idx)
            self.final_vocap[pair]=idx
    
        return self.final_vocap
    
    def decoder(self,ids:list=None):
        self.tain_loop()
        vocaplary={i:bytes([i]) for i in range(256)}
        for (p0,p1),idx in self.final_vocap.items():
            vocaplary[idx]=vocaplary[p0]+vocaplary[p1]
        decoding=b''.join(vocaplary[indces] for indces in ids )
        text=decoding.decode('utf-8')
        return text
    
    def encoder(self,text:str):
        ids_encoding=list(text.encode('utf-8'))
        while len(ids_encoding) >=2:
            state=self.get_state([ids_encoding])
            pair=min(state,key=lambda p: self.final_vocap.get(p,float('inf')))
            if  pair not in self.final_vocap:
                break
            idx=self.final_vocap[pair]
            ids_encoding=self.merge(ids_encoding,pair,idx)
        return ids_encoding



        

# import sys

gpt=GPTA('./text/output.txt',vocap_size=10)
gpt.tain_loop()
try:
    vocap=open('./gptA','wb')
    pickle.dump(vocap,vocap)
    vocap.close()
except:
    print('somtion wrong happend')







# text="""
# Ah, that makes perfect sense. If you are building a GPT-style tokenizer (which uses Byte-Pair Encoding, or BPE) from scratch, you should process the text sentence by sentence (or chunk by chunk), rather than loading the whole document as one giant string.
# """
# pattern_tokens=r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
# # sentence=regex.findall(pattern_tokens,text)

# with open('./text/test_test.txt','rb') as f:
#     file=f.read().decode('utf-8',errors='ignore')
#     sentence=regex.findall(pattern_tokens,file)
#     for i in sentence:
#         print(list(map(int,i.encode('utf-8'))))

#     split_file=file.splitlines()
# for i in split_file:
#     print(i.decode('utf-8',errors='replace'))
#     # sentence=regex.findall(pattern_tokens,i)