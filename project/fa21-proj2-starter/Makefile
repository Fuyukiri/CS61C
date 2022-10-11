PYTHON = python3

.PHONY = help convert ascii convert binary read

.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To convert text file to binary: make text_to_bin bin=[INSERT BINARY FILE NAME] text=[INSERT TEXT FILE NAME]"
	@echo "To convert binary file to text: make bin_to_text text=[INSERT TXT FILE NAME] bin=[INSERT BINARY FILE NAME]"
	@echo "To read a binary file: make read bin=[INSERT BINARY FILE NAME]"
	@echo "------------------------------------"

bin_to_text:
	${PYTHON} tools/convert.py ${bin} ${text} --to-ascii

text_to_bin:
	${PYTHON} tools/convert.py ${text} ${bin} --to-binary

read:
	xxd -e -g 4 ${bin}