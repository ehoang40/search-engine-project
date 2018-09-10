# Emily M. Hoang
# spring quarter 2016

import glob

# pre: needs list of punctuation symbols and list of stop words
# post returns search phrase and list of punctuation
def get_phrase(punctuation, stopWords):
    #ONE BIG WHILE LOOP
    validInput = False
    while not(validInput): #while input is NOT valid
        search_phrase = input("Enter the phrase to search: ")
        search_phrase = search_phrase.split(" ") 

        #Check for digits
        digit = test_for_digits(search_phrase)

        #Clean up  
        search_phrase = remove_punctuation(search_phrase,punctuation)
        search_phrase = remove_stopwords(search_phrase, stopWords)

        #CHECK LENGTH
        less_than_two = True
        length = 0
        for element in search_phrase:
            for char in element:
                length += 1
                
        if length >= 2:
            less_than_two = False

        if digit == False and less_than_two == False: #if there are no digits and length
                                                      #is not less than 2
            validInput = True
        else:
            print("Invalid entry; try again.")

    return search_phrase, punctuation


# pre: needs search phrase
# post: returns flag "digit".  "True" means search phrase contains
# digits; "False means it does not contain digits.
def test_for_digits(search_phrase):
    digit = False #set flag, "False" means no digits
    for element in search_phrase:
        if element.isdigit():
            digit = True
    return digit


# pre: needs list to clean and list of stop words
# post: returns list w/o stop words
def remove_stopwords(to_clean, stopWords):
    clean = []

    for word in to_clean:
        if word not in stopWords:
            clean.append(word)

    return clean


# pre: needs list to clean and list of punctuation symbols
# post: returns list w/o puncutation
def remove_punctuation(to_clean,punctuation):
    search_phrase = [""]*len(to_clean) #create new list with same length as search_phrase (w/o stop
                                     #words).  This will become new search phrase, but without
                                     #punctuation.
    index = -1
    for word in to_clean:
        index += 1
        for el in punctuation:
            if el in word:
                word2 = word.rstrip(el) #strip ending punctuation symbol off word
                search_phrase[index] = word2 #replace with cleaned up word
                break
            else:
                search_phrase[index] = word
    return search_phrase

# pre: needs text file, search phrase, list of punctuation symbols, and list of
# stop words
# post: accepts files, processes them, and prints results of search query
def filesToProcess(file,search_phrase, punctuation, stopWords):
    print("There are", len(file), ".txt files in this directory.")
    choice = input("Type Y to search all the txt files in the current" \
                   " folder: ")

    if choice == "Y": 
        for i in range(len(file)): #open and process each file one at a time
            infile = file[i] 
            file_to_process = open(infile, "r") 

            occurences = processFile(file_to_process, search_phrase, punctuation, stopWords)
            print("File", infile, "has", occurences, "occurences of the phrase", search_phrase)
            file_to_process.close()
    else:
        number_files = int(input("How many files do you want to search in? "))
        while not(number_files > 0) or not(number_files <= len(file)): #while number of files
        #entered is not greater than 0 AND not less than or equal to number of files in directory
            print("Invalid entry; try again.")
            number_files = int(input("How many files do you want to search in? "))

        for i in range(number_files):
            validInput = False
            while not(validInput):
                name_of_file = input("Enter the file name with extension: ")
                name_of_file2 = list(name_of_file) #turn name of file entered into a list
                if name_of_file2[len(name_of_file2)-1]=="t" and \
                   name_of_file2[len(name_of_file2)-2]=="x" and \
                   name_of_file2[len(name_of_file2)-3]=="t" and \
                   name_of_file2[len(name_of_file2)-4]=="." and \
                   name_of_file in file: #if last four characters of file name is ".txt" AND
                   #the name exists in the directory
                    validInput = True
                else:
                    print("We can only search in .txt files which already exist.")

            file_to_process = open(name_of_file, "r")
            occurences = processFile(file_to_process, search_phrase, punctuation, stopWords)
            print("File", name_of_file, "has", occurences, "occurences of the phrase", search_phrase)
            file_to_process.close()   


# pre: needs file to process, search file, list of punctuation symbols, and list of
# stop words
# post: returns number of times search phrase appears in file
def processFile(file, search_phrase, punctuation, stopWords):
    occurences = 0
    for l in file:
        l = l.split(" ") 
        
        #clean up each line, make lowercase
        l = remove_punctuation(l, punctuation) 
        l = remove_stopwords(l, stopWords)
        l = all_lowercase(l)

        index = 0
        for element in l:
            if search_phrase[index] == element:
                index += 1
            else:
                index = 0
            if index == len(search_phrase):
                occurences += 1
                index = 0
    return occurences

# pre: no argument
# post: returns list of stop words
def get_stopWords():
    stopWords = [] #list for stop words
    file = open("StopWords.csv", "r")
    for l in file:
        l = l.rstrip()
        stopWords.append(l)
    file.close()
    return stopWords

       
### pre: none
### post: returns list of all filenames in current directory
##  with .txt extension
def getFilesInDir():
    filenames = glob.glob('./*.txt') 
    for i in range(len(filenames)):
        filenames[i] = filenames[i][2:]
    return filenames

# pre: needs list with only letters
# post: returns list with all lower-case letters
def all_lowercase(list):
    for i in range(len(list)):
        list[i] = list[i].lower()
    return list
    
def main():
    punctuation = [".", ",",":",";","!","?"]
    stopWords = get_stopWords()
    stopWords2 = all_lowercase(stopWords)
    choice = "Y"
    while choice == "Y":
        search_phrase, punctuation = get_phrase(punctuation, stopWords)
        search_phrase2 = all_lowercase(search_phrase)
        filenames = getFilesInDir()
        filesToProcess(filenames, search_phrase, punctuation, stopWords)
        choice = input("Do you want to search again?  Say Y to continue searching: ")

main()
