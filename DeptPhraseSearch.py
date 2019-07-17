import os
import numpy as np


class DeptPhraseSearch:
    
    def __init__(self):
        self.start_phrases = ['Department','department','School','College','Dept.','dept.', 'Dept','dept', 
                         'Dep.', 'dep.','Submitted','submitted']
        
        self.terminating_phrases = ['in ','In ','in\n','In\n']
        
        
        self.error_exceptions = [['fsu_180310_MODS.xml','Department of Psychology'], 
                                ['fsu_180368_MODS.xml','Department of Electrical and Computer Engineering'],
                                ['fsu_180369_MODS.xml','Department of Marketing'],
                                ['fsu_180498_MODS.xml','Department of Middle and Secondary Education'],
                                ['fsu_180551_MODS.xml','Department of Educational and Learning Systems']]
        
        self.error_additions = []
        
    
    def slicer(self, sliced, filename):
        
        errorflag=False
            
        #check for a number of common ways to end the department name
        for s in self.terminating_phrases:
            if s in sliced and len(sliced[:sliced.index(s)])>0:
                errorflag=True
                
                #Cut the new note from the beginning up to the location of one of the name enders
                loc = sliced.index(s)
                sliced = sliced[:loc]
                
                #Sometimes there's a space, sometimes not. But if there is it should be removed.
                if sliced[-1]==' ':
                    sliced = sliced[:-1]
                
                return sliced, True
        
        #I know there are a few problem records, I'm ignoring them here and I add them explicitly later
        if errorflag==False and sliced not in np.array(self.error_exceptions)[:,0]:
            self.error_additions.append([filename, sliced])
        
        return sliced, False
    
    
    
    def phraseSearch(self, text, filename):
        for phrase in self.start_phrases:
            if phrase in text:
                
                #special case where starting point of phrase won't be in the resulting string
                if phrase=='Submitted' or phrase=='submitted':
                    loc = text.index(phrase) + 17
                else:
                    loc = text.index(phrase)
                
                #cut note up to the start point
                sliced = text[loc:]
                
                #try to slice again at an end point
                sliced, check = self.slicer(sliced, filename)
                
                #terminate search in either case
                #either there was an end point or there wasn't, but the department was found
                if check:
                    return sliced, 0
                else:
                    return sliced, 1
                
        #if the search was never terminated then no phrase could be located in the note
        return text, 2



def main():
    #Retains department names from note
    dept_ret = []
    
    #Retains malformed department names, i.e. there isn't a uniform terminating string
    part_dep_ret = []
    
    #Whatever isn't added to the other two retainers
    leftovers = []
    
    search = DeptPhraseSearch()
    
    
    text_directory = 'C:\\text_files\\'
    files = os.listdir(text_directory)
    
    
    
    for num, file in enumerate(files):
        
        if num%1000==0:
            print ('Note analysis iteration #' + str(num))
        
        with open(text_directory+file, 'r', encoding="utf-8") as f:
            text = f.read()
        filename = file[:-4]
        
        sliced, option = search.phraseSearch(text, filename)
        
        if "council" not in sliced:
            if option==0:
                dept_ret.append([filename,sliced])
            elif option==1:
                part_dep_ret.append([filename,sliced])
            else:
                leftovers.append([filename,sliced])
        else:
            leftovers.append([filename,sliced])
    
    #a few problem records are added manually here
    for exc in search.error_exceptions:
        dept_ret.append(exc)



if __name__=='__main__':
    main()