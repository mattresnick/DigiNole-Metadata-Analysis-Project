'''
This file has three main functions:
    
    1) Returns an array containing the name and value(s) for every element and
    subelement for every xml record in a given directory.
    
    2) Returns and exports an array of boolean arrays indicating which 
    elements/subelements have values and which don't for every record.
    
    3) Determines the number of unique values (and what those values are)
    for each element/subelement in all of the records


Structure of fullset:

Outer array holding        
all records --> [

record 1 -->        [[element1, value],
                     [element2, value],
                     [element3 - subelement1, value],
                     [element3 - subelement2, value],
                     [element4 - subelement1, [value1, value 2,...]],
                     ...
                    ], <--close record 1
        
record 2 -->        [
                        ...
                    ],  <-- close record 2
                ...      
                ] <-- close outer array
        

        

        
Structure of boolset:
    
    [[0,0,1,0,1,...,0,1],
     [0,1,1,1,0,...,1,0],
     ...
    ]
    

Structure of uniquevals:
    
    [[element1_val1, element1_val2,...],
     [element2_val1, element2_val2,...],
    ...
    ]
    
    So that len(row1) = number of unique values for element 1.
'''

import os
import pymods
import numpy as np
import matplotlib.pyplot as plt
from operator import attrgetter



class ElementSearchAnalysis:
    
    def __init__(self):
        pass


    # Function will run functions given to it and retain values it finds
    # and will check subelements if there are any.
    def recordRunner(self, record, func, subelementset=[]):
        
        retainer = []
        
        # Each function is given as a string, attrgetter will run them from that.
        # "tempelement" is the result of running said function for "record".
        f = attrgetter(func)
        tempelement = f(record)
        
        
        # If there is no value for a particular element we want to know that,
        # and we also want to show that each subelement is not there either:
        if tempelement is None or len(tempelement)==0:
            
            if len(subelementset)==0:
                retainer.append([func, None])
            else:
                for num_none in range(len(subelementset)):
                    retainer.append([func + ' - '+ subelementset[num_none], None])
        
        # One (rather important) case has no subelements, this is handled here:
        elif len(subelementset)==0:
           retainer.append([func, tempelement])
        
        
        
        # Many cases will have subelements, and each needs to be run individually,
        # BUT for multiple values of the same subelement they should all be in just 
        # one entry. I want to know that they have values, but I don't necessarily
        # need to know how many values there are for each one.
        else:
            
            # So here each subelement function is run and the values retained.
            # There can be multiple values for one subelement (like a few sets
            # of people would have multiple name values) so this is the reason for
            # the nested structure here.
            partret = []
            for part in tempelement:
                row = []
                for subfunc in subelementset:
                    g = attrgetter(subfunc)
                    #sometimes if a subelement isn't there an error will be raised
                    try:
                        row.append([func + ' - ' + subfunc, g(part)])
                    except:
                        row.append([func + ' - ' + subfunc, None])
                partret.append(row)
            
            # Here the values can be separated into the right structure to be returned.
            # This means: [Element - Subelement, value] or
            # in the case of multiple values: [Element - Subelement, [value1, value2, ...]] 
            for col in range(len(partret[0])):
                valret = []
                for row in range(len(partret)):
                    valret.append(partret[row][col][1])
                
                # If there's just one value we don't need it to be in an array.
                if len(valret)==1:
                    retainer.append([partret[0][col][0],valret[0]])
                else:
                    retainer.append([partret[0][col][0],valret])
        
        return retainer



    # This function has logic to meticulously check if an 
    # element really has a value or not.
    def valChecker(self, val):
    
        # The easiest case is a single existing value.
        if val is not None and not isinstance(val, (list,)):
            return True
        
        # Sometimes there could be multiple values, so it'll be a list.
        elif val is not None and isinstance(val, (list,)):
            
            # Only one value needs to be there, if the last val is reached without 
            # returning true, there are no values.
            for v in val:
                if v is not None:
                    return True
                if val.index(v)==len(val)-1:
                    return False
       
        # Otherwise it isn't a list and there's no single value either.
        else:
            return False
            


    def keyFunc(val):
        return val[0]


    def plotter(self, pairs, option):
        
        pairs.sort(key=self.keyFunc)
        pairs = np.array(pairs)
        
        x = pairs[:,0]
        y = pairs[:,1]
        
        fig, ax = plt.subplots()
        
        ax.scatter(x, y)
        
        ax.set(xlabel='File number', ylabel='Number of existing elements.',
               title=option)
        
        plt.show()


    def titleSlicer(name):
        name = name[name.index('_')+1:]
        return int(name[:name.index('_')])











class ElementSearchHandler:
    
    def __init__(self, maindir):
        
        self.maindir = maindir
        self.opendir = os.listdir(maindir)
        self.num_records=len(self.opendir)
        
        self.mods_records=[]
        
        
        self.fullset = []# Will retain all element values of ALL records in the given directory.
        
        self.uniquevals = [[] for r in range(41)]
        self.boolset = []
        
        
        '''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MODS Vars~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        
        self.element_types = []
        self.element_types.append(["digital_origin", "extent", "form", "identifiers", 
                              "iid", "internet_media_type", "issuance", 
                              "physical_description_note", "physical_location", 
                              "pid", "publisher", "purl", "titles", "type_of_resource"]) #no sub-elements
        self.element_types.append(["abstract", "note"]) #text, type, displayLabel
        self.element_types.append(["collection"]) #title
        self.element_types.append(["dates", "publication_place"]) #text, type
        self.element_types.append(["genre"]) #uri, authority, authorityURI
        self.element_types.append(["language"]) #text, code, authority
        self.element_types.append(["names", "subjects"]) #text, uri, authority, authorityURI
        self.element_types.append(["rights"]) #text, type
        
        
        self.subelement_types = []
        self.subelement_types.append([])
        self.subelement_types.append(['text','type','displayLabel'])
        self.subelement_types.append(['title'])
        self.subelement_types.append(['text','type'])
        self.subelement_types.append(['uri','authority','authorityURI'])
        self.subelement_types.append(['text','code','authority'])
        self.subelement_types.append(['text','uri','authority','authorityURI'])
        self.subelement_types.append(['text','type'])
        
        #Currently 41 individual elements/subelements.
        self.all_elements = ["digital_origin", "extent", "form", "identifiers", 
                        "iid", "internet_media_type", "issuance", 
                        "physical_description_note", "physical_location", "pid", 
                        "publisher", "purl", "titles", "type_of_resource",
                        "abstract:text", "abstract:type", "abstract:displayLabel", 
                        "note:text", "note:type", "note:displayLabel", "collection:title", 
                        "dates:text", "dates:type", "publication_place:text", 
                        "publication_place:type","genre:uri", "genre:authority", 
                        "genre:authorityURI", "language:text", "language:code", 
                        "language:authority", "names:text", "names:uri", "names:authority", 
                        "names:authorityURI", "subjects:text", "subjects:uri", "subjects:authority", 
                        "subjects:authorityURI", "rights:text", "rights:type"]
        '''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        

    def getRecords(self):
        print ('Initiating file retrieval...')
        
        for filenum in range(self.num_records):
            if filenum%1000==0:
                print ('Retrieving record '+str(filenum)+'/'+str(self.num_records))
            
            self.mods_records.append(pymods.MODSReader(self.maindir + self.opendir[filenum]))
    
    # Splits element values out of the XML records and optionally exports the data
    # to a .npy file.
    def parseRecords(self, filedir=None):
        print ('Initiating parsing...')
        
        for mr in range(self.num_records):
        
            if mr%1000==0:
                print ('Parsing record '+str(mr)+'/'+str(self.num_records))
            
            for record in self.mods_records[mr]:
                recordset = []# Will retain the elements of a single record.
                
                #Iterate through the different sets of elements.
                for num in range(len(self.element_types)):
                    
                    #Iterate through each element of each type.
                    for func in self.element_types[num]:
                        ESA = ElementSearchAnalysis()
                        retainer = ESA.recordRunner(record=record, 
                                                    func=func, 
                                                    subelementset=self.subelement_types[num])
                        
                        #Add each value individually.
                        for val in retainer:
                            recordset.append(val)
                
                self.fullset.append(recordset)
        
        if filedir:
            np.save(filedir, self.fullset)
        
        
    # Checks for and counts unique elements values.
    def uniqueValAnalysis(self, filedir=None):
        for recordrep in self.fullset:
        
            if self.fullset.index(recordrep)%1000==0:
                print ('Analysis iteration',str(self.fullset.index(recordrep))+'/'+str(len(self.fullset)))
            
            # Populate a boolean array, 1's represent an element's existence in a given record.
            ESA = ElementSearchAnalysis()
            recordrow = [1 if ESA.valChecker(i) else 0 for i in np.array(recordrep)[:,1]]
            self.boolset.append(recordrow)
            
            # Check to see if element values are in the existing list for the particular element.
            for n in range(41):
                elementval = recordrep[n][1]
                if elementval is not None and elementval not in self.uniquevals[n]:
                    self.uniquevals[n].append(elementval)
        
        
        # Print a count summary.
        print ('')
        print ('')
        for x in range(41):
            print (self.all_elements[x],'-',sum(np.array(self.boolset)[:,x]))
            print ('Unique values:', len(self.uniquevals[x]))
            
            if len(self.uniquevals[x])<10:
                print (self.uniquevals[x])
            
            print('')
            print('')
        
        if filedir:
            np.save(filedir, np.array(self.boolset))
    
    # Saves note text and file name to specially delimited text files.    
    def saveNote(self, filedir):
        with open(filedir,'w', encoding="utf-8") as file:
            for recordnum in range(len(self.fullset)):
                
                fullnote = self.fullset[recordnum][17][1]
                
                #make sure there's a record/note text here
                if self.opendir[recordnum] is not None and fullnote is not None:
                    
                    #if there's one note it can be added trivially
                    if isinstance(fullnote, str):
                        rstr = str(self.opendir[recordnum]) + '+++' + str(fullnote)
                        
                    #if not, the note text parts all need to be added separately
                    else: 
                        rstr = str(self.opendir[recordnum]) + '+++' + fullnote[0]
                        for notenum in range(1,len(fullnote)):
                            rstr = rstr + '/' + str(fullnote[notenum])
                    
                    # ||| is the record delimiter, +++ is the element delimiter.
                    if len(rstr)>0:    
                        try:
                            file.write(rstr+'|||')
                        except Exception as error:
                            print (error)

def main():
    
    record_directory = 'C:\\Users\\Owner\\Desktop\\Work\\Data-Metadata-Etc\\etds_processed\\'
    
    handler = ElementSearchHandler(record_directory)
    handler.getRecords()
    handler.parseRecords()
    handler.uniqueValAnalysis()
    
    #'C:\\Users\\Owner\\Desktop\\Work\\workspace\\full_element_data.npy'
    #'C:\\Users\\Owner\\Desktop\\Work\\workspace\\boolset.npy'
    #'C:\\Users\\Owner\\Desktop\\Work\\workspace\\all_xml_data.txt'
    


if __name__=='__main__':
    main()
