# Emily M. Hoang
# Spring quarter 2016 project
# Edited Sept. 2018


import glob



# pre: needs list of words
# post: returns list with all words lowercase
def all_lowercase(words_list):
    for i in range(len(words_list)):
        words_list[i] = words_list[i].lower()
    return words_list



# pre: needs search phrase
# post: returns length of search phrase
def check_length(s_phrase):
    counter = 0
    for element in s_phrase:
        for char in element:
            counter += 1

    return counter



# pre: none
# post: returns list of all filenames in current directory
# with .txt extension
def getFilesInDir():
    file_names = glob.glob('./*.txt') 
    for i in range(len(file_names)):
        file_names[i] = file_names[i][2:]

    print("There are", len(file_names), ".txt files in this directory.")
    print(file_names)
    return file_names



# pre: needs list of stop words and list of punctuation symbols
# post returns valid search phrase
def get_phrase(stop_l, punc_symbols):
    invalid_input = True
    while invalid_input: #while input is invalid
        search = input("Enter the phrase to search: ")
        search = search.split(" ") 

        #Check for digits
        contains_digit = test_for_digits(search)
        if contains_digit == True:
            print("Invalid entry; try again.")

        else:
            #Clean search_phrase  
            search = remove_punctuation(search, punc_symbols)
            search = remove_stopwords(search, stop_l)

            #Check length
            length = check_length(search)
            if length >= 1:
                invalid_input = False
            else:
                print("Invalid entry; try again.")

    return search



# pre: no argument
# post: returns list of stop words
def get_stop_words():
    stop_list = [] #create list for stop words
    stop_file = open("StopWords.csv", "r")
    for l in stop_file:
        l = l.rstrip()
        stop_list.append(l)
    stop_file.close()
    return stop_list



# pre: returns list of all filenames in current directory with .txt extension,
# search phrase, list of punctuation, and list of stop words.
# post: reads, processes, and closes each file.
def process_all(all_files, search_p, punc_l, stop_l):
    for i in range(len(all_files)): #open and process files one at a time
        infile = all_files[i] 
        current_file = open(infile, "r") 

        process_file(infile, current_file, search_p, punc_l, stop_l)

        current_file.close()


        
# pre: needs name of file to process, the actual file to process, search phrase,
# list of puntuation, and list of stop words.
# post: prints the number of times that search phrase appears in file
def process_file(name_file, afile, search_phr, pun_list, st_list):
    occurrences = 0
    for l in afile:
        l = l.split(" ") 
        
        #clean up each line, make lowercase
        l = remove_punctuation(l, pun_list) 
        l = remove_stopwords(l, st_list)
        all_lowercase(l)

##        index = -1
##        for el in l:
##            index += 1
##            if index <= (len(search_phr)-1):
##                if search_phr[index] == el:
##                    if index == len(search_phr):
##                        occurrences += 1
                    
        index = 0
        for el in l:
            if search_phr[index] == el:
                index += 1
            else:
                index = 0
            if index == len(search_phr):
                occurrences += 1
                index = 0

    print("File", name_file, "has", occurrences, "occurrences of the phrase", search_phr)



# pre: returns list of all filenames in current directory with .txt extension,
# search phrase, list of punctuation, and list of stop words.
# post: reads, processes, and closes each valid file input by user.
def process_some(all_files, search_p, punc_l, stop_l):

    while True: 
        number_files = int(input("How many files do you want to search in? "))
        if number_files < 0 or number_files > len(all_files):  # if number of files is less than 0
                                                          # or more than in directory
            print("Invalid entry; try again.")
        else:
            break
    
    for i in range(number_files):
        invalid_input = True
        while invalid_input:
            file_name = input("Enter the file name with extension: ")
            file_name_list = list(file_name) #convert file name into a list
            if file_name_list[len(file_name_list)-1]=="t" and \
               file_name_list[len(file_name_list)-2]=="x" and \
               file_name_list[len(file_name_list)-3]=="t" and \
               file_name_list[len(file_name_list)-4]=="." and \
               file_name in all_files: # if file name has ".txt" extention AND exists in directory
                break
            else:
                print("We can only search in existing .txt files.")

        current_file = open(file_name, "r")
        process_file(file_name, current_file, search_p, punc_l, stop_l)
        current_file.close()   


        
# pre: needs phrase list to clean and list of punctuation symbols
# post: returns phrase list without puncutation
def remove_punctuation(phrase_list, punc_list):
    index = -1
    for word in phrase_list:
        index += 1
        for el in punc_list:
            if el in word:
                no_punc_word = word.rstrip(el) #strip ending punctuation symbol 
                phrase_list[index] = no_punc_word #replace word into to_clean without punctuation

    return phrase_list



# pre: needs phrase list to clean and list of stop words
# post: returns phrase list without stop words
def remove_stopwords(to_clean, stop_w):
    clean = [] #create list for phrase list without stop words
    for word in to_clean:
        if word not in stop_w: 
            clean.append(word)

    return clean



# pre: needs search phrase 
# post: returns flag "digit".  "True" means search phrase contains
# digits; "False" means it does not contain digits.
def test_for_digits(phrase):
    digit = False #set flag where "False" means no digits
    for el in phrase:
        if el.isdigit():
            digit = True
            break
    return digit



def main():
    punctuation = [".", ",",":",";","!","?"]
    stop_words = get_stop_words() 
    all_lowercase(stop_words)
    choice = "Yes"
    while choice == "Yes":
        search_phrase = get_phrase(stop_words, punctuation)
        all_lowercase(search_phrase)
        files = getFilesInDir()
        choice = input("Type Y to search all the txt files in the current" \
                       " folder: ")
        if choice == "Y":
            process_all(files, search_phrase, punctuation, stop_words)
        else:
            process_some(files, search_phrase, punctuation, stop_words)

        choice = input("Do you want to search again?  Type \"Yes\" to continue searching: ")

main()
