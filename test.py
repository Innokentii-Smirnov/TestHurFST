import os
import requests
from os import path
SOURCE = 'TestSuite'
TARGET = 'out'
URL = 'http://127.0.0.2:8067'
os.makedirs(TARGET, exist_ok=True)
for file in os.listdir(SOURCE):
	infile = path.join(SOURCE, file)
	with open(infile, 'r', encoding='utf-8') as fin:
		outfile = path.join(TARGET, file)
		with open(outfile, 'w', encoding='utf-8') as fout:
			for line in fin:
				word = line.strip()
				params = {'word': word}
				r = requests.get(URL, params=params)
				analyses = r.text
				output = '{0}\n{1}\n\n'.format(word, analyses)
				fout.write(output)
