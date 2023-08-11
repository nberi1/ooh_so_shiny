# reverse-complement a string of nucleotides
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('query')
args = parser.parse_args()

#make dict of nucleotide pairs
myDict = {
'A':'T', 'T':'A', 'C':'G', 'G':'C'
}

# declare objects query, comp_seq, comp_list
query = args.query
comp_seq = ''
comp_list = []

# get complement of each nucleotide
for i in query:
	res = [val for key, val in myDict.items() if i in key]
	comp_seq += ''.join(res)

# reverse the complementary sequence
revcom = ''.join(reversed(comp_seq))

#print query and revcom sequences 
print("FWD:", query, "\nREV:", revcom)
