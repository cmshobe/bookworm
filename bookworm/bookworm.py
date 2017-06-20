# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:00:50 2017

@author: Charlie

Program for storing and plotting information about reading habits: "bookworm"

IMPORTANT!! CLASS AND SUBFUNCTIONS SHOULD JUST DO PYTHON STUFF.

FUNCTIONS BELOW THE CLASS THAT CALL THE CLASS FNS ARE FOR PLAYING WITH CLICK
"""
import click #for command line interface
import pickle 
import matplotlib.pyplot as plt
import numpy as np
import csv

@click.command()
@click.argument('filename')
def start_new_booklist(filename):
    book_list = [] #empty list
    with open(filename + '.pkl', 'wb') as f:
        pickle.dump(book_list, f, pickle.HIGHEST_PROTOCOL)
    if len(book_list) > 0:
        with open(filename + '.txt', 'w') as txtfile:
            for item in book_list:
                print>>txtfile, item
        
@click.command()
@click.argument('filename')
@click.option('--method', type=click.Choice(['stdin', 'file']))
def add_new_book(filename, method):
    "Get and save info for a new book"
    if method == 'stdin':
        with open(filename + '.pkl', 'rb+') as f:
            book_list = pickle.load(f)
        title = click.prompt('Enter the book title', type = str)
        title_list = title.split()
        search_string = ''
        for word in title_list:
            search_string += word
            search_string += '+'
        click.launch('https://www.goodreads.com/search?q=' + search_string)
        author_last = click.prompt('Enter the author\'s LAST name', type = str)
        author_first = click.prompt('Enter the author\'s FIRST name', type = str)
        author_gender = click.prompt('Enter the author\'s gender (M/F/n)', type = str)
        author_race = click.prompt('Enter the author\'s race', type = str)
        author_nationality = click.prompt('Enter the author\'s nationality', type = str)
        publication_year = click.prompt('Enter the publication year', type = int)
        genre = click.prompt('Enter the book genre', type = str)
        rating = click.prompt('Enter your rating (1-10)', type = int)    
        #insert info provided above into a dictionary held in the book list
        book_list.insert(0, {'Title': title, 
                             'Author last name': author_last,
                             'Author first name': author_first,
                             'Author gender': author_gender,
                             'Author race': author_race,
                             'Author nationality': author_nationality,
                             'Publication year': publication_year,
                             'Genre': genre,
                             'Rating': rating})
    elif method == 'file':
        title = click.prompt('Enter the book title', type = str)
        title_list = title.split()
        search_string = ''
        for word in title_list:
            search_string += word
            search_string += '+'
        click.launch('https://www.goodreads.com/search?q=' + search_string)
        with open(filename + '.pkl', 'rb+') as f:
            book_list = pickle.load(f)
        temp_dict = {'Title:': title, 
                     'Author last name:': [],
                     'Author first name:': [],
                     'Author gender:': [],
                     'Author race:': [],
                     'Author nationality:': [],
                     'Publication year:': [],
                     'Genre:': [],
                     'Rating:': []}
        f = open('temp_book.txt', 'w+')
        for key in temp_dict:
            if key == 'Title:':
                f.write(key + ' ' + title + '\n')
            else:
                f.write(key + '\n')
        f.close()
        #bring up the template for the user to edit
        click.edit(filename='temp_book.txt')
        #now read the file and parse into the book entry dictionary
        input_dict = {}
        with open('temp_book.txt') as f:
            for line in f:
                (key, val) = line.split(':')
                input_dict[key] = val
        book_list.insert(0, input_dict)
                
    with open(filename + '.pkl', 'wb') as f:
        pickle.dump(book_list, f, pickle.HIGHEST_PROTOCOL)
    if len(book_list) > 0:
        with open(filename + '.txt', 'w') as txtfile:
            for item in book_list:
                print>>txtfile, item
                
@click.command()
@click.argument('filename')
@click.option('--plot_style', default='pie') #options: 'pie' and 'hist'
def plot_author_gender(filename, plot_style):
    with open(filename + '.pkl', 'rb') as f:
        book_list = pickle.load(f)
    men = 0.
    women = 0.
    other = 0.
    for book in book_list:
        gender = book['Author gender'].encode('ascii','ignore') #convert from 
        #...unicode to python string
        if gender == 'M':
            men += 1
        elif gender == 'F':
            women += 1
        elif gender == 'n':
            other += 1
    counts = np.array([men, women, other])
    labels = 'Men', 'Women', 'Other'
    fig, ax = plt.subplots()
    if plot_style == 'pie':
        ax.pie(counts, labels=labels)
        ax.axis('equal')
        fig.savefig('piechart.png')
        
@click.command()
@click.argument('filename')
def export_to_csv(filename):
    with open(filename + '.pkl', 'rb') as f:
        book_list = pickle.load(f)
    keys = book_list[0].keys()
    with open(filename + '.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(book_list)
        
#==============================================================================
# import pickle #for saving sictionary
# 
# class Bookworm(object):
#     def __init__(self):
#         "Initialize Bookworm"        
#         pass
# 
#     def start_new_booklist(self):
#         "Begin a new list of books"
#         #instantiate book list (a list of dictionaries)
#         #try to find saved dictionary
#         #otherwise, make a new one:
#         self.book_list = []
#     
#     def open_existing_booklist(self, name_to_open):
#         "Open an existing list of books"
#         with open(name_to_open + '_books.pkl', 'rb') as f:
#             self.book_list = pickle.load(f)
#             
#     def add_new_book(self):
#         "Get and save info for a new book"
#         title = click.prompt('Enter the book title:', type = str)
#         author_last = click.prompt('Enter the author\'s LAST name:', type = str)
#         author_first = click.prompt('Enter the author\'s FIRST name:', type = str)
#         author_gender = click.prompt('Enter the author\'s gender (M/F/n):', type = str)
#         author_race = click.prompt('Enter the author\'s race:', type = str)
#         author_nationality = click.prompt('Enter the author\'s nationality:', type = str)
#         publication_year = click.prompt('Enter the publication year:', type = str)
#         genre = click.prompt('Enter the book genre:', type = str)
#         rating = click.prompt('Enter your rating (1-10):', type = int)
#         
#         #insert info provided above into a dictionary held in the book list
#         self.book_list.insert(0, {'Title': title, 
#                                   'Author last name': author_last,
#                                   'Author first name': author_first,
#                                   'Author gender': author_gender,
#                                   'Author race': author_race,
#                                   'Author nationality': author_nationality,
#                                   'Publication year': publication_year,
#                                   'Genre': genre,
#                                   'Rating': rating})
#     #    def make_template_input_file(self):
#     #        "Make template text file with parameters blank"
#     #        
#     #    def open_template_file_in_editor(self):
#     #        "Open the text file in an editor to get user input"
#         
#     #    def export_info_to_csv(self):
#     #        "Export all attributes to a csv file"
#         
#     #    def make_pie_chart_author_gender(self):
#     #        "Make a pie chart of author gender"
#     
#     def save_book_dictionary(self,book_list_name, save_as_name):
#         "Save the dictionary, overwriting the old one, for reopening next time"
#         with open(save_as_name + '_books.pkl', 'wb') as f:
#==============================================================================
#            pickle.dump(book_list_name, f, pickle.HIGHEST_PROTOCOL)
            
