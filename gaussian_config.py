#!/usr/bin/python

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
                if 'pop=' in option: 
                    keyword_split=option.split('=')
                    keywords.append('Population analysis')    
                if ('td(' or 'td=') in option:
                    keywords.append('TD-DFT')
                if 'freq' in option:
                    keywords.append('Frequency')
        #For per atom basis sets, the name is in the line previous to ****
        if line.rstrip()=='****':
            keywords.append(prev_line.rstrip())
            
        prev_line=line

    return keywords

if __name__=="__main__":

    g09_input='input_3.gjf'

    keywords=[]

    keywords=parse_route_section(g09_input,keywords)

    print keywords


