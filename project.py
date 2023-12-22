from pypdf import PdfReader, PdfWriter
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

class PdfEdit:
    """
    Handles PDF operations such as merging, splitting, watermarking, and encrypting/decrypting PDF files.
    """
    def __init__(self):
        """
        Initializes the PdfEdit class. Currently, there's no specific initialization needed.
        """
        pass
        
    def merge(self, file_paths, output_path, overwrite_confirm):
        """
        Merges multiple PDF files into a single PDF file.

        This method combines the contents of multiple PDF files specified in 'file_paths'
        into a single PDF file saved at 'output_path'. If the output file already exists,
        it prompts the user for confirmation before overwriting, depending on the
        'overwrite_confirm' parameter.

        :param file_paths: A list of file paths for the PDFs to be merged.
        :param output_path: The file path where the merged PDF will be saved.
        :param overwrite_confirm: A callback function to confirm file overwrite.
        :raises ValueError: If less than two files are provided.
        :raises FileExistsError: If the output file exists and overwrite is not confirmed.
        :raises IOError: For issues in reading source files or writing the output file.
        """
        if len(file_paths) < 2:
            # Ensure atleast 2 files are provided
            raise ValueError("Need at least two files to perform merging")

        if os.path.exists(output_path) and not self.confirm_overwrite(output_path):
            # Check if output file exists and confirm overwrite if necessary (and if No)
            raise FileExistsError(f"Merge cancelled: {output_path} already exists")

        pdf_writer = PdfWriter() # Used to create a new PDF file
        for file_path in file_paths: # Loop through each file chosen
            try:
                pdf_reader = PdfReader(file_path) # Read each file to access contents like pages
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page) # Add each page to the new PDF of this file
            except Exception as e:
                # Raise an error if any of the files cannot be read
                raise IOError(f"Failed to process {file_path}. Error: {e}")

        try:
            # Writing the merged content to an output file
            with open(output_path, 'wb') as out: # 'wb' = binary write, writing binary data 
                pdf_writer.write(out)
        except Exception as e:
            # Raise an error if file cannot be written
            raise IOError(f"Failed to write merged file. Error: {e}")
        
    def split(self, file_path, page_range, output_path):
        """
        Splits a PDF file based on the provided page range and saves it to a new file.

        :param file_path: Path to the PDF file to split.
        :param page_range: Page range to split (e.g., "1-3, 5, 7").
        :param output_path: Path where the split PDF will be saved.
        :raises IOError: If there's an issue reading the input file or writing the output file.
        :raises ValueError: If the page range is invalid or out of bounds.
        """
        pdf_reader = PdfReader(file_path)
        pdf_writer = PdfWriter()

        # Logic to handle the page range written in helper function _split_pdf
        self._split_pdf(pdf_reader, page_range, pdf_writer)

        try:
            # Write the split PDF to file
            with open(output_path, "wb") as out:
                pdf_writer.write(out)
        except Exception as e:
            raise IOError(f"Failed to write split file. Error: {e}")

    def _split_pdf(self, pdf_reader, page_range, pdf_writer):
        """
        Helper function to handle the splitting based on the range given.

        :param pdf_reader: PdfReader object of the PDF to split.
        :param page_range: A string specifying the page range, e.g., "1-3, 5, 7".
        :param pdf_writer: PdfWriter object to add the split pages to.
        :raises ValueError: If the page range is invalid or out of bounds.
        """
        # Splitting the page_range string into individual page numbers and ranges
        ranges = page_range.split(",")
        total_pages = len(pdf_reader.pages) # For conditionals to raise error later

        for r in ranges: # Loop through each unit of entry (page number or range)
            r = r.strip() # remove leading and trailing whitespace
            if "-" in r: 
                # Processing a range of pages unit
                start, end = map(int, r.split("-"))
                if start <= end and 1 <= start <= total_pages and 1 <= end <= total_pages:
                    for page_num in range(start - 1, end):  # -1 to account for 0-indexing
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                else:
                    raise ValueError("Invalid page range")
            else:
                # Processing a single page unit
                page_num = int(r) - 1  # -1 to account for 0-indexing
                if 1 <= page_num + 1 <= total_pages:
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                else:
                    raise ValueError("Page number out of range")

    def add_watermark(self, file_path, watermark_text, output_path):
        """
        Adds a text watermark to each page of a PDF file.
        By default, the watermark is configured to be placed in the bottom left 
        corner of each page and it's tiny. 

        :param file_path: Path to the PDF file to be watermarked.
        :param watermark_text: Text to use as the watermark.
        :param output_path: Path where the watermarked PDF will be saved.
        :raises IOError: If there's an issue reading the input file or writing the output file.
        """
        pdf_reader = PdfReader(file_path)
        pdf_writer = PdfWriter()

        for page_number in range(len(pdf_reader.pages)): # Loop through each page in file
            packet = BytesIO() # Simulates a file in RAM, used for binary data
            can = canvas.Canvas(packet, pagesize=letter) # Create a PF canvas where you can draw/write on
            can.drawString(100, 100, watermark_text) # Drawing a string of text onto a PDF canvas
            can.save() 
            packet.seek(0) # Upon writing, need to move back to start of the buffer to read or save to an actual file
            new_pdf = PdfReader(packet)
            page = pdf_reader.pages[page_number] # Retrieve specific page in this loop 
            page.merge_page(new_pdf.pages[0]) # Merge watermark onto selected page 
            pdf_writer.add_page(page)

        try:
            with open(output_path, "wb") as out:
                pdf_writer.write(out)
        except Exception as e:
            raise IOError(f"Failed to write watermarked file. Error: {e}")

    def encrypt_pdf(self, file_path, password, output_path):
        """
        Encrypts a PDF file with user given password.

        :param file_path: Path to the PDF file to be encrypted.
        :param password: Password for encrypting the PDF.
        :param output_path: Path where the encrypted PDF will be saved.
        :raises IOError: If there's an issue reading the input file or writing the output file.
        """
        pdf_reader = PdfReader(file_path)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        pdf_writer.encrypt(password) 

        try:
            with open(output_path, "wb") as out:
                pdf_writer.write(out)
        except Exception as e:
            raise IOError(f"Failed to write encrypted file. Error: {e}")

    def decrypt_pdf(self, file_path, password, output_path):
        """
        Decrypts a PDF file with the given password.

        :param file_path: Path to the encrypted PDF file.
        :param password: Password for decrypting the PDF.
        :param output_path: Path where the decrypted PDF will be saved.
        :raises IOError: If there's an issue reading the input file or writing the output file.
        """
        pdf_reader = PdfReader(file_path)
        pdf_reader.decrypt(password)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        try:
            with open(output_path, "wb") as out:
                pdf_writer.write(out)    
        except Exception as e:
            raise IOError(f"Failed to write decrypted file. Error: {e}")

class PdfGui:
    """
    This class is responsible for creating the graphical user interface (GUI) for the PDF editor.
    It uses tkinter for creating and managing GUI elements.
    Calls the PdfEdit class to perform the actual PDF editing operations. 
    """
    def __init__(self, root):
        """
        Initializes the GUI components for the PDF editor.

        :param root: The main window for the tkinter GUI, typically an instance of tk.Tk()
        """
        self.root = root
        root.title("PDF Editor")

        # Setting window size
        root.geometry("300x445")

        # Creating a button
        # command as self.merge, the function merge is called which belong to PdfGui class
        self.merge_button = tk.Button(root, text="Merge PDFs", command=self.merge, width=40, height=5)
        # Pack button into parent container, making it visible to user. 
        # Important line, if not packed, button is created but not visible to user
        self.merge_button.pack()

        self.split_button = tk.Button(root, text="Split PDF", command=self.split, width=40, height=5)
        self.split_button.pack()

        self.watermark_button = tk.Button(root, text="Add Watermark", command=self.add_watermark, width=40, height=5)
        self.watermark_button.pack()

        self.encrypt_button = tk.Button(root, text="Encrypt PDF", command=self.encrypt_pdf, width=40, height=5)
        self.encrypt_button.pack()

        self.decrypt_button = tk.Button(root, text="Decrypt PDF", command=self.decrypt_pdf, width=40, height=5)
        self.decrypt_button.pack()

    def confirm_overwrite(self, file_path):
        """
        Confirms with the user whether to overwrite an existing file.

        :param file_path: The path of the file which might be overwritten.
        :return: True if the user confirms to overwrite, False otherwise.
        """
        # GUI version using Tkinter's messagebox
        return messagebox.askyesno("Overwrite File", f"The file {file_path} already exists. Do you want to overwrite it?")

    def merge(self):
        """
        Handles the merging of PDF files. Opens a file dialog for the user to select multiple PDF files,
        merges them, and saves the merged PDF to a specified location. Also handles errors and informs
        the user about the status of the operation.
        """
        # Allows selection of multiple pdf type files with the use of * and .pdf
        file_paths = filedialog.askopenfilenames(
            filetypes=[("PDF files", "*.pdf")], title="Select PDF Files to Merge"
        )
        # Shows user appropriate error messages as need >= 2 files
        if len(file_paths) < 2:
            messagebox.showwarning("Not Enough Files", "Please select at least two files to merge.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Merged PDF As"
        )
        # To make sure user has selected an output file
        if not output_path:
            messagebox.showwarning("No Output File Selected", "Please select an output file.")
            return

        pdf_edit = PdfEdit()
        try:
            # Pass the confirm_overwrite function to PdfEdit
            pdf_edit.merge(file_paths, output_path, self.confirm_overwrite)
            messagebox.showinfo("Success", f"PDF files have been merged into {output_path}")
        except FileExistsError as e: # Error with file already exists
            messagebox.showinfo("Merge Cancelled", str(e))
        except Exception as e: # Any other error
            messagebox.showerror("Error", f"Failed to merge files. Error: {e}")


    def split(self):
        """
        Handles the splitting of a PDF file. Opens a file dialog for the user to select 
        a PDF file, splits them and saves the split PDF to a specified location. 
        Also handles errors and informs the user about the status of the operation.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")], title="Select PDF File to Split"
        )
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select a file to split.")
            return
        # New feature, requesting input from user for page range
        page_range = simpledialog.askstring("Page Range", "Enter page range (e.g., 1-3, 5, 7):")
        # Mandatory input validation
        if not page_range:
            messagebox.showwarning("No Page Range Chosen", "Please enter a page range.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Split PDF As"
        )
        if not output_path:
            messagebox.showwarning("No Output File Selected", "Please select an output file.")
            return

        pdf_edit = PdfEdit()
        try:
            pdf_edit.split(file_path, page_range, output_path)
            messagebox.showinfo("Success", f"PDF has been split and saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to split file. Error: {e}")


    def add_watermark(self):
        """
        Handles the addition of a watermark into each page of a PDF file of user's choice.
        Opens a file dialog for user to select a PDF file, adds the watermark, and
        saves the modified PDF to a specified location. Also handles errors and informs
        user about the status of the operation. 
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")], title="Select PDF File to Add Watermark"
        )
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select a file to add watermark.")
            return
        # New feature, requesting input from user for watermark text
        watermark_text = simpledialog.askstring("Watermark Text", "Enter watermark text:")
        if not watermark_text:
            messagebox.showwarning("No Watermark Text", "Please enter watermark text.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Watermarked PDF As"
        )
        if not output_path:
            messagebox.showwarning("No Output File Selected", "Please select an output file.")
            return

        pdf_edit = PdfEdit()
        try:
            pdf_edit.add_watermark(file_path, watermark_text, output_path)
            messagebox.showinfo("Success", f"Watermark added and saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add watermark. Error: {e}")


    def encrypt_pdf(self):
        """
        Handles the GUI for PDF encryption. Requests a password and user's input
        for the encryption. Also handles errors and informs the user about
        the status of the operation, and as usual saves the file in the specified
        location.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")], title="Select PDF File to Encrypt"
        )
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select a file to encrypt.")
            return

        password = simpledialog.askstring("Password", "Enter a password for encryption:", show="*")
        if not password:
            messagebox.showwarning("No Password", "Please enter a password.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Encrypted PDF As"
        )
        if not output_path:
            messagebox.showwarning("No Output File Selected", "Please select an output file.")
            return

        pdf_edit = PdfEdit()
        try:
            pdf_edit.encrypt_pdf(file_path, password, output_path)
            messagebox.showinfo("Success", f"PDF has been encrypted and saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt file. Error: {e}")


    def decrypt_pdf(self):
        """
        Handles the GUI for PDF decryption. Ensures protected file's password 
        and user's input matches. Also handles errors and informs the user about
        the status of the operation, and as usual saves the file in the specified
        location.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")], title="Select Encrypted PDF File to Decrypt"
        )
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select a file to decrypt.")
            return

        password = simpledialog.askstring("Password", "Enter the password to decrypt the PDF:", show="*")
        if not password:
            messagebox.showwarning("No Password", "Please enter a password.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Decrypted PDF As"
        )
        if not output_path:
            messagebox.showwarning("No Output File Selected", "Please select an output file.")
            return

        pdf_edit = PdfEdit()
        try:
            pdf_edit.decrypt_pdf(file_path, password, output_path)
            messagebox.showinfo("Success", f"PDF has been decrypted and saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt file. Error: {e}")


def main():
    """
    The main function to initialize and run the tkinter GUI application.
    """
    # Creating main window for GUI application
    # tk.Tk() is a constructor that initializes a tkinter 'Tk' object which serves as main window
    root = tk.Tk()
    # Creating an instance of PdfGui class
    # root is passed in PdfGui, PdfGui object wil be associated with and displayed in main window
    # basically, initializing GUI by creating an instance of the "PdfGui" class within main window
    gui = PdfGui(root)
    # main event loop is core of any gui application, listens and responds to user interaction
    # enables program to run until user closes main window or exits application
    root.mainloop()

if __name__ == "__main__":
    main()  
