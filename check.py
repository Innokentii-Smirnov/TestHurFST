import os
import requests
from os import path
from os.path import splitext
from typing import Callable
from shutil import rmtree
def read_infile(infile: str) -> list[tuple[str, list[str]]]:
	result = list[tuple[str, list[str]]]()
	with open(infile, 'r', encoding='utf-8') as fin:
		while (word := fin.readline().strip()) != '':
			analyses = list[str]()
			while (line := fin.readline().strip()) != '':
				analyses.append(line)
			result.append((word, analyses))
			if len(analyses) == 0:
				line = fin.readline().strip()
				assert line == '', infile
	return result
def evaluate(preddata: list[tuple[str, list[str]]], corrdata: list[tuple[str, list[str]]], log: Callable[[str], None]) -> tuple[float, int, int, list[tuple[str, list[str], list[str]]]]:
	correct, total = 0, 0
	errors = list[tuple[str, list[str], list[str]]]()
	for ((pred_word, pred_analyses), (corr_word, corr_analyses)) in zip(preddata, corrdata, strict=True):
		if pred_word != corr_word:
			log('Input words not matching: {0} {1}\n'.format(pred_word, corr_word))
		if pred_analyses == corr_analyses:
			correct += 1
		else:
			errors.append((pred_word, pred_analyses, corr_analyses))
		total += 1
	accuracy = 100 * correct / total
	return accuracy, correct, total, errors
def write_errors(errors: list[tuple[str, list[str], list[str]]], outfile: str):
	if len(errors) > 0:
		with open(outfile, 'w', encoding='utf-8') as fout:
			for word, preds, corrs in errors:
				fout.write(word + '\n')
				for pred in preds:
					fout.write(pred + '\n')
				fout.write('\n')
				for corr in corrs:
					fout.write(corr + '\n')
				fout.write('\n\n')
PRED_DIR = 'out'
CORR_DIR = 'correct'
CHECK_LOG = 'check_result.txt'
ERR_DIR = 'errors'
LINE_TEMPLATE = '{0:20} {1} % ({2}/{3})\n'
rmtree(ERR_DIR)
os.mkdir(ERR_DIR)
general_correct, general_total = 0, 0
with open(CHECK_LOG, 'w', encoding='utf-8') as check_log:
	for file in os.listdir(CORR_DIR):
		predfile = path.join(PRED_DIR, file)
		corrfile = path.join(CORR_DIR, file)
		errfile = path.join(ERR_DIR, file)
		preddata = read_infile(predfile)
		corrdata = read_infile(corrfile)
		accuracy, correct, total, errors = evaluate(preddata, corrdata, check_log.write)
		general_correct += correct
		general_total += total
		output_line = LINE_TEMPLATE.format(splitext(file)[0], round(accuracy, 2), correct, total)
		check_log.write(output_line)
		write_errors(errors, errfile)
	general_accuracy = 100 * general_correct / general_total
	output_line = LINE_TEMPLATE.format('Total', round(general_accuracy, 2), general_correct, general_total)
	check_log.write('\n')
	check_log.write(output_line)
