import requests
import time
import os

class PDFRequests:
    
    '''
    Provide a directory for writing pulled PDFs, a directory of XML records
    with PIDs in the titles, and a directory to write savepoints, and this
    will pull source PDFs for ETDs in the digital repository. Some records
    are associated with e-books, and while the pull will go through, the
    resulting PDFs will have 24kb of data and will be unreadable.
    
    The save process here is very crude, and there are many better ways to
    do it, but I only needed to run this process once and this seemed to be 
    the easiest to quickly write. Should be a breeze to change though.
    '''
    
    def __init__(self, write_directory, record_directory, save_directory):
        
        if not len(os.listdir(save_directory)):
            with open(save_directory + '0' + '.txt', "w") as handle:
                handle.write('')
        
        self.write_directory = write_directory
        self.record_directory = record_directory
        self.save_directory = save_directory
        
        self.savepoint = int(os.listdir(self.save_directory)[-1][:-4])
        self.records = os.listdir(self.record_directory)[self.savepoint:]
        
        self.requester()
    
    # Save progress on a pull.
    def save(self, num):
        savenum = "{:05n}".format(self.savepoint + num)
        with open(self.save_directory + savenum + '.txt', "w") as handle:
            handle.write('')
    
    # Cut PID from XML file names.
    def titleSlicer(self, name):
        name = name[name.index('_')+1:]
        return name[:name.index('_')]
    
    def requester(self):
        for num, file in enumerate(self.records):
            pid = self.titleSlicer(file)
            
            print ('Pulling PDF with PID:', pid)
            response = requests.get('http://fsu.digital.flvc.org/islandora/object/fsu%3A'+ pid +'/datastream/OBJ/download', stream=True)
            with open(self.write_directory + pid + ".pdf", "wb") as handle:
                handle.write(response.content)
            
            self.save(num+1)
            time.sleep(5)

'''
def main():
    main_dir = 'C:\\Users\\Owner\\Desktop\\Work\\'
    
    write_directory = main_dir + 'pdfs\\'
    record_directory = main_dir + 'Data-Metadata-Etc\\etds_processed\\'
    save_directory = main_dir + 'savepoints\\'
    
    PDFRequests(write_directory, record_directory, save_directory)
    
if __name__=='__main__':
    main()
'''