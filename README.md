# PDF Basic Editor

### Introduction:
Formally, this project is designed to provide a comprehensive solution for various PDF manipulation tasks. It consists of two main files: `project.py` and `test_project.py`. Currently it is able to perform 5 tasks, such as merging more than 1 PDFs, splitting a single PDF, adding a simple watermark to all pages of a PDF, encrypting a PDF with a password and decrypting these (and other) encrypted PDFs. 

### Project.py

- **project.py**: This file is the core of the project, featuring the `PdfEdit` and `PdfGui` classes. `PdfEdit` handles the backend logic for PDF operations like merging, splitting, adding watermarks, and encrypting/decrypting PDFs. `PdfGui` provides a user-friendly graphical interface using tkinter, making it easy for users to interact with the PDF editing functionalities.

__init__ function in PdfEdit required no specific initialization, which was left empty, merge in PDF edit takes in multiple arguments similarly to the other functions but it takes an additional overwrite_confirm, which allowed me to include in the conditionals based off the users reply (this function is implemented in PdfGui to split the GUI commands). In the code itself, I have made many comments for almost every line that might not be trivial to anyone new, and docstrings. Its worth mentioning that my function split has a helper function _split which handled the logic of how different inputs of page numbers are handled. 

Introduced canvas and letter when adding watermarks to bring this new idea even to myself of creating a temporary space (canvas) to write on and to save it and to re-calibrate its position after writing to the start which allows any saving or merging with the original pdf page. The other functions encrypt and decrypt takes care of simple processes from the PdfReader/PdfWriter from pypdf library. Following that, we have the PdfGui class and main function, which carries the GUI commands. I have added notes to my program regarding this part of the code for better understanding.

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

### The End (or the beginning of something beautiful)

Formally, the project demonstrates efficient use of various libraries to handle different aspects of PDF manipulation, offering a user-friendly tool for everyday PDF tasks. 

I am glad now I have this program, which can save me a lot of time and some money from online services to handle my PDFs. Time to time, when I come across needing different functionalities, I would upgrade this program to add additional functionalities. 

Feel free to explore the functionalities and provide feedback for further improvements. I am open to all kinds of criticism :D
