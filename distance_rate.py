def  distance_rate(dist):
#distance_rate:  We use a simple wireless channel model in which the user
#bit rate depends only on the distance to the AP.
 if (0 <= dist) and (dist <50):
 	rate = 11 #Mbps
 	return rate
 elif (50 <= dist) and (dist <80):
 	 rate = 5.5
 	 return rate
 elif (80 <= dist) and (dist <120):
 	rate = 2
 	return rate
 elif (120 <= dist) and (dist <150):   
 	rate = 1
 	return rate
 else:
            print("The user is out of coverage!")
