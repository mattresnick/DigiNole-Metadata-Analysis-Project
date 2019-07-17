'''
This script specifically looks in the namePart XML element and a file containing
previously retrieved text from the note element for phraes that may be department names.
It then will check how many are overlapping and create a combined list (without overlaps).

It'll take some text, find a start phrase and cut the text down there. Then it will continue
to look for a terminating phrase and cut it again there. It'll then add that to an array, paired
with the file name, then move on to the next given text.



In general, though, this can be used to find virtually any phrase in any xml element,
however it does have some limitations:
    
    For one thing, the phrase will need to be fairly uniform or contain some uniform set of 
    words, as there is no statistical processing or machine learning going on here. We are 
    simply checking for starting phrases and terminating phrases and getting the string in 
    between (and including the start phrase usually).
    
    Additionally, the phrase search will not be optimal for many purposes because if a phrase
    that is used is inside of another word then it will still return true (i.e. if you search
    for the phrase "in" it would return true for the word "finance" which may or may not be
    what you want... in my case I needed it for the terminating phrase because of typos). 
    This can be changed pretty easily using regular experessions, but beware of typo issues if 
    you do this.
    
    There were a few records in my case that should have been in the right format but were not
    identified as such by the script. This is likely because of the encoding of the characters or
    something strange like that. There appeared to only be 5 of these in my case (error_exceptions) 
    so I didn't investigate further and just added them manually in the interest of time. You may 
    want to check this out yourself just in case it is a more pervasive issue in other areas.
    

You will need to change a bit of the structure to get the code to do what you want. If you have
the element text retrieved already, use the note search section only, otherwise use the namepart 
search section. Obviously any comparison code will also need to be removed/modified.
'''



import os
from xml.etree import ElementTree as ET
import numpy as np
from Custom_Text_IO import writeFileLines

'''global variable declarations'''
start_phrases = ['Department','department','School','College','Dept.','dept.', 'Dept','dept', 
                    'Dep.', 'dep.','Submitted','submitted']

terminating_phrases = ['in ','In ','in\n','In\n']


error_exceptions = [['fsu_180310_MODS.xml','Department of Psychology'], 
                        ['fsu_180368_MODS.xml','Department of Electrical and Computer Engineering'],
                        ['fsu_180369_MODS.xml','Department of Marketing'],
                        ['fsu_180498_MODS.xml','Department of Middle and Secondary Education'],
                        ['fsu_180551_MODS.xml','Department of Educational and Learning Systems']]

error_additions = []


#This loads in a very specifically formatted text file.
def fileLoader(file):
    
    f = open(file, 'r', encoding="utf-8")
    
    data = f.read()
    
    all_lines = data.split('|||')
    
    retainer = []
    for line in all_lines:
        values = line.split('+++')
        retainer.append(values)
    
    f.close()
    
    del retainer[-1]
    
    return retainer





def slicer(sliced, filename):
    
    errorflag=False
        
    #check for a number of common ways to end the department name
    for s in terminating_phrases:
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
    if errorflag==False and sliced not in np.array(error_exceptions)[:,0]:
        error_additions.append([filename, sliced])
    
    return sliced, False



def phraseSearch(note, filename):
    for phrase in start_phrases:
        if phrase in note:
            
            #special case where starting point of phrase won't be in the resulting string
            if phrase=='Submitted' or phrase=='submitted':
                loc = note.index(phrase) + 17
            else:
                loc = note.index(phrase)
            
            #cut note up to the start point
            sliced = note[loc:]
            
            #try to slice again at an end point
            sliced, check = slicer(sliced, filename)
            
            #terminate search in either case
            #either there was an end point or there wasn't, but the department was found
            if check:
                return sliced, 0
            else:
                return sliced, 1
            
    #if the search was never terminated then no phrase could be located in the note
    return note, 2



def main():
    
    '''                     Pull department names from namePart element                     '''
    '''-------------------------------------------------------------------------------------'''
    
    targetdir = 'C:\\Users\\Owner\\Desktop\\Work\\Data-Metadata-Etc\\etds_processed\\'
    files = os.listdir(targetdir)
    
    dept_ret_namepart = []
    
    count = 1
    for file in files:
        
        if count%1000==0:
            print ('namePart analysis iteration #' + str(count))
        
        count += 1
        
        if file.endswith('.xml'):
            #try:
            mods = ET.parse(targetdir + "/" + file)
            namespaces = {'mods': 'http://www.loc.gov/mods/v3'}
            ET.register_namespace('', "http://www.loc.gov/mods/v3")
            ET.register_namespace('dcterms', "http://purl.org/dc/terms/")
            ET.register_namespace('etd', "http://www.ndltd.org/standards/metadata/etdms/1.0/")
            ET.register_namespace('flvc', "info:flvc/manifest/v1")
            ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
            root = mods.getroot()
      
            #Attempt to get text values of nameparts for particular record
            namepart_retainer = []
            rolecheck = ''
            for name in root.findall('mods:name', namespaces):
                try:
                    for namepart in name.findall('mods:namePart', namespaces):
                        namepart_retainer.append(namepart.text)
                except Exception as e:
                    print ('Namepart retieval error:', e)
                
                try:
                    for role in name.findall('mods:role', namespaces):
                        for roleterm in role.findall('mods:roleTerm', namespaces):
                            if roleterm.text=='degree granting department':
                                for namepart in name.findall('mods:namePart', namespaces):
                                    rolecheck = namepart.text
                except Exception as e:
                    pass
            
            
            
            dept_retainer = []
            if  len(namepart_retainer)>0: 
                for part in namepart_retainer: 
                    #add the namepart text if any phrase except the last two are found
                    if part is not None:
                        if any(x in part for x in start_phrases[:-2]):
                            dept_retainer.append(part)
            
            if len(dept_retainer)==1:
                dept_ret_namepart.append([file, dept_retainer[0]])
            #very few cases have 2 parts but its always the second one when it does happen
            elif len(dept_retainer)==2:
                dept_ret_namepart.append([file, dept_retainer[1]])
            elif len(rolecheck)>0:
                dept_ret_namepart.append([file, rolecheck])       
            #except Exception as e:
             #   print ('Error:', e)
    '''-------------------------------------------------------------------------------------'''
    
    
    
    
    
    
    
    '''                         Pull department names from note element                              '''
    '''----------------------------------------------------------------------------------------------'''
    #Retains department names from note
    dep_ret_note = []
    
    #Retains malformed department names, i.e. there isn't a uniform terminating string
    part_dep_ret_note = []
    
    #Whatever isn't added to the other two retainers
    leftovers = []
    
    
    note_data = fileLoader('C:\\Users\\Owner\\Desktop\\Work\\workspace\\all_xml_data.txt')
    
    
    
    for notenum in range(len(np.array(note_data)[:,1])):
        
        if notenum%1000==0:
            print ('Note analysis iteration #' + str(notenum))
        
        filename = note_data[notenum][0]
        note = note_data[notenum][1]
        
        sliced, option = phraseSearch(note, filename)
        
        if "council" not in sliced:
            if option==0:
                dep_ret_note.append([filename,sliced])
            elif option==1:
                part_dep_ret_note.append([filename,sliced])
            else:
                leftovers.append([filename,sliced])
        else:
            leftovers.append([filename,sliced])
    
    #a few problem records are added manually here
    for exc in error_exceptions:
        dep_ret_note.append(exc)
    '''----------------------------------------------------------------------------------------------'''
    
    
    main_ret_note = dep_ret_note + part_dep_ret_note
    mrn_filenames = np.array(main_ret_note)[:,0]
    
    
    combined_ret = []
    counter = [0,0]
    for dname in dept_ret_namepart:
        counter[0] = counter[0]+1
        print ('Combiner iteration #' + str(counter[0]) + '/' + str(len(dept_ret_namepart)))
        
        #check whether each department retrieved from namepart has already been retrieved in note
        if dname[0] not in mrn_filenames:
            combined_ret.append(dname)
            counter[1] = counter[1] + 1
    
    combined_ret = combined_ret + main_ret_note
    
    
    print ('Number of departments found in namePart and not in note:', str(counter[1]))
    print ('Total number of department names retrieved:', len(combined_ret))
    
    
    combined_files = np.array(combined_ret)[:,0]
    everything_else = [f for f in files if f not in combined_files]
    print (len(everything_else))
    
    #writeFileLines('C:\\Users\\Owner\\Desktop\\Work\\workspace\\', 'no_department_files.txt', everything_else)
    
    return leftovers, dept_ret_namepart
    
    
if __name__=='__main__':
    leftovers, drn = main()
