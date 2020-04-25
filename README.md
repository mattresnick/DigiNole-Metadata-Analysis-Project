# DigiNole-Metadata-Analysis-Project
Some code from my InternFSU project to fill in some gaps in the metadata records in FSU's DigiNole repository.

Almost all files have some overall description as well as a bit of line-by-line comments that I wrote either as I was doing the 
project or just as I was wrapping it up. Unfortunately I waited a while after the end of the internship to upload the code, so there were
some gaps in my memory of what does what. The main component that is not very specific to this project (and thus could be used with
minimal changes for an entirely different project) is the PDF to text portion. This relatively short bit of code is essentially a little
pipeline for doing OCR on PDFs that may otherwise give you trouble. Obviously there are programs out there that will do this exact thing
already, however a) this is free and b) it is designed to do the conversion in batches of PDFs rather than having to do them one at a time
like other free programs might.

I had wanted to do a lot more with this project, but as it stands now, the existing code basically just fished for the missing data 
in whatever was already in the metadata. What I really wanted was to set up a model to segment the PDFs to do more intelligent and
efficient OCR and find the metadata within the actual data. However, the project was only a total of 120 hours, which included
investigating the problem in the first place, and so I just couldn't get the ball rolling on that quick enough.

I'm satisfied with what I did get done though, as it's fairly efficient and works well.

\- Matt
