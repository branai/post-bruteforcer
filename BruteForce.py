import asyncio
import aiohttp
import math
import requests
from itertools import product

url = ""
badRes = ""
dataStr = ""
charNum = 0
charSet = ""
combos = []

#Set bruteforcing parameters from user supplied arguments
def setArgs(urlArg, respArg, dataArg, charNumArg, charSetArg):
	global url
	url = urlArg
	print("Target url: " + url)

	global badRes
	badRes = respArg
	print("Ignored responses: " + badRes)

	global dataStr
	dataStr = dataArg
	print("Request body format: " + dataStr)

	global charNum
	charNum = charNumArg
	print("Key length: " + str(charNum))

	global charSet
	charSet = charSetArg
	print("Character set: " + charSet)

	print("Generating cartesian product from options file...")
	global combos
	combos = list(product(charSet, repeat=charNum))
	print("Finished")

#Divide main set into subsets
def divideSets(divisor):
	#Total
	high = len(combos) #len(charSet) ** charNum
	if(divisor <= 0 or divisor > high):
		print("Invalid divisor. Exiting...")
		exit()
	increment = float(high)/divisor
	bounds = []
	for i in range(divisor):
		bounds.append(round(increment * i))
	if(bounds[len(bounds) - 1] != high):
		bounds.append(high)
	return bounds

async def attempt(varStr, session):
	#Put variable string into constant request body
	finalDataStr = formatToDataString(varStr)
	try:
		#Send post request to url with data
		async with session.post(url, data=finalDataStr) as resp:
			#Do not continue with this thread until response is recieved
			responseString = await resp.text()
			log = {
				finalDataStr: responseString,
				"check": responseString == badRes
			}
			print(str(log))
			#If the response is not the same as an ignored response
			if(log['check'] == False):
				print(finalDataStr + " returned different data than usual")
	#If server disconnected for whatever reason, continue with script
	except aiohttp.client_exceptions.ServerDisconnectedError:
		print("Server tried to disconnect for input: " + finalDataStr)

#Async'ly send requests using combos between given bounds
async def loopWithGivenBounds(beginBound, endBound):
	tasks = []
	print("Starting set " + str(beginBound) + " to " + str(endBound) + "...")
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
		for i in range(beginBound, endBound):
			task = asyncio.ensure_future(attempt("".join(combos[i]), session))
			tasks.append(task)
		for i in range(0, len(tasks)):
			await asyncio.gather(tasks[i])

def formatToDataString(string):
	return dataStr.format(string)

#FINICKEY Send a single test request
def singleRequest():
	print("===> OPTIONS Request <===\n")
	print(requests.options(url).text)
	print("\n======\n")
	print("===> GET Request <===\n")
	print(requests.get(url).text)
	print("\n======\n")
	print("===> HEAD Request <===\n")
	print(requests.head(url).text)
	print("\n======\n")
	print("===> POST Request <===\n")
	print(requests.post(url, data={}).text)
	print("\n======\n")
	print("===> PUT Request <===\n")
	print(requests.put(url, data={}).text)
	print("\n======\n")
	print("===> DELETE Request <===\n")
	print(requests.delete(url).text)
	print("\n======\n")

def runThisSet(beginBound, endBound):
	loop = asyncio.get_event_loop()
	future = asyncio.ensure_future(loopWithGivenBounds(beginBound, endBound))
	loop.run_until_complete(future)
