from fpdf import FPDF
import pandas as pd
import numpy as np
import unicodedata

def convert(s): #https://stackoverflow.com/questions/51186075/python-convert-this-utf8-string-to-latin1 
    r=''
    for c in s:
        try:
            c.encode('latin-1')
        except UnicodeEncodeError:
            c = unicodedata.normalize('NFKD', c).encode('latin-1', 'ignore').decode('latin-1')
        r += c
    return r

class PDF(FPDF):
    def __init__(self):
        super().__init__('L','mm')                
        self.alias_nb_pages()
        self.add_page() 
        self.yel=False     
        #self.set_doc_option('core_fonts_encoding', 'windows-1252') # not working https://github.com/PyFPDF/fpdf2/issues/330   >>> def convert(s)
        
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 10
        self.set_font('Arial', 'I', 10)
        # Page number
        self.cell(0, 5, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    def reptitle(self):
        title='Two thousand restaurants from the federal state of Bavaria with email addresses'
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, title, 0, 1, 'C')        
        self.ln()        
    def tablehead(self):
        #self.set_draw_color(84,115,200)
        self.set_fill_color(220,20,60)   #(84,115,200)
        self.set_text_color(255)
        # Set font
        self.set_font('Arial', 'B', 10)        
        self.cell(70, 5, 'Name', 0, 0, 'L', fill=True)
        self.cell(8+8+8, 5, 'Rt. Rev.Claimed', 0, 0, 'L', fill=True)
        self.cell(55, 5, 'Address', 0, 0, 'L', fill=True)
        self.cell(30, 5, 'Phone', 0, 0, 'L', fill=True)
        self.cell(40, 5, 'Website URL', 0, 0, 'L', fill=True)
        self.cell(0, 5, 'E-mail address', 0, 1, 'L', fill=True)
    def tablerow(self,row):
        self.set_text_color(0)
        if self.yel: self.set_fill_color(245,245,222)
        else:self.set_fill_color(255)        
        self.set_font('Arial', '', 10)        
        self.cell(70,5,convert(str(row['name'])),0,0,'L',fill=True)
        self.cell(8,5,str(row["rating"]),0,0,'R',fill=True)
        self.cell(8,5,'{0:.0f}'.format(row["reviews"]),0,0,'R',fill=True)
        self.cell(8,5,row["claimed"],0,0,'R',fill=True)
        self.cell(55,5,convert(str(row["address"])[:80]),0,0,'L',fill=True)
        self.cell(30,5,str(row["phone"]),0,0,'L',fill=True)
        self.cell(40,5,convert(str(row["website"])[:50]),0,0,'L',fill=True)
        self.cell(0,5,convert(str(row["mail"])[:31]),0,1,'L',fill=True)
        self.yel = not self.yel
    def summary(self, a, w, m):
        self.ln(12)
        self.set_font('Arial', 'B', 10)        
        self.set_x(50)
        self.write(5,'SUMMARY:')              
        self.set_fill_color(245,245,222)
        self.set_x(120)
        self.cell(100,5,'Total number of records:',0,0,'L',fill=True)
        self.cell(20,5,str(a),1,1,'R',fill=True)
        self.set_x(120)
        self.cell(100,5,'With website:',0,0,'L',fill=False)
        self.cell(20,5,str(w),1,1,'R',fill=False)
        self.set_x(120)
        self.cell(100,5,'With e-mail addresses:',0,0,'L',fill=True)
        self.cell(20,5,str(m),1,0,'R',fill=True)
        
def main():        
    p=PDF()
    p.reptitle()       
    p.tablehead()
    wm = pd.read_csv('withmails.csv')
    wm.reset_index()
    for index,row in wm.iterrows():
        if p.get_y() > 185:
            p.add_page()
            p.yel=False
            p.tablehead()
        p.tablerow(row)    
    # summary
    if p.get_y() > 165:
        p.add_page()   
    c = wm.count()
    p.summary(c['name'],c['website'],c['mail'])
    p.output('reportb.pdf', 'F')    

if __name__ == "__main__":
    main()    
    
"""
%load_ext autoreload
%autoreload 2

"""    
