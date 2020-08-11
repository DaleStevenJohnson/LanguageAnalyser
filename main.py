import re
import os
from string import ascii_uppercase as alphabet


def remove_symbols(text):
    text = list(text)
    symbols = [",", "/", ".", ":", ";", "'", "\"", "#", "£", "$", "%", "(", ")", "[", "]", "{", "}", "|", "!", "?", "*", "&"]
    for i in range(len(text)):
        if text[i] in symbols:
            text[i] = " "
    text = "".join(text)
    return text

def get_file_paths(directory):
    files = []
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            files.append(os.path.join(directory, file))
    return files

def read_files(filepaths):    
    texts = []
    for path in filepaths:
        texts.append(read_file(path))
    return texts

def read_file(filename):
    with open(filename, "r") as file:
        text = file.read()
    return text



def count_letters(text):
    text = list(text)
    letters = {"counts":{}, "percents":{}}
    total = 0
    for letter in text:
        letter = letter.upper()
        test = re.search(r"^[a-zA-Z]+$", letter)
        #print(word, test)
        if test != None and len(letter) > 0:
            if letter in letters["counts"]:
                letters["counts"][letter] += 1
            else:
                letters["counts"][letter] = 1
            total += 1
    ptotal = 0
    for letter in letters["counts"]:
        percent = (letters["counts"][letter]/total)*100
        letters["percents"][letter] = round(percent, 2)
        ptotal += percent
    letters["counts"]["total"] = total
    letters["percents"]["total"] = ptotal
    return letters

def print_result(result):
    # Print Headings
    template = "{}{} | {}{} | {}{}\n"
    output = "\n\n\nSource: {}\n".format(result["source"])
    headings = ["Letter","Count","Percentage"]
    output += template.format(headings[0], "", headings[1], "", headings[2], "")
    dashes = template.format(len(headings[0]) * "-", "", len(headings[1]) * "-", "", len(headings[2]) * "-", "")
    output += dashes
    
    # Print Individual Letter Data
    for char in alphabet:
        if char in result["counts"]:
            charspace = " " * (len(headings[0]) - len(char))
            count = str(result["counts"][char])
            countspace = " " * (len(headings[1]) - len(count))
            percent = str(result["percents"][char])+" %"
            percentspace = " " * (len(headings[2]) - len(percent))
            output += template.format(char, charspace, count, countspace, percent, percentspace)
    
    # Print totals
    output += dashes
    total = "Total"
    totalspace = " " * (len(headings[0]) - len(total))
    count = str(result["counts"]["total"])
    countspace = " " * (len(headings[1]) - len(count))
    percent = str(result["percents"]["total"])+" %"
    percentspace = " " * (len(headings[2]) - len(percent))
    output += template.format(total, totalspace, count, countspace, percent, percentspace)
    print(output)


def main():
    filepaths = get_file_paths("texts")

    for path in filepaths:
        text = read_file(path)
        result = count_letters(text)
        result["source"] = path
        print_result(result)

main()