#!/usr/bin/env python3

from revChatGPT.V3 import Chatbot
import json
import subprocess

debug = False

#debug = True

"""
Opens the system_prompt.txt file that contains the initial prompt sent to ChatGPT. 
This is where the magic happens.
"""
mode = input("MODE ?\n 1-Assistant\n 2-Jailbreak\n 3-DAN-6\n 4-STAN\n 5-DUDE\n 6-Mongo Tom\n")

if mode == "1" :
	with open("/home/USERNAME/chatgpt-linux-assistant/system_prompt.txt", 'r') as sprompt:
		system_prompt=sprompt.read()
if mode== "2" :
	with open("/home/USERNAME/chatgpt-linux-assistant/jailbreak_prompt.txt", 'r') as sprompt:
		system_prompt= sprompt.read()
if mode== "3" :
	with open("/home/USERNAME/chatgpt-linux-assistant/dan6_prompt.txt", 'r') as sprompt:
		system_prompt= sprompt.read()
if mode== "4":
	with open("/home/USERNAME/chatgpt-linux-assistant/stan_prompt.txt", 'r') as sprompt:
		system_prompt= sprompt.read()
if mode== "5":
	with open("/home/USERNAME/chatgpt-linux-assistant/dude_prompt.txt", 'r') as sprompt:
		system_prompt= sprompt.read()
if mode== "6":
	with open("/home/USERNAME/chatgpt-linux-assistant/mongo_prompt.txt", 'r') as sprompt:
		system_prompt= sprompt.read()


#Connect to the openAI API using your API key
chatbot = Chatbot(api_key="YOUR_API_KEY!!!!!", system_prompt=system_prompt)


#Main loop
while True:
	prompt = input("Query:> ")
	#This part checks whether or not the user typed exit or quit
	#to exit the script
	if prompt.lower().strip() in ['exit', 'quit']:
		exit(0)

	#And here the query/request/question is sent to chatGPT
	response = chatbot.ask("Human: " + prompt)

	#This is in a loop for future proofing reasons in case
	#chatGPT decides to run another command after running a previous
	#one, before responding to the user so that the script is not broken.
	
	while mode == "1":
		if "@Backend" in response:
			#Extract the command that chatGPT wants to run and 
			#deserialize it.
			res = response.split("@Backend")[1]
			if debug:
				print(res)
			#if "Backend:" in res and "Proxy Natural Language Processor:" in res:
			#	print(chatbot.ask("DO NOT REPLY AS BACKEND PLEASE. ONLY REPLY as Proxy Natural Language Processor."))
			#	break
			json_str = json.loads(res)
			command = json_str['command']

			print("Running command [%s] ..."%(command))
			#Run the command and store it's outputs for later
			p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) 
			output, err = p.communicate()
			#Get the exit code
			exit_code = p.wait()
			#Send the command results to chatGPT so it can be interpreted by it.
			response = chatbot.ask('Backend: {"STDOUT":"%s", "EXITCODE":"%s"}'%(output, exit_code))
		elif "@Human" in response:
			if debug:
				print(response)
			chatGPT_reply = "Response:: " + response.split("@Human")[1]
			print(chatGPT_reply)
			break
		else:
			print("UNEXPECTED RESPONSE:: [%s]"%(response))
			break
	if mode != "1":
		print(response)
