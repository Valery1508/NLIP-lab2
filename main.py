from tkinter import *
from tkinter import filedialog as fd

import nltk
from bs4 import BeautifulSoup

from help import HELPTEXT
import time

import nltk
nltk.download('averaged_perceptron_tagger_ru')

DOT = '.'
COMMA = ','
FG = '-'
GRAMMAR_RULES = r"""
        P: {<IN>}
        V: {<V.*>}
        N: {<S.*>}
        NP:{<PR>*<A.*|A-PRO><CONJ>*<A.*|A-PRO>*<N|NP>}   
        NP:{<A.*|A-PRO>*<S.*>+<A.*|A-PRO>*} 
        VP: {<V.*>+<NP|N>}
        VP: {<V.*>}

        """


def download_nltk_dependencies():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')


def open_file():
    file_name = fd.askopenfilename(filetypes=(("HTML files", "*.html"),))
    if file_name != '':
        file = open("example.html", "r", encoding="utf-8")
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')
        calculated_text.insert(1.0, soup.body.text)


def info():
    children = Toplevel()
    children.title('Help')
    children.geometry("600x300+500+350")
    outputHelpText = Text(children, height=20, width=80)
    scrollb = Scrollbar(children, command=outputHelpText.yview)
    scrollb.grid(row=4, column=8, sticky='nsew')
    outputHelpText.grid(row=4, column=0, sticky='nsew', columnspan=3)
    outputHelpText.configure(yscrollcommand=scrollb.set)
    outputHelpText.insert('end', HELPTEXT)
    outputHelpText.configure(state='disabled')


def draw_tree():
    start = time.time()
    text = calculated_text.get(1.0, END)
    text = text.replace('\n', '')
    if text != '':
        download_nltk_dependencies()
        doc = nltk.word_tokenize(text)
        doc = nltk.pos_tag(doc, lang='rus')
        new_doc = []
        for item in doc:
            if item[1] != COMMA and item[1] != DOT and item[1] != FG:
                new_doc.append(item)
        cp = nltk.RegexpParser(GRAMMAR_RULES)
        result = cp.parse(new_doc)
        result.draw()
    end = time.time()
    print("Total time: {:.1f}".format(end - start))


root = Tk()
root.title("Sentence parse tree")

root.resizable(width=False, height=False)
root.geometry("620x150+500+250")

label = Label(root, text='Input text:', font=("Times new roman", 13, "bold"))
label.grid(row=0, column=0)

calculated_text = Text(root, height=5, width=50)
calculated_text.grid(row=1, column=1, sticky='nsew', columnspan=2)

help_button = Button(text="Help", width=10, command=info)
help_button.grid(row=0, column=3)

open_button = Button(text="Open file", width=10, command=open_file)
open_button.grid(row=1, column=3)

ok_button = Button(text="Parse sentence", width=14, command=draw_tree)
ok_button.grid(row=2, column=3)
root.mainloop()