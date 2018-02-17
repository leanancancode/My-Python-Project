# -*- coding: utf-8 -*-
# Names: Leana Nakkour and Deelyn Cheng
# CSE 160, Section AC
# HW 7 Part 2

import csv
from operator import itemgetter
import matplotlib.pyplot as plt


def read_csv(filename, era): 
    ''' Given a filename and int era (1970 for 70s, 1980 for 80s, ...), function
    reads in the csv dataset from the filename and returns a list of dictionaries
    for each movie that was produced within that decade where Year, Title, 
    Actor, Actress, Genre, Awards, Director, and Popularity are mapped to their 
    designated values
    '''
    input = open(filename)
    decade = []
    for line in input:
        data = line.split(";")
        year = int(data[0])
        if era <= year < era + 9: 
            film_dict = dict()
            film_dict["Year"] = year
            film_dict["Title"] = data[2]
            film_dict["Genre"] = data[3]
            film_dict["Actor"] = full_name(data[4])
            film_dict["Actress"] = full_name(data[5])
            film_dict["Director"] = full_name(data[6])
            if data[7] != "":
                film_dict["Popularity"] = int(data[7])
            else:
                film_dict["Popularity"] = None
            if data[8] == "No":        
                film_dict["Awards"] = False
            else:
                film_dict["Awards"] = True      
            decade.append(film_dict)
    input.close()
    return decade

def full_name(lastfirst):
    ''' Function takes in a string in the format "Last name, First name" 
    and returns the full name in order of the first then last as a string
    Special case: If the name passed in is a single word, returns that 
    name as a string
    '''
    name = lastfirst.split(",")
    if len(name) == 1:
        if name[0] == "":
            return None
        else:
            return str(name[0])
    else: 
        return str(name[1] + " " + name[0])
     
def genre_specific_movies(list_of_films, genre):
    ''' Given a list of dictionaries of movies and a genre, returns a new
    list of dictionaries made up of movies, from the given list, of the given genre
    '''
    films_of_genre = []
    for index in range(len(list_of_films)):
        curr_film = list_of_films[index]
        curr_genre = curr_film["Genre"]
        if curr_genre == genre:
            films_of_genre.append(curr_film)  
    return films_of_genre                 

def count_occurrences(list_of_films, category):
    ''' Given a list of dictionaries of movies in order of greatest to least 
    popularity, returns a new dictionary mapping the values of the given category
    (Actor, Actress, Genre...) to the number of times they are featured in the 
    list of movies
    '''
    seen = set()
    occurrences = dict()
    for i in range(len(list_of_films)):
        curr_dict = list_of_films[i]
        value = curr_dict[category]
        if value != None:   
            if value not in seen:
                seen.add(value)
                occurrences[value] = 1
            else:
                occurrences[value] += 1
    return occurrences 

def cast_occurrences(list_of_films):
    ''' Given a list of films, returns a dictionary of every actor and actress
    mapped to the number of times they appear in the casting for a movie in the 
    list 
    '''
    cast = dict()
    actor_dict = count_occurrences(list_of_films, "Actor")
    actress_dict = count_occurrences(list_of_films, "Actress")
    for actor in actor_dict:
        cast[actor] = actor_dict[actor] #make a key for actor and map to value
    for actress in actress_dict:
        cast[actress] = actress_dict[actress] #make key for actress and map to value                
    return cast    
   
def most_recurring(occurrences):
    ''' Given a dictionary of a category (actors, actresses, genre...) mapped 
    to their number of occurrences in the list of popular films for a 
    particular era, function returns a list of the most recurring (max)
    element in that category
    Special Case: if the most recurring element's occurrence value = 1, then there
    is no reccurrence of actors or actresses in the particular decade for that genre
    '''
    sorted_list = sorted(occurrences.items(), key = itemgetter(1), reverse = True)
    most_recurred = []
    # Because the list is sorted, we can assume that the first item is the max 
    element = sorted_list[0]
    max = element[1]
    if max != 1:    
        for index in range(len(sorted_list)):
            current = sorted_list[index]
            occurrence = current[1]
            if occurrence == max:
                most_recurred.append(current[0])
        return most_recurred 
    else:
        print "No recurring Actors or Actresses in this decade of popular films"
        ## return [] ## changed at 9:36 PM to the statement below
        return most_recurred      

def most_popular_rating(list_of_films):
    ''' Given a list of dictionaries of films from a particular decade, the
    function organizes the films by popularity and returns a new list of 
    dictionaries of the films in order of rating
    '''
    copy = list_of_films[:]
    for index in range(len(list_of_films)):
        current = list_of_films[index]
        if current["Popularity"] == None:
            copy.remove(current)
    result = sorted(copy, key=itemgetter('Popularity'), reverse = True)
    if len(result) < 10:
        return result
    else:
        return result[:10]
              
def most_popular_genre(list_of_films):
    ''' Given a list of dictionaries of movies in order of greatest to least 
    popularity, function returns a list of the most popular genres of that era
    '''
    genre_dict = count_occurrences(list_of_films, "Genre")
    most_reccurring_genre = most_recurring(genre_dict)
    return most_reccurring_genre                 
                                                
def most_popular_cast(list_of_films):
    ''' Given a list of dictionaries of movies in order of greatest to least 
    popularity, returns a list of actor(s) and actress(es) most reccurring in the
    list of movies
    '''
    cast_counts = cast_occurrences(list_of_films)         
    actors_actresses = most_recurring(cast_counts)   
    return actors_actresses          
            
def decade_appearances(filename, person):
    ''' Given a dataset of films and string value, Actor/Actress/Director name,
    function calculates how many times the given value/name appears in each 
    decade and returns a list of their occurrences for each year
    '''
    decades = [1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990]
    #for member in range(len(recurring_cast)):
    #    person = recurring_cast[member]
    occurrences = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for year in range(len(decades)):
        films = read_csv(filename, decades[year])
        for index in range(len(films)):
            curr_film = films[index]
            if curr_film["Actress"] == person:
                occurrences[year] += 1
            if curr_film["Actor"] == person:
                occurrences[year] += 1
        #list_occur.append(occurrences)
    return occurrences      
        
def max_occurrences_in_decades(list_occurrences, person):
    ''' Given a list of the given person's occurrences over the decades,
    function returns a dictionary mapping that person to the year they 
    frequently appear the most in
    '''       
    decades = [1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990]
    era_appearances = dict()
    max = None
    era = None
    for i in range(len(list_occurrences)):    
        if max == None:
            max = list_occurrences[i]
        elif list_occurrences[i] > max:
            max = list_occurrences[i]
            era = decades[i]
        era_appearances[person] = era
    return era_appearances                                       

def plotting_decades_of_star_occurrences(filename, recurring_cast):
    ''' Given a filename of film data and a list of recurring actors and 
    actresses, a line graph is outputted of the person's occurrences over the 
    decades from 1910 to 1990
    '''
    plt.clf() 
    plt.title("Reccurring Actors/Actresses Over the Decades")
    plt.ylabel("Occurrences")
    plt.xlabel("Decades")
    decades = [1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990]
    if len(recurring_cast) != 0:
        for index in range(len(recurring_cast)):    
            person = recurring_cast[index]
            person_occurrences = decade_appearances(filename, person)
            plt.plot(decades, person_occurrences, label = person)
        plt.legend()
        plt.show()     

def plot_bar_graph(era, counts, title, ylabel, xlabel, color):
    ''' Given a decade and dictionary of category specific keys mapped to their
    counted occurrences in the given decade, string Title, y-axis label, and x-axis label
    function outputs a bar graph of each key in the dictionary and their 
    counted occurrences in films for that decade
    '''
    plt.clf()
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.bar(range(len(counts)), counts.values(), width = 1/1.5, align = 'center', color = color)
    plt.xticks(range(len(counts)), counts.keys(), rotation = 90)
    plt.legend()
    plt.show()    

def film_success(film_list, genre):
    ''' Given a list of dictionaries of films from a particular era and genre,
    function prints whether or not the most popular film is an award winner. 
    If so, prints the director's other award winning movies and
    total number of awards
    '''
    movies = genre_specific_movies(film_list, genre) 
    popularity_list = most_popular_rating(movies)
    most_popular_film = popularity_list[0]
    award_winner = most_popular_film["Awards"]
    if award_winner == False:
        print "According to the graphs, " + most_popular_film['Title'],
        print "is not an award winner"
    else:
        director = most_popular_film["Director"]
        director_movies = director_success(film_list, director)
        print director + "'s award winning movies: ", str(director_movies)
        print "Total Awards Won:", len(director_movies)
        
        
def director_success(film_list, director):
    ''' Given a list of dictionaries of films and a string director name,
    Returns a list of award winning movies for the given director, if any  
    '''
    result = []
    for index in range(len(film_list)):
        film = film_list[index]
        if film["Director"] != None:
            if film["Director"] == director:     
                if film["Awards"] == True:
                    result.append(film["Title"])
    return result
    
def extract_film_data(film_title, film_list):
    ''' Given a specific film and a list of dictionaries of films, both from the
    same decade, returns a dictionary mapping Title, Genre, Year, Actor, Actress,
    and Director, to their particular values for a single movie.
    '''
    film_data = dict()
    for i in range(len(film_list)):
        film = film_list[i]
        if film["Title"] == film_title:
            film_data["Title"] = film_title
            film_data["Genre"] = film["Genre"] 
            film_data["Year"] = film["Year"]
            film_data["Actor"] = film["Actor"]
            film_data["Actress"] = film["Actress"]
            film_data["Director"] = film["Director"]

    return film_data

def get_era(year):
    '''Function takes in an integer value year, (1928, 1932, etc..) and returns
    the era in which that year took place (if 1928, returns 1920)
    '''
    decades = [1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990]
    era = year / 10 % 10
    era = decades[era - 1]
    return era
    
def bar_plot_genre_trends_based_off_film(film_title, film_list):
    ''' Given a film_title and a list of dictionaries of films,
    function plots a bar chart of all the genre occurrences in the particular
    era that the given film_title was produced
    '''
    film_data = extract_film_data(film_title, film_list)
    genre_counts = count_occurrences(film_list, 'Genre')
    year = get_era(film_data['Year'])

    title = "Genre Occurrences in the " + str(year) +"s"
    yaxis = "Occurrences"
    xaxis = "Genres"
    
    plot_bar_graph(year, genre_counts, title, yaxis, xaxis, 'pink')

def bar_plot_director_movie_genres(film_title, film_list):
    ''' Given a film title and a list of dictionaries of films, the funciton
    plots a bar chart of all the films the Director from the given film_title 
    has produced in the era of the given film_title, where each bar represents
    a genre
    '''
    film_data = extract_film_data(film_title, film_list)
    director = film_data['Director']
    director_films =[]
    for i in range(len(film_list)):
        film = film_list[i]
        film_director = film['Director']
        if film_director == director:
            director_films.append(film)
    director_film_counts = count_occurrences(director_films, 'Genre')

    year = get_era(film_data['Year'])
    title = "Genres of Movies by" + director + " in the " + str(year) + "s"
    ylabel = "Number of Movies"
    xlabel = "Genres"
    plot_bar_graph(year, director_film_counts, title, ylabel, xlabel, 'pink')


def film_reflection(film_title, film_list):
    ''' Given a film title that matches the title within the data case-sensitively
    and a list of dictionaries of films, function prints if the movie is a 
    reflection of the most popular genre in that era and how many reccurrences 
    the director of the given film has made in the movies of that popular genre
    '''
    reflection = None
    film_data = extract_film_data(film_title, film_list)
    popular_genres = most_popular_genre(read_csv("film_dataset.csv", film_data['Year']))
    if film_data['Genre'] == popular_genres[0]:
        reflection = True
        print "According to the graph, the movie " + film_title + "'s genre is a", 
        print "reflection of the popular genre in the year " + str(film_data['Year'])
        if reflection == True:
            movies = genre_specific_movies(film_list, film_data['Genre']) 
            occurrence = 0
            if film_data["Director"] != None:
                for m in range(len(movies)):
                    curr = movies[m] 
                    if curr["Director"] == film_data["Director"]:
                        occurrence += 1
                print "Director" + film_data["Director"] + " recurrs in the",  
                print "popular genre movies",
                print str(occurrence) + " times"
            else:
                print "There is no Director associated with this film."
    else:
        print "According to the graph, the movie " + film_title + "'s genre is",
        print "NOT a reflection of the popular genre"

def print_cast(cast):
    ''' Function takes in a list of actors and actresses
    and prints the most recurring actors and actresses or if there
    weren't any at all
    '''
  
    if len(cast) == 0:
        print "There are no recurring actors/actresses in this decade of films"
    for member in range(len(cast)):
         print cast[member]
                
            
def print_dec_app(appearances):
    ''' Function takes in a dictionary of actors/actresses mapped to the year
    they most frequented and prints them out
    '''
    for key in appearances.keys():
        print "According to the graph," + key + " appears most in the year",
        print str(appearances[key])

def research_question_one(filename, era, genre, recurring_cast):
    ''' Given a filename, era, genre, and list of people who most often recurred
    in the particular genre and era given. Function restates/prints the 
    original research question and prints the output results to the question
    '''
    print "Research Question One: Which actors or actresses are more consistently" 
    print "associated with the most popular films in a certain genre, and which" 
    print "decade do they appear the most in?"
    print "Given the year: " + str(era) + ", and the genre: " + genre
    print "According to the bar chart, the most recurring actor(s)/actress(es)", 
    print "of this time, in this genre are:"
    print_cast(recurring_cast) 
    appearances = dict()
    for person in range(len(recurring_cast)):
        occurrences = decade_appearances(filename, recurring_cast[person])
        max_occur = max_occurrences_in_decades(occurrences, recurring_cast[person])
        appearances[recurring_cast[person]] = max_occur[recurring_cast[person]]                             
    return appearances
                          

def research_question_two(era, genre, list_of_films):
    ''' Given an era, genre, and list of dictionaries of films, function
    restates/prints the particular research question and ouputs the results
    of the question in print statements
    '''
    print "Research Question Two: Given a particular genre and era, is the"
    print "most popular movie within that category and year an award winner,"
    print "and if so, is the director of the film correlated to its success?"
    print "(Has the director made other award winning movies? How many?)"
    print "Given the year: " + str(era) + ", and the genre: " + genre
    
    popular_films = most_popular_rating(list_of_films)
    most_pop_film = popular_films[0]
    print "The most popular movie was " + most_pop_film['Title']
    
    film_success(list_of_films, genre)
    print 

def plot_film_popularity(era, most_popular_genre_films):
    ''' Given an era and list of dictionaries of popular movies from a
    specific genre, function plots a bar chart based on the popularity of 
    each film and whether or not the films are awards winners
    '''
    ylabel = "Popularity Rating"
    xlabel = "Films"
    ratings_no_awards = dict()
    ratings_awards = dict()
    for index in range(len(most_popular_genre_films)):
        film = most_popular_genre_films[index]
        popularity = film['Popularity']
        if film['Awards']:
            ratings_awards[film['Title']] = popularity
        else:
            ratings_no_awards[film['Title']] = popularity
    
    ## PLOT NON AWARD WINNERS
    #if len(ratings_no_awards) != 0:
        title = "Popularity Ratings of Non Award Winning Films in the " + str(era) +"s"
        #plot_bar_graph(era, ratings_no_awards, title, ylabel, xlabel, 'red')
    
    ## PLOT AWARD WINNERS
    if len(ratings_awards) != 0:
        title = "Popularity Ratings of Award Winning Films in the " + str(era) +"s"
        plot_bar_graph(era, ratings_awards, title, ylabel, xlabel, 'cyan')
    else: 
        print "There were no award winners in this list of popular films"
        
def research_question_three(film_title, list_of_films): 
    ''' Given a film title and a list of dictionaries of films, both of the same
    era, function prints/restates the research question and prints the result
    of the particular research question.
    '''
    print "Research Question Three: Given a particular film, is that film’s"
    print "genre a reflection of the most recurring genre of the era in which" 
    print "it was produced? If so, is the director of the given film frequented"
    print "in that recurring genre during that era? How does that contribute to" 
    print "the most recurring genre in that decade?"
    film_data = extract_film_data(film_title, list_of_films)
    year = get_era(film_data['Year'])
    print
    print film_title +"'s genre is " + film_data['Genre']
    print "Based on " + film_title + "'s genre, the bar chart illustrates the"
    print "occurrences of each genre in the " + str(year) + "s"
    

##### MAIN STARTS HERE #######
def main(): 
    # leave this as is
    era = 1920
    filename = "film_dataset.csv"
    genre = "Drama"
    films = read_csv(filename, era)
    
    ## RESEARCH QUESTION ONE
    popular = most_popular_rating(films)
    cast_counts = cast_occurrences(popular)
    popular_cast = most_popular_cast(popular)
    #appearances = research_question_one(filename, era, genre, popular_cast)
    #plot_bar_graph(era, cast_counts, "Cast Occurrences in the " + str(era) + "'s", "Occurrences", "Actors/Actresses", 'pink')
    #plotting_decades_of_star_occurrences(filename, popular_cast)
    #print_dec_app(appearances)
    print
    
    
    ## RESEARCH QUESTION TWO
    genre_spec = genre_specific_movies(films, genre)
    popular = most_popular_rating(genre_spec)
    #research_question_two(era, genre, popular)
    #plot_film_popularity(era, popular)


    ## RESEARCH QUESTION THREE 
    ## 1920s: 'Woman of Affairs', 1940s: 'Gaslight'
    film_title = 'Woman of Affairs'
    research_question_three(film_title, films)
    bar_plot_genre_trends_based_off_film(film_title, films)
    #film_reflection(film_title, films)
    #bar_plot_director_movie_genres(film_title, films)
    
    
if __name__ == "__main__":
    main()

