# load an html page as txt
# grab line 3280 (counting from 0)
# extract from <!-- to -->
# save this as a json file


import codecs
import os
import json

def OpenJSON(ToOpen):
    if os.path.isfile(ToOpen) and os.path.getsize(ToOpen) > 0:
        with open(ToOpen) as data_file:    
            return json.load(data_file)
    else:
        return 0

#html to json
localdir = 'html/'
jsondir = 'json/'

for html_file in os.listdir(localdir):
    

    #open this file for reading
    text_object = codecs.open((localdir + html_file),'r','utf-8')
    text_lines = text_object.readlines()

    # luckily, the part that we need from these pages is always on the same line
    key_part = text_lines[3280]
    start_point = key_part.index('<!--') + 4   # offset for length of <!--
    end_point = key_part.index('-->')          # no offset needed
    key_part = key_part[start_point:end_point]

    # change file extension to .json
    out_filename = html_file.split('.')[0] + '.json'

    print("saving",out_filename, end=', ')
    with open(jsondir + out_filename, "w") as out_file:
        print(key_part, file=out_file)
    
    # pretty print the json and save it
    print("converting to pretty json")
    a_json_object = OpenJSON(jsondir + out_filename)
    json.dump(a_json_object,open(jsondir + out_filename, "w"), indent=4)





