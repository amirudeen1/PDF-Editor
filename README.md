# PDF Basic Editor

### Introduction:
Formally, this project is designed to provide a comprehensive solution for various PDF manipulation tasks. It consists of two main files: `project.py` and `test_project.py`. Currently it is able to perform 5 tasks, such as merging more than 1 PDFs, splitting a single PDF, adding a simple watermark to all pages of a PDF, encrypting a PDF with a password and decrypting these (and other) encrypted PDFs. 

I am at the end of completing my CS50P project which is python programming, an online course taught by David Malan from Harvard. Shoutout to him! As a year 1 physics major, I was introduced to data analytics and processing with Python, and back then, 4 years ago, I completely hated it. Now, all due to his efforts to engage the class, inspire, motivate and show us the mind-blowing things programming can do, here I am 4 years later, totally in love with coding languages and the idea of programming. Anyways, the final task of this course, was to create a project of my own, and that's when I thought to myself, why not kill 2 birds with 1 stone and build something that will allow me to both pass this course, and have something built for me to automate a task or make my life (and even other lives) easier. It took me a really long time to brainstorm one good idea that I should work on, as I had a few ideas.

Ultimately, I recalled how I would always be so annoyed whenever I had to manipulate PDFs files, such as for the functions built in my very own program here, I would go to online websites such as ilovepdf/smallpdf and etc., and always end up finding myself having the need to pay some real money or sign up for a paid membership to access all of its tool, and to not be limited by only being able to merge 2 pdfs and not anymore than that and etc. You get the idea, so, maybe instead of ever having to do that, I thought that it would be so cool to program my own PDF Editor. It was a painful journey, but one that I needed to be a better programmer myself, as I learned a lot at almost every line of code, on top of already having gone through every CS50P (which was much needed for this program for all the basics that helped me understand the less basic portions).

I had this idea to manipulate pdfs, but I started with the wrong function, which was to optimize pdfs. I did not actually know before how large PDF files were compressed and optimized, and then I learned through research that to compress and PDF files, usually, images from these pdfs would be downsized or made of a lower quality and so on. As I was starting my project from scratch, I was already very unsure of libraries like tkinter which enabled visual GUI dialogs for user, reportlab which helped generate pdfs from scratch, io and pypdf and etc, which took me many hours of researching and learning and understanding how to write this program, and then starting off with optimization was indeed the worst decision I could have made. Many many hours later, i decided to scrap that idea off, and leave it for next time as a smaller project on my own to implement this function, and continued with implementing merging, which took me a way shorter time as I did not have to play around with images in PDFs but just manipulate the PDFs with simple logic. Similarly, all of the other 5 functions require basic logic around which took me shorter time to make each one after the other after building the first few such as merging and splitting.

Finally, although I completed this program maybe a few hours ago, and it was fully functional from a user POV(not having it tested with pytest yet), I realized when I wanted to run a test for my functions and parts of this program, I ran into this problem of having to create mocktest for mock user usage of my program and etc., which was far too confusing and time consuming (although possible for sure), I decided to refactor my main project. The problem was my GUI related commands was mixed in between the class which handled the backend logic for the operations, so I had to refactor, split these GUI commands into another class and let my first class only handle the backend operations, which then allowed me to test the functions and part of this class very very easily. Although, as seen in my test_project.py file, I did not fully test every corner case, as it was too late into the night and i wanted to get some sleep, BUT, i did most reasonable tests to ensure output files exist, and if merged, output pdf pages is logical and if split, similar logic and so on. 

FYI: Almost every single library used was not mentioned or taught directly in CS50P, so, yeap, had to research and learn myself how to implement these libraries. Only because I wanted something user-friendly. If I implemented a CLI version istead of a GUI version, it would have required less time spent on researching, but still, I prefer the GUI version in the end as for a user of my own program like myself, it will be easier to just click on buttons and let the program handle everything for me instead of typing manually in to a CLI. 

The rest of this README.md should be less long-winded and straight to the point.

### Project.py

- **project.py**: This file is the core of the project, featuring the `PdfEdit` and `PdfGui` classes. `PdfEdit` handles the backend logic for PDF operations like merging, splitting, adding watermarks, and encrypting/decrypting PDFs. `PdfGui` provides a user-friendly graphical interface using tkinter, making it easy for users to interact with the PDF editing functionalities.

__init__ function in PdfEdit required no specific initialization, which was left empty, merge in PDF edit takes in multiple arguments similarly to the other functions but it takes an additional overwrite_confirm, which allowed me to include in the conditionals based off the users reply (this function is implemented in PdfGui to split the GUI commands). In the code itself, I have made many comments for almost every line that might not be trivial to anyone new, and docstrings. Its worth mentioning that my function split has a helper function _split which handled the logic of how different inputs of page numbers are handled. 

Introduced canvas and letter when adding watermarks to bring this new idea even to myself of creating a temporary space (canvas) to write on and to save it and to re-calibrate its position after writing to the start which allows any saving or merging with the original pdf page. The other functions encrypt and decrypt takes care of simple processes from the PdfReader/PdfWriter from pypdf library.

The development process involved significant design choices. Initially, the GUI commands using tkinter were embedded within the `PdfEdit` class. However, this approach led to complexity, especially in unit testing. To address this, the code was refactored to separate the GUI logic from the core PDF processing logic. This separation not only simplified the testing process but also enhanced the modularity and readability of the code.

### Test_Project.py

- **test_project.py**: This file contains unit tests for the `PdfEdit` class, ensuring the reliability and robustness of the PDF operations. It uses the pytest framework for testing various functionalities like merging, splitting, watermarking, and encryption/decryption of PDFs.

Something new for me was setting up and tearing down test pdf files, as this program is working with real-time pdf files to perform such functions. We set up a fixture at the start with a scope of function which enables us to re-use this function of setting up and tearing down of test files for each of the functions to be tested such as merge and etc. 

For watermark and encryption/decryption, ontop of the first test which checks for the existence of an output file, I had very little knowledge on how these files could actually be tested without much complexities, but after some research, I realized I could use the comparision of the contents using read-binary mode, and using .read() on the original and output file for these 3 cases, I was able to test if the output file is simply not the same original file, and a modification is done which could be watermarking, encryption or decryption. 

### Pytest.ini

Upon testing, I had successful green passes for all 4 functions, but ran into dependencies issues hence 2 warnings were issued in yellow. The first warning was solved by implementing the importation of pypdf instead of PyPDF2 (initially used). 

The 2nd warning, was written off in pytest.ini for my pytest to ignore this warning, as it has no effect on my actual program's function, but since this warning was raised, it is worth mentioning that this program might be faulty/buggy if the library of reportlab was not maintained or affected. The warning for reportlab is a deprecated warning.

### README.md

This file, which contains everything you should know about my program, and my experience writing it as my first project!

### Requirements.txt

Contains the list of pip-installable libraries that I used and an additional pycryptodome which was needed to run my program. 

### YouTube Video

As a requirement of CS50P's final project submission, a less than 3 minute video is required to talk about this project and display it to others. The link is at the top of this README.md.

### The End (or the beginning of something beautiful)

Formally, the project demonstrates efficient use of various libraries to handle different aspects of PDF manipulation, offering a user-friendly tool for everyday PDF tasks. 

I am glad now I have this program, which can save me a lot of time and some money from online services to handle my PDFs. Time to time, when I come across needing different functionalities, I would upgrade this program to add additional functionalities. 

Feel free to explore the functionalities and provide feedback for further improvements. I am open to all kinds of criticism :D
