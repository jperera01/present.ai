#======================================================
#CSC430 PDF Analysis Prototype
#Count words on each page & perform sentiment analysis
#======================================================

#------------------------------------------------------
#INSTALLS
#------------------------------------------------------
# pip install PyMuPDF nltk
# nltk.download('vader_lexicon') #if needed

#------------------------------------------------------
#LIBRARIES
#------------------------------------------------------
#- interface
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
#- pdf analysis
import fitz  #PyMuPDF
import nltk 
from nltk.sentiment import SentimentIntensityAnalyzer
#- general/other 
import os
import tempfile

#------------------------------------------------------
#PDF-ANALYSIS CORE BEHAVIOR
#------------------------------------------------------
class PdfSentimentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Sentiment Analysis")
        self.geometry("400x250")
        
        #-button to upload PDF
        self.upload_button = tk.Button(self, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.pack(pady=20)

        #-text box to display results
        self.results_text = tk.Text(self, height=10, width=50)
        self.results_text.pack(side=tk.LEFT, pady=10, fill=tk.BOTH, expand=True)

        #-create a scrollbar and attach to text box
        scrollbar = tk.Scrollbar(self, orient='vertical', command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        #-configure text widget to work with scrollbar
        self.results_text.config(yscrollcommand=scrollbar.set)

        #-setup sentiment analyzer
        self.sia = SentimentIntensityAnalyzer()

    #upload_pdf(): open file dialog + retrieve file path
    def upload_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filepath:
            self.analyze_pdf(filepath)
            
    #analyze_pdf(): perform analysis on full-pdf & generate output
    def analyze_pdf(self, filepath):
        doc = fitz.open(filepath)  # open PDF
        self.results_text.delete(1.0, tk.END)  # clear previous results
        self.results_text.insert(tk.END, "Page-wise Sentiment Analysis:\n\n")
        
        #-iterate through pages
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            words = text.split()
            word_count = len(words)
            sentiment = self.sia.polarity_scores(text)
            
            #--display results
            result = (f"Page {page_num}: {word_count} words\n"
                      f"Sentiments: {sentiment}\n\n")
            self.results_text.insert(tk.END, result)
        
        doc.close()

#------------------------------------------------------
#MAIN
#------------------------------------------------------
if __name__ == "__main__":
    app = PdfSentimentApp()
    app.mainloop()

