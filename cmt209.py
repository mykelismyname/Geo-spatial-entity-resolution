import pandas as plib
import numpy as num
import io
import jellyfish as jf
from haversine import haversine as hv
from math import *


def main():
    try:
        #creates a dataframe that reads into text file
        cmtTd = plib.read_table('TrainingData.txt');
        
	#set column labeled Id1 to be the index of dataFrame and converts data frame to a csv file
	cmtTd.set_index('Id1', inplace=True)
        cmtTd.to_csv('matchCmtPlaces_file.csv')
        
	#convert new csv file into list 
	newcmtTd = plib.read_csv('matchCmtPlaces_file.csv')
	matchCmtPlaces_Array = num.array(newcmtTd)
        matchCmtPlaces_Array_List = matchCmtPlaces_Array.tolist()

	#create empty lists that will hold the levenshtein distance as per comparison of each pair of data items in the list
	matched_Names = []
	hammed_distance = []
	damerau_distance = []
	jaccard_sim = []
	distances = []
	decision = []
	
	
	#compare the Names i.e (Name1 - item[1] and Name2-item[7]), Latitudes(Latitude1 and Latitude2) and Longitudes using the levenshtein edit distance
	for item in matchCmtPlaces_Array_List:         
	    match_Names = jf.levenshtein_distance(unicode(str(item[1])), unicode(str(item[7])))
	    hm_distance = jf.hamming_distance(unicode(str(item[1])), unicode(str(item[7])))
	    dm_distance = jf.damerau_levenshtein_distance(unicode(str(item[1])), unicode(str(item[7])))
	    #convert each name into a list of characters to compute jaccard similarity
	    name1 = list(item[1])
	    name2 = list(item[7])
	    
	    intersection_cardinality = len(set.intersection(*[set(name1), set(name2)]))
	    union_cardinality = len(set.union(*[set(name1), set(name2)]))
	     
            place_record_1 = (item[4], item[5])
	    place_record_2 = (item[10], item[11])
	    distanceBtnPlaces = hv(place_record_1, place_record_2) 

   	    matched_Names.append(match_Names)
	    jaccard_sim.append(intersection_cardinality/float(union_cardinality))
	    hammed_distance.append(hm_distance)
	    damerau_distance.append(dm_distance)
	    distances.append(distanceBtnPlaces)
	    decision.append(item[12])
	    
	    
	match_output_dataFrame = plib.DataFrame({'Levenshtein-distance': matched_Names,
						 'damerau_distance':damerau_distance,
						 'Jaccard-similarity': jaccard_sim,
						 'Hamming-distance': hammed_distance,
		   				 'Haversine-distance': distances,
						 'decision': decision}
		  				 )	
	match_output_dataFrame.set_index('Levenshtein-distance', inplace=True)
	match_output_dataFrame.to_csv('final_output_file.csv')
	print (match_output_dataFrame)
            
    except (IOError, ValueError, TypeError) as e:
        print (e)
    

if __name__=="__main__":
    main()

