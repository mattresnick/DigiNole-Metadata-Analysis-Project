# DigiNole-Metadata-Analysis-Project
Some code from my InternFSU project to fill in some gaps in the metadata records in FSU's DigiNole repository.

Almost all files have some overall description as well as a bit of line-by-line comments that I wrote either as I was doing the 
project or just as I was wrapping it up. Unfortunately I waited so long since the end of the internship to upload the code that
now I don't remember enough to write up full instruction. I can say, though, that the only file that is not very specific to this
project (and thus could be used with minimal changes for an entirely different project) is the PDF to text file. This relatively
short bit of code is essentially a little pipeline for doing OCR on PDFs that may otherwise give you trouble. Obviously there are
programs out there that will do this exact thing already, however a) this is free and b) it is designed to do the conversion in 
batches of PDFs rather than having to do them one at a time like other free programs might.

I had wanted to do a lot more with this project, but as it stands now, the existing code basically just fished for the missing data 
in whatever was already in the metadata. What I really wanted was to set up a machine learning model to segment the PDFs to do
more intelligent and efficient OCR and find the metadata in the actual data. However, the internship was only a total of 120 hours, 
which included investigating the problem in the first place, and so I just couldn't get the ball rolling on that quick enough. 
Additionally, there wasn't a whole lot of metadata in the data to begin with, so that additional step would have been quite a bit
of work for very little return.  

Oh well, I'm satisfied with what I did get done, and while it's not all pretty and highly efficient,  it is still fairly efficient 
and above all it works well.

- Matt
