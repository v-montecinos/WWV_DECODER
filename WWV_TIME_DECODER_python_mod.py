# this module will be imported in the into your flowgraph

import sys
import time
from datetime import datetime, timedelta, date



t_start     = 0     # Rising edge timer
t_stop      = 0     # Falling edge timer
flag        = 0     # Flag
detected    = 0     # Mark pulse detected flag
mark_t      = 0     # Duration of mark
space_t     = 0     # Duration of space
sync        = 0     # Sync condition flag
error       = 1     # Error flag
bit_val     = 1     # 0 for 0, 1 for 1 & 2 for Position identifiers
counter     = 1     # Pulse counter

minutes     = 0
hours       = 0
days        = 0
unit_year   = 0
ten_year    = 0

year        = 0

output_str  = "No time signal decoded yet!"


def www_decoder(prob_level):
    global t_start,t_stop,flag,detected,mark_t,space_t,sync,error,bit_val,counter,minutes,hours,unit_year,ten_year,year,days,output_str,res, res_date

#**********************************************************************************************************************
# Wait until the "Hole" or preamble condition is detected (1200 ms of silence) if occur the sync flag is True
#**********************************************************************************************************************

    if (sync == 0):
    
            if (prob_level == 0 and flag == 0):                     # Detect the falling edge and get the current time
                    flag = 1
                    t_start = time.time()
                    
            if (prob_level == 1 and flag == 1):                     # Detect the rising edge and get the current time
                    flag = 0
                    t_stop = time.time()
                    detected = 1
            
            if (detected == 1):                                     # If a whole pulse occur calc the pulse duration
                    space_t = round(t_stop - t_start, 3)*1000       # Space duration in ms
                    detected = 0
                    #print ("space t:",space_t," ms")               # for debug porpuse
                    
                    if (space_t in range(1100,1300)):               # Range detection for "Hole" (1200 ms)
                        print ("\n")
                        print ("Start Sync condition detected\n")
                        sync = 1
                        
#**********************************************************************************************************************
# If sync flag is True,  wait until a whole pulse occur and calc the pulse duration and change detected to True
#**********************************************************************************************************************

    if (sync == 1):
    
            if (prob_level == 1 and flag == 0):                     # Detect the rising edge and get the current time
                 flag = 1
                 t_start = time.time()
                 
            if (prob_level == 0 and flag == 1):                     # Detect the falling edge and get the current time
                 flag = 0
                 t_stop = time.time()
                 detected = 1
                 
#**********************************************************************************************************************
# If detected is True, evaluate range detection for 0, 1 o Px
#**********************************************************************************************************************

    if (detected == 1):
    
                mark_t = round(t_stop - t_start, 3)*1000            # Pulse duration in ms
                #print ("mark t:",mark_t," ms")                     # for debug porpuse
                detected = 0
                error = 1
                        
                if (mark_t in range(150,250)):                      # Range detection for os (200ms)
                    bit_val = 0
                    error   = 0

                if (mark_t in range(450,550)):                      # Range detection for 1s (500ms)
                    bit_val = 1
                    error   = 0

                if (mark_t in range(750,850)):                      # Range detection for Px (800ms)
                    bit_val = 2
                    error   = 0

#**********************************************************************************************************************
# If no error during the range detection continue with the decoding if not wait until de next sync condition
#**********************************************************************************************************************

                if (error == 1):
                    sync = 0
                    print ("Range detection error!, waiting until the next sync\n")
                    
  #**********************************************************************************************************************
  # BCD decode for the moment only hours, minutes and year
  #**********************************************************************************************************************
                else:
                    counter = counter + 1

                    if (counter == 5):
                        unit_year = unit_year +  1 * bit_val        # Decode units of year
                    elif (counter == 6):
                        unit_year = unit_year +  2 * bit_val
                    elif (counter == 7):
                        unit_year = unit_year +  4 * bit_val
                    elif (counter == 8):
                        unit_year = unit_year +  8 * bit_val
                        

                    elif (counter == 11):                           # Decode minutes
                        minutes = minutes +  1 * bit_val
                    elif (counter == 12):
                        minutes = minutes +  2 * bit_val
                    elif (counter == 13):
                        minutes = minutes +  4 * bit_val
                    elif (counter == 14):
                        minutes = minutes +  8 * bit_val
                    elif (counter == 16):
                        minutes = minutes +  10 * bit_val
                    elif (counter == 17):
                        minutes = minutes +  20 * bit_val
                    elif (counter == 18):
                        minutes = minutes +  40 * bit_val
                        
                    elif (counter == 21):                           # Decode hours
                        hours = hours +  1 * bit_val
                    elif (counter == 22):
                        hours = hours +  2 * bit_val
                    elif (counter == 23):
                        hours = hours +  4 * bit_val
                    elif (counter == 24):
                        hours = hours +  8 * bit_val
                    elif (counter == 26):
                        hours = hours +  10 * bit_val
                    elif (counter == 27):
                        hours = hours +  20 * bit_val
                        
                    elif (counter == 31):                           # Decode days
                        days = days +  1 * bit_val
                    elif (counter == 32):
                        days = days +  2 * bit_val
                    elif (counter == 33):
                        days = days +  4 * bit_val
                    elif (counter == 34):
                        days = days +  8 * bit_val
                    elif (counter == 36):
                        days = days +  10 * bit_val                       
                    elif (counter == 37):
                        days = days +  20 * bit_val
                    elif (counter == 38):
                        days = days +  40 * bit_val    
                    elif (counter == 39):
                        days = days +  80 * bit_val
                    elif (counter == 41):
                        days = days +  100 * bit_val                            
                    elif (counter == 42):
                        days = days +  200 * bit_val                               
                        
                        
                                            
                        

                    elif (counter == 52):                           # Decode tens of year
                        ten_year = ten_year +  10 * bit_val
                    elif (counter == 53):
                        ten_year = ten_year +  20 * bit_val
                    elif (counter == 54):
                        ten_year = ten_year +  40 * bit_val
                    elif (counter == 55):
                        ten_year = ten_year +  80 * bit_val
                        
#**********************************************************************************************************************
# Data formating and extra validate
#**********************************************************************************************************************
                    
                    elif (counter == 60):
                        minutes = minutes + 1                       # Remenber add 1 minute because the decode finish
                                                                    # before the next decode
                        if (minutes == 60):
                            minutes = 0
                            hours = hours +1
                        if (hours == 24):
                            hours = 0
                        
                        year = 2000 + ten_year + unit_year
                                        
                        
                        if (minutes in range (0,59) and hours in range (0,23)):
                            
                            res_date = date(year, 1, 1) + timedelta(days=days - 1)          #calculate the diference between 1-1-year
                        
                            res = res_date.strftime("%m-%d-%Y")
                        
                        
                            output_str = str(hours) + ":" + str(minutes) + "  UTC     " + str(res)
                        
                            print (output_str)
                            
                             
                        else:
                            print ("Error decoding, waiting until the next sync\n")
                            sync = 0
                            


#**********************************************************************************************************************
# Reset counter and data before the next sync condition
#**********************************************************************************************************************
                        sync      = 0
                        counter   = 1
                        minutes   = 0
                        hours     = 0
                        days      = 0
                        unit_year = 0
                        ten_year  = 0
                        year      = 0
                        
                        

            
    return output_str
    
