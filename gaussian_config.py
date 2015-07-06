#!/usr/bin/python

import glob
from StringIO import StringIO

def parse_route_section(gaussian_input_file,keywords):

    prev_line=''

    input_file=open(gaussian_input_file,'r')

    for line in input_file:
        #Look for route section
        if line[0]=='#':
            route_section=line.split()
            
            for option in route_section:
                #Relaxation keyword
                if option=='opt':
                    keywords.append('Relaxation')
                #Get the functional and basis set info
                #Need to omit internal parameters which have equal signs
                if '/' in option and '=' not in option:
                    keyword_split=option.split('/')
                    #Put the functional in the keyword list
                    keywords.append(keyword_split[0])
                    #Check the basis set
                    #If there are different basis functions per atom 
                    #They are at the bottom of the file
                    if keyword_split[1].lower()=='gen':
                        pass
                    #Otherwise stick it in
                    else:
                        keywords.append(keyword_split[1])
                #Get solvation info
                if 'SCRF=' in option:
                    keyword_split=option.split('=')
                    keywords.append(keyword_split[-1].rstrip(')'))
                #Check for population analysis
                if 'pop=' in option: 
                    keyword_split=option.split('=')
                    keywords.append('Population analysis')    
                #Check for TDDFT 
                if ('td(' or 'td=') in option:
                    keywords.append('TD-DFT')
                #Check for frequency of calclations
                if 'freq' in option:
                    keywords.append('Frequency')
        #For per atom basis sets, the name is in the line previous to ****
        if line.rstrip()=='****':
            keywords.append(prev_line.rstrip())
            
        prev_line=line

    return keywords

def write_config(keywords,files):
    config_file = StringIO()

    config_file.write('Description\n\n')
    config_file.write('Keywords\n')
    
    for keyword in keywords:
        config_file.write('    '+keyword+'\n')
    
    config_file.write('\ninputfiles\n')
    
    for file_name in files:
        config_file.write('    '+file_name+'\n')

    return config_file.getvalue()

def run():
    keywords_list=[]
    file_list=[]

    for g09_input in glob.glob("*.gjf"):
        keywords_list=parse_route_section(g09_input,keywords_list)
        file_list.append(g09_input)
    
    #Remove duplicate keywords
    keywords_list=list(set(keywords_list))
    
    return write_config(keywords_list,file_list)

if __name__=="__main__":    
    run()




