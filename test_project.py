from pypdf import PdfReader
import os
from reportlab.pdfgen import canvas
import pytest
from project import PdfEdit

### Yet to test corner cases due to complexity of setting up test cases. 
### Did minimal but sufficient testing, including checking of existence of resulting file, and basic features
### Such as number of pages of resulting file, or the contents of the resulting file in bytes.

# Test Setup for creating and cleaning up test PDF files. Used by multiple tests.
# Decorator to definte a fixture for setting up and tearing down test PDF files
# Used by multiple tests, re-usable by multiple tests
# Function scope = "function" ensures that the fixture is only created once per test function when explicitly requested
# In the grand scheme of things, this fixture allows us to not duplicate and lengthen the code
@pytest.fixture(scope="function") 
def pdf_setupteardown():
    """
    Fixture for setting up and tearing down test PDF files.

    This fixture creates two test PDF files, yields their file paths as a tuple,
    and deletes the test files after the tests are done.
    """
    # Setup test PDF files
    test_file1 = "test1.pdf"
    test_file2 = "test2.pdf"
    create_test_pdf(test_file1) # To be defined down after this function
    create_test_pdf(test_file2)

    yield test_file1, test_file2 # As a tuple

    # Cleanup test PDF files
    os.remove(test_file1)
    os.remove(test_file2)

def create_test_pdf(filename):
    """
    Creates a simple test PDF file with the given filename.

    :param filename: The name of the file to create.
    """
    c = canvas.Canvas(filename) # Create new PDF using ReportLab library 
    # Add some text to the PDF file
    c.drawString(100, 750, "Hello, World!") 
    # Save the PDF file
    c.save()

# Test for Merging
def test_merge(pdf_setupteardown): 
    """
    Test merging two PDF files and checks for existence and page count.

    This test case merges two test PDF files and checks whether the merged PDF file exists
    and whether its page count matches the sum of pages from the original PDFs.
    """
    test_file1, test_file2 = pdf_setupteardown
    pdf_edit = PdfEdit()

    output_file = "merged.pdf"
    pdf_edit.merge([test_file1, test_file2], output_file, overwrite_confirm=True)

    assert os.path.exists(output_file), "Merged file doesn't exist" # Error message displayed if fail
    
    merged_reader = PdfReader(output_file)
    original_reader1 = PdfReader(test_file1)
    original_reader2 = PdfReader(test_file2)
    total_original_pages = len(original_reader1.pages) + len(original_reader2.pages)
    assert len(merged_reader.pages) == total_original_pages, "Pages in merged PDF don't match original PDFs"

    os.remove(output_file)

# Test for Splitting
def test_split(pdf_setupteardown):
    """
    Test splitting a PDF file and checks for existence and page count.

    This test case splits a test PDF file and checks whether the split PDF file exists
    and whether its page count matches the expected number.
    """
    test_file, _ = pdf_setupteardown # _ is a placeholder to ignore second argument in tuple
    pdf_edit = PdfEdit()

    output_file = "split.pdf"
    pdf_edit.split(test_file, "1", output_file) # extract page 1

    assert os.path.exists(output_file), "Split file doesn't exist"

    # Check total page count in split file
    split_reader = PdfReader(output_file)
    expected_page_count = 1 # As above we split 1 page, can be adjusted whenever testing
    assert len(split_reader.pages) == expected_page_count, "Pages in split PDF don't match expected"

    os.remove(output_file)

# Test for Watermark Addition
def test_add_watermark(pdf_setupteardown):
    """
    Test adding a watermark to a PDF file and checks for existence and content difference.

    This test case adds a watermark to a test PDF file and checks whether the watermarked
    PDF file exists and whether its content differs from the original PDF file.
    """
    test_file, _ = pdf_setupteardown
    pdf_edit = PdfEdit()

    output_file = "watermarked_test.pdf"
    pdf_edit.add_watermark(test_file, "Test Watermark", output_file)

    assert os.path.exists(output_file), "Watermarked file doesn't exist"
    
    # Compare contents of original and watermarked file
    # Opening both original and watermarked file in read-binary mode
    with open(test_file, "rb") as file1, open(output_file, "rb") as file2:
        original_content = file1.read()
        watermarked_content = file2.read()

    assert original_content != watermarked_content, "Watermark not added"

    os.remove(output_file)
    
# Test for PDF Encryption and Decryption
def test_encrypt_decrypt(pdf_setupteardown):
    """
    Test PDF encryption and decryption and checks for existence and content difference.

    This test case encrypts and then decrypts a test PDF file, checking whether the encrypted
    and decrypted files exist and whether their content differs from the original PDF file.
    """
    test_file, _ = pdf_setupteardown
    pdf_edit = PdfEdit()

    encrypted_file = "encrypted_test.pdf"
    decrypted_file = "decrypted_test.pdf"

    # Encrypt
    pdf_edit.encrypt_pdf(test_file, "password", encrypted_file)
    assert os.path.exists(encrypted_file), "Encrypted file doesn't exist"
    # Opening both original and encrypted file in read-binary mode
    with open(test_file, "rb") as file1, open(encrypted_file, "rb") as file2:
        assert file1.read() != file2.read(), "PDF not encrypted"

    # Decrypt
    pdf_edit.decrypt_pdf(encrypted_file, "password", decrypted_file)
    assert os.path.exists(decrypted_file), "Decrypted file doesn't exist"
    # Opening both original and decrypted file in read-binary mode
    with open(test_file, "rb") as file1, open(decrypted_file, "rb") as file2:
        assert file1.read() != file2.read(), "File not decrypted"

    os.remove(encrypted_file)
    os.remove(decrypted_file)
