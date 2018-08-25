#/usr/bin/sh
# Build arabic-roots package

default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
all: 

# convert roots.txt into programming language tables:
#python
build:DATA=abdnormal
build:
	scripts/tokenize_uniq2.sh samples/${DATA}.txt > output/${DATA}.unq
	python scripts/analyze_doc.py -f output/${DATA}.unq -o output/${DATA}.csv

# Publish to github
publish:
	git push origin master 

