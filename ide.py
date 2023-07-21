from tkinter import *
from tkinter.colorchooser import askcolor
import ctypes
import re
import os

# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Setup Tkinter
root = Tk()
root.geometry('500x500')


# Execute the Programm
def execute(event=None):

    # Write the Content to the Temporary File
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    # Start the File in a new CMD Window
    os.system('start cmd /K "python run.py"')

# Register Changes made to the Editor Content
def changes(event=None):
    repl = [
        ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords, keywords_font],
        ['print|exec', keywords, normal_font],
        ['".*?"|/\\\"', string, string_font],
        ['\'.*?\'', string, string_font],
        ['#.*?$', comments, keywords_font]
    ]

    # Remove all tags so they can be redrawn
    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")

    # Add tags where the search_re function found the pattern
    code = editArea.get('1.0', END)
    i = 0
    for pattern, color2, font2 in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color2)
            font_parts = str(font2).split(" ")
            editArea.tag_config(f'{i}', font=(font_parts[0].replace("-", " "), int(font_parts[1]), font_parts[2]))

            i+=1

def search_re(pattern, text, groupid=0):
    matches = []

    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):

            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches


def rgb(rgb):
    return "#%02x%02x%02x" % rgb


previousText = ''

# Define colors for the variouse types of tokens
normal = rgb((234, 234, 234))
keywords = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))
imports = rgb((234, 234, 234))
normal_font = 'Consolas 15 '
keywords_font = 'Segoe-Print 15 italic'
string_font = '©Malgun-Gothic 15 italic'

def change_color_keywords():
    color = askcolor()
    global keywords
    keywords = rgb(color[0])
    print(keywords)


menu = Menu(root)
menubar = Menu(menu)
color = Menu(menubar)
color.add_command(label="Keywords", command=change_color_keywords)
menubar.add_cascade(label="Color", menu=color)
root.config(menu=menubar)

# Define a list of Regex Pattern that should be colored in a certain way
repl = [
    [],
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|global|if|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield|print)($| )', keywords, keywords_font],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
]

# Make the Text Widget
# Add a hefty border width so we can achieve a little bit of padding
editArea = Text(
    root,
    background=background,
    foreground=normal,
    insertbackground=normal,
    relief=FLAT,
    borderwidth=30,
    font=normal_font
)

# Place the Edit Area with the pack method
editArea.pack(
    fill=BOTH,
    expand=1
)

# Insert some Standard Text into the Edit Area
editArea.insert('1.0', """from argparse import ArgumentParser
from random import shuffle, choice
import string

# Setting up the Argument Parser
parser = ArgumentParser(
    prog='Password Generator.',
    description='Generate any number of passwords with this tool.'
)
""")

# Bind the KeyRelase to the Changes Function
editArea.bind('<KeyRelease>', changes)

# Bind Control + R to the exec function
root.bind('<Control-r>', execute)

changes()
root.mainloop()
