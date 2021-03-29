# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 20:25:00 2021

@author: erkan
"""

import random
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import re
#%%
st.title('Genetik Algoritma ile Yerleşim')

#%%
def create_starting_chromosome(number_of_function,number_of_day,coming_day):
   # Set up an initial array of all zeros
   chromosome = np.zeros((number_of_function, number_of_day))
   # Loop through each row (individual)
   for i in range(number_of_function):
       # Choose a random number of ones to create
   # Change the required number of zeros to ones
       chromosome[i,:coming_day[i]] = 1
       # Sfuffle row
       np.random.shuffle(chromosome[i])
       
   return chromosome
       


def create_starting_population(individuals,number_of_function,number_of_day,coming_day):
   population = []
   for i in range(individuals):
       chromosome = create_starting_chromosome(number_of_function,number_of_day,coming_day)
       population.append(chromosome)
   return population



def calculate_fitness_score(population,number_seat,capacity):
   fitness_scores = []
   for i in range(len(population)):
       chromosome = population[i]
       #fitness_score = np.sum((np.sum(chromosome*number_seat,axis=0)<=capacity))
       fitness_score_1 = np.sum(abs(np.sum(chromosome*number_seat,axis=0)-capacity))
       fitness_score_2 = np.std(np.sum(chromosome*number_seat,axis=0))
       fitness_score = fitness_score_1*fitness_score_2
       fitness_scores.append(fitness_score)
   return fitness_scores




def select_individual_by_tournament(population, fitness_scores):
   # Get population size
   population_size = len(fitness_scores)
   
   # Pick individuals for tournament
   fighter_1 = random.randint(0, population_size-1)
   fighter_2 = random.randint(0, population_size-1)
   
   # Get fitness score for each
   fighter_1_fitness = fitness_scores[fighter_1]
   fighter_2_fitness = fitness_scores[fighter_2]
   
   # Identify undividual with highest fitness
   # Fighter 1 will win if score are equal
   if fighter_1_fitness < fighter_2_fitness:
       winner = fighter_1
   else:
       winner = fighter_2
   
   # Return the chromsome of the winner
   return population[winner]



def breed_by_crossover(parent_1, parent_2):
   # Get length of chromosome
   chromosome_length = len(parent_1)
   
   # Pick crossover point, avoding ends of chromsome
   crossover_point = random.randint(1,chromosome_length-1)
   
   #print("Crossover noktası {} olarak belirlenmiştir.".format(crossover_point))
   
   # Create children. np.hstack joins two arrays
   child_1 = np.vstack((parent_1[0:crossover_point],
                       parent_2[crossover_point:]))
   
   child_2 = np.vstack((parent_2[0:crossover_point],
                       parent_1[crossover_point:]))
   
   # Return children
   return child_1, child_2



def randomly_mutate_population(population, mutation_probability):
   chromosome_size = len(population)
   gen_size = len(population[0])
   random_mutation_array_population = np.random.random(
       size=(chromosome_size))
   
   random_mutation_boolean_population = \
           random_mutation_array_population <= mutation_probability
   
   for i in range(len(random_mutation_boolean_population)):
       if random_mutation_boolean_population[i]:
           random_mutation_array_gene = np.random.random(
               size=(gen_size))

           random_mutation_boolean_gene = \
               random_mutation_array_gene <= mutation_probability

           for j in range(len(random_mutation_boolean_gene)):
               if random_mutation_boolean_gene[j]:
                   population[i][j] = np.zeros((5,))
                   gene = population[i][j]
                   gene[:coming_day[j]] = 1
                   np.random.shuffle(gene)
                   population[i][j] = gene


   # Return mutation population
   return population
#%%
lets_go = False
collect_numbers = lambda x : [int(i) for i in re.split("[^0-9]", x) if i != ""]
number_of_team = st.text_input('Lütfen katta bulunan takım sayısını giriniz.')
number_of_team = collect_numbers(number_of_team)
if len (number_of_team)!=0:
    number_of_team = number_of_team[0]

coming_day = st.text_input("Lütfen sırasıyla takımların gelmeleri gereken gün sayılarını virgül ile ayırarak giriniz.")
coming_day = collect_numbers(coming_day)
coming_day = np.array(coming_day)


number_of_seat = st.text_input("Lütfen sırasıyla takımların koltuk sayılarını virgül ile ayırarak giriniz.")
number_of_seat = collect_numbers(number_of_seat)
number_of_seat = np.array(number_of_seat)
if len(number_of_seat)!=0:
    capacity = np.ceil(np.sum(number_of_seat*coming_day)/5)
    st.write('Uygun bir çözümün bulunabilmesi için gerekli kapasite miktarı:',capacity)
    lets_go = True
number_of_seat = number_of_seat.reshape((len(number_of_seat),1))




#%%

if lets_go:
    population_size = 100
    maximum_generation = 30
    number_of_day = 5
    best_score_progress = [] # Tracks progress
    best_score_parameters = []
    # Create starting population
    population = create_starting_population(population_size,number_of_team,number_of_day,coming_day)
    
    # Display best score in starting population
    fitness_scores = calculate_fitness_score(population,number_of_seat,capacity)
    best_score = np.min(fitness_scores)
    best_score_parameter = population[fitness_scores.index(best_score)]
    
    # Add starting best score to progress tracker
    best_score_progress.append(best_score)
    best_score_parameters.append(best_score_parameter)
    
    
    # Now we'll go through the generations of genetic algorithm
    for generation in range(maximum_generation):
       # Create an empty list for new population
       new_population = []
    
       # Create new popualtion generating two children at a time
       for i in range(int(population_size/2)):
           parent_1 = select_individual_by_tournament(population, fitness_scores)
           parent_2 = select_individual_by_tournament(population, fitness_scores)
           child_1, child_2 = breed_by_crossover(parent_1, parent_2)
           new_population.append(child_1)
           new_population.append(child_2)
    
       # Replace the old population with the new one
       population = np.array(new_population)
    
       # Apply mutation
       mutation_rate = 0.1
       population = randomly_mutate_population(population, mutation_rate)
    
       # Score best solution, and add to tracker
       fitness_scores =  calculate_fitness_score(population,number_of_seat,capacity)
      
       best_score = np.min(fitness_scores)
       best_score_parameter = population[fitness_scores.index(best_score)]
       best_score_progress.append(best_score)
       best_score_parameters.append(best_score_parameter)
    
    # GA has completed required generation
    final_result_chromosome = best_score_parameters[best_score_progress.index(np.min(best_score_progress))]
    final_result_chromosome_df = pd.DataFrame(final_result_chromosome,columns=["Pzt","Salı","Çarş","Perş","Cuma"])
    st.write("Optimum çözüm:",final_result_chromosome_df)
    
    yerlesim_df = pd.DataFrame(final_result_chromosome*number_of_seat,columns=["Pzt","Salı","Çarş","Perş","Cuma"])
    st.write("Optimum çözüm sonrası yerleşim:",yerlesim_df)
    
    
    total_capacity_usage = np.sum(final_result_chromosome*number_of_seat,axis=0).reshape((5,1)).T
    total_capacity_usage_df = pd.DataFrame(total_capacity_usage,columns=["Pzt","Salı","Çarş","Perş","Cuma"],index =['Kapasite Kullanımı'])
    
    
    st.write("Optimum çözüm sonrası toplam kapasite kullanımı:",total_capacity_usage_df)
    


