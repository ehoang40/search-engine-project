# Emily M. Hoang
# Spring quarter 2016 project
# Edited Oct. 2018

"""Text Search Engine Project

With this script, a user can run a search query in .txt files and obtain
the number of times the query .  The user
can either search all .txt files in the directory or specify certain
files.  The search is keyword-based and is not case sensitive.  The
search only identifies matches that are contained on one line of the
file(s), not wrapped over multiple lines.

If the user does not want to search all .txt files, s/he must enter an
intenger to specify how many.

The query must be contain at least one alphabetic character and contain
no stand-alone digits.  E.g., the phrase "Hello 123" is invalid, but
"Hello123" is valid.

This script requires the 'glob' module.

All functions (except main()) are defined alphabetically for easy
reference.
"""

import glob


def all_lowercase(words_list):
    """
    Accept a list of strings and return the list made lowercase.
	
    Parameters:
    words_list (list): List of strings

    Returns:
    list: List of lowercase strings
    """
    
    for i in range(len(words_list)):
        words_list[i] = words_list[i].lower()
    return words_list


def check_length(s_phrase):
    """
    Accept the search phrase as a list and return its length. 
	
    Parameters:
    s_phrase (list): List of strings
	
    Returns:
    int: Length of search phrase
    """
    
    counter = 0
    for element in s_phrase:
        for char in element:
            counter += 1

    return counter


def getFilesInDir():
    """
    Return the list of .txt filenames in the current directory.
	
    Returns:
    list: Filenames with .txt extension in directory
    """
    
    file_names = glob.glob('./*.txt') 
    for i in range(len(file_names)):
        file_names[i] = file_names[i][2:]

    print("There are", len(file_names), ".txt files in this directory.")

    return file_names


def get_phrase(stop_l, punc_symbols):
    """
    Prompt for a valid search query and return the simplified version.
	
    Parameters:
    stop_l (list): List of stop words
    punc_symbols (list): List of punctuation symbols
	
    Returns:
    list: Search query as a list without stop words and punctuation
    """
    
    invalid_input = True
    while invalid_input: #While input is invalid
        search = input("Enter the phrase to search: ")
        search = search.split(" ") 

        #Check for stand-alone digits
        contains_digit = test_for_digits(search)
        if contains_digit == True:
            print("The query cannot contain stand-alone digits.  Please try again.")

        else:
            #Clean search_phrase  
            search = remove_punctuation(search, punc_symbols)
            search = remove_stopwords(search, stop_l)

            #Check length
            length = check_length(search)
            if length >= 1:
                invalid_input = False
            else:
                print("The query must contain at least one alphabetic character. Please try again.")

    return search


def get_stop_words():
    """
    Return a list of stop words.
	
    Returns:
    list: List of stop words
    """
    
    stop_list = [] #create list for stop words
    stop_file = open("StopWords.csv", "r")
    for l in stop_file:
        l = l.rstrip()
        stop_list.append(l)
    stop_file.close()

    return stop_list


def process_all(all_files, search_p, punc_l, stop_l):
    """
    Search all .txt files in the current directory.
	
    Parameters:
    all_files (list): List of all .txt filenames in directory
    search_p (list): Search phrase as a list
    punc_l (list): List of punctuation symbols
    stop_l (list): List of stop words
    """
    
    for i in range(len(all_files)): #open and process files one at a time
        infile = all_files[i] 
        current_file = open(infile, "r") 

        process_file(infile, current_file, search_p, punc_l, stop_l)

        current_file.close()


def process_file(name_file, afile, search_phr, pun_list, st_list):
    """
    Search a file for the search query.

    Paramters:
    name_file (string): Name of .txt file
    afile (file object): File open for reading
    search_phr (list): Search phrase as a list
    pun_list (list): List of punctuation symbols
    st_list (list): List of stop words
    """
    
    occurrences = 0
    for l in afile:
        l = l.split(" ") 
        
        #clean up each line, make lowercase
        l = remove_punctuation(l, pun_list) 
        l = remove_stopwords(l, st_list)
        all_lowercase(l)

        index = 0
        for el in l:
            if search_phr[index] == el:
                index += 1
            if index == len(search_phr):
                occurrences += 1
                index = 0

    print("File", name_file, "has", occurrences, "occurrences of the phrase", search_phr)


def process_some(all_files, search_p, punc_l, stop_l):
    """
    Search all valid .txt files specified by the user.

    Parameters:
    all_files (list): List of all .txt filenames in directory
    search_p (list): Search phrase as a list
    punc_l (list): List of punctuation symbols
    stop_l (list): List of stop words
    """
    
    while True: 
        number_files = int(input("How many files do you want to search in? "))
        if number_files < 0 or number_files > len(all_files):  # if number of files is less than 0
                                                          # or more than in directory
            print("The number of files must be between 0 and", len(all_files), ".")
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

        
def remove_punctuation(for_cleaning, punc_list):
    """
    Remove punctuation from a phrase.

    Parameters:
    for_cleaning (list): Phrase as a list
    punc_list (list): List of punctuation symbols

    Returns:
    list: Phrase without punctuation
    """
    
    index = -1
    for word in for_cleaning:
        index += 1
        for el in punc_list:
            if el in word:
                no_punc_word = word.rstrip(el) #strip ending punctuation symbol 
                for_cleaning[index] = no_punc_word #replace word into for_cleaning without punctuation

    return for_cleaning


def remove_stopwords(to_clean, stop_w):
    """
    Remove stop words from a phrase.

    Parameters:
    to_clean (list): Phrase as a list
    stop_w (list): List of stop words

    Returns:
    list: Phrase without stop words
    """
    
    clean = [] #create list for phrase list without stop words
    for word in to_clean:
        if word not in stop_w: 
            clean.append(word)

    return clean


def test_for_digits(phrase):
    """
    Determine if the given phrase contains digits (True or False).

    Parameters:
    phrase (list): Search phrase as a list

    Returns:
    boolean: If phrase contains digits, then True.  Else, then False.
    """
    
    digit = False #set flag where "False" means no digits
    for el in phrase:
        if el.isdigit():
            digit = True
            break
        
    return digit


def main():
    print(__doc__) #display script info
	
    punctuation = [".", ",",":",";","!","?"]
    stop_words = get_stop_words() #obtain list of stop words 
    all_lowercase(stop_words) #convert stop words to lowercase
    choice1 = "Yes"
    while choice1 == "Yes":
        search_phrase = get_phrase(stop_words, punctuation) #obtain search query
        all_lowercase(search_phrase) #convert query to lowercase
        files = getFilesInDir() #obtain list of .txt filenames in directory
        choice2 = input("Do you want to search all .txt files in the current folder?  " \
                       "If so, type \"Yes\": ")
        if choice2 == "Yes":
            process_all(files, search_phrase, punctuation, stop_words)
        else:
            process_some(files, search_phrase, punctuation, stop_words)

        choice1 = input("Do you want to search again?  If so, type \"Yes\": ")


main()
