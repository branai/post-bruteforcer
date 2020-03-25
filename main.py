import argparse
import BruteForce as bf
import json

setBounds = []

parser = argparse.ArgumentParser()
parser.add_argument("filePath", help="JSON config file path for bruteforcer")
parser.add_argument("-s", "--single", help="Send a single sample request and print the response (FINICKEY)", action="store_true")
parser.add_argument("-d", "--divide-sets", help="Divide data set into x subsets and work through each one at a time", type=int)
args = parser.parse_args()

f = open(args.filePath)
jsonDat = json.load(f)

#Send user supplied arguments to main bruteforcing script
bf.setArgs(jsonDat['url'], jsonDat['invalidResponse'], jsonDat['data'], jsonDat['charNum'], jsonDat['charSet'])

if args.single:
	print("Sending single test request...")
	bf.singleRequest()

if(args.divide_sets == None):
	setBounds = bf.divideSets(1)
else:
	setBounds = bf.divideSets(args.divide_sets)

#Main loop
i = 0
while i < len(setBounds) - 1:
	#Try to run the combos between setBounds of indices i and i + 1
	try:
		bf.runThisSet(setBounds[i], setBounds[i + 1])
	#If anything fatal happens, restart the last subset
	except Exception as e:
		print(e)
		print("FORCED EXIT: RESTART")
		i -= 1
	i += 1
