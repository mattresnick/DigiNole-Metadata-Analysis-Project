#PDF Directory--->(to image)--->(modify)--->Image Directory/Image Array--->(OCR)--->Text Directory

from pdf2image import convert_from_path
import os
from PIL import Image
from pytesseract import image_to_string

class PDFToText:
    
    '''
    Convert a directory of PDFs to images and convert images to text.
    
    ex:
        PDFToText('C:\\pdfs','C:\\images','C:\\text',5)
        <or>
        PDFToText('C:\\pdfs',None,'C:\\text',None)
    
    - Directories should end with '\\'.
    - If an entire document is desired, use None for num_pages.
    - If you wish to skip the creation of an image directory, use None
      for image_dir.
    '''
    
    def __init__(self, pdf_dir, image_dir, text_dir, num_pages):
        
        self.pdf_dir = pdf_dir
        self.text_dir = text_dir
        self.num_pages = num_pages
        
        if image_dir:
            self.image_dir = image_dir
        else:
            self.image_dir = []
        
        self.pdfsToImage()
        self.convertOCR()
    
    
    
    # Any image modifactions.
    # Currently scales up 10x using nearest neighbor sampling.
    def imageMods(self, im):
        shape = (im.width*10, im.height*10)
        return im.resize(shape,resample=Image.NEAREST)
    
    
    # Saves images with correct naming convention,
    # either in a directory or a list.
    def saveImage(self, im, group_array, pdf):
        
        name = pdf[:-4]+'_'+str(group_array[1])
        
        if isinstance(self.image_dir, str):
            im.save(self.image_dir+name+'.png')
        else:
            self.image_dir.append([name, im])
    
    
    def pdfsToImage(self):
        
        dir_len = len(os.listdir(self.pdf_dir))
        group_array = ['',0]
        
        for num, pdf in enumerate(os.listdir(self.pdf_dir)):
            
            # Print progress 20 evenly spaced times.
            if num%int(dir_len/20)==0:
                print ('Converting pdf #' + str(num) + 'to image.')
            
            # Convert to image (png).
            im = convert_from_path(pdf_path=self.pdf_dir+pdf,  
                              first_page=1, 
                              last_page=self.num_pages, 
                              fmt='png')
            
            # Image modifications.
            im = self.imageMods(Image.fromarray(im))
            
            # Images from the same pdf should be grouped together
            # in the format: 1234_0.png, 1234_1.png, etc.
            if pdf[:-4]==group_array[0]:
                group_array[1] += 1
            else:
                group_array = [pdf[:-4],0]
            
            # Save result.
            self.saveImage(im, group_array, pdf)
    
    
    def convertOCR(self):
        
        # This logical structure allows for text to be written from
        # either a directory of images or an array in memory.
        if isinstance(self.image_dir, str):
            
            dir_len = len(os.listdir(self.image_dir))
            for num, image in enumerate(os.listdir(self.image_dir)):
                
                if num%int(dir_len/20)==0:
                    print ('Converting image #' + str(num) + 'to text.')
                
                with open(self.text_dir+image[:-4]+'.txt','w') as file:
                    file.write(image_to_string(Image.open(self.image_dir+image)))
        else:
            
            dir_len = len(self.image_dir)
            for num, image in enumerate(self.image_dir):
               
                if num%int(dir_len/20)==0:
                    print ('Converting image #' + str(num) + 'to text.')
               
                with open(self.text_dir+image[0]+'.txt','w') as file:
                    file.write(image_to_string(image[1]))
         
