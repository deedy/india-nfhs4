
1-fetch-pdfs:
Reads from url_list.txt, which was manually retrieved with javascript on the NFHS-4 website. This was the first batch of the data. It fetches the pdfs and stores it in the data/

1-fetch-pdfs-2:
Reads from url_list2.txt and does the same as above.

2-extract-pdfs:
Reads the pdfs and attempts to extract the data from it textually into a csv. It may fail, and may need more special casing (that I've removed) for certain pdfs. Particularly, my logic failed with Gujarat Junagadh and Odisha's Debagarh - which I did manually. It writes it to india-nfh4-final.csv.

That csv file is fully compiled and stored in parsed/india-nfhs4.csv.

3-plot-basic-maps:
Has helper functions to map India on a national, state, district and the finest - the taluk level. 

3-plot-data:
Reads parsed/india-nfhs4.csv and the district shape file from IND_adm_shp/IND_adm2.shp (and it's metadata files - shx, and dbf), performs the correct mappings between names and districts and uses some helper functions to save a map india.png. There are a bunch of helper functions for plotting in the file, and you can add your own or modify the call to 
get_color_and_alpha_for_women_high_blood_sugar_82 in the file. 

This code is obviously very hacky and does not follow any standards nor is particularly easy to use. Please contact me with any questions. I'm unlikely to be maintaining this in the future. 
