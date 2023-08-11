#! /home/nberi/miniconda3/bin/python3

import simple_colors
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('oligos')
parser.add_argument('oligo_entry_method')
args = parser.parse_args()

#return args.oligo_entry_method

def checkInserts():
    oligo_entry_method = args.oligo_entry_method
    # open your file with the sequenced plasmid and
    # read it into a string
    with open(args.filename) as querent:
        querent = list(querent)
        target_id = querent[0].lstrip('>').rstrip()
        target_seq = ''
        for field in querent[1:]:
            target_seq += field.rstrip()
  
        # return 'test'
        
        if args.oligo_entry_method == 'File':
           # print('File entry,9871,plasmid,35657')
            #return '[\'ggggg,yyyyy,aaaaa\n\']'
            with open(args.oligos) as oligos:
                #return 'test,test,tes,tes'
                for entry in oligos:
                    attributes = entry.split(',')
                    oligo_name = attributes[0].lstrip('>')
                    oligo_seq = attributes[1]
                    if target_seq.find(oligo_seq) > 0:
                        matching_seq = attributes[1]
                        attributes_lower = str(attributes[1]).lower()
                        lower_target = target_seq.lower()
                        target_seq_with_upper_oligo = lower_target.replace(attributes_lower, oligo_seq)
                        detailed_output = oligo_name + ',' + oligo_seq + ',' + target_id + ',' + target_seq_with_upper_oligo
                        print(detailed_output)
                    return detailed_output

        elif oligo_entry_method == 'Manual':
            #print('Manual entry,1,2,3')
            entry = args.oligos.split(',')
            #entry = ['name', 'AGG', 'CCT']
            #entry = list(entry)
            #print(type(entry))
            oligo_name = entry[0]
            oligo_seq = entry[1] 
            oligo_rev = entry[2]
            # find the squence in the target plasmid
            if target_seq.find(oligo_seq) > 0:
                #print('Oligo', oligo_name, '(', oligo_seq, ') found in', target_id) 
                matching_seq = entry[1]
                attributes_lower = str(entry[1]).lower()
                lower_target = target_seq.lower()
                target_seq_with_upper_oligo = lower_target.replace(attributes_lower, oligo_seq)
                #print(target_seq_with_upper_oligo)
                detailed_output = oligo_name + ',' + oligo_seq + ',' + target_id + ',' + target_seq_with_upper_oligo
                #print(detailed_output)
                return detailed_output
            elif target_seq.find(oligo_rev) > 0:
                matching_seq = entry[2]
                attributes_lower = str(entry[2]).lower()
                lower_target = target_seq.lower()
                target_seq_with_upper_oligo = lower_target.replace(attributes_lower, oligo_rev)
                detailed_output = oligo_name + ',' + oligo_rev + ',' + target_id + ',' + target_seq_with_upper_oligo
                return detailed_output
            else:
                return 'No match was found,,,'



g = checkInserts()
print(g)

# # Include the lines below if you want to also see which sequences were not found
# #		else:
# #			print('Search string', attributes[0], attributes[1], 'not found in file', target_id)
