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
	echo "Tokenize sample data texts and extract unique words"
	scripts/tokenize_uniq2.sh samples/${DATA}.txt > output/${DATA}.unq
	python3 scripts/analyze_doc.py -f output/${DATA}.unq -o output/${DATA}.csv
	echo "Data is stored in output/${DATA}.csv"
	echo "Data stats are stored in output/${DATA}.csv.stats"

words:DATA=words
words:
	echo "Tokenize sample data word list and extract unique words"
	cut -f1 samples/${DATA}.csv > output/${DATA}.unq
	python3 scripts/analyze_doc.py -f output/${DATA}.unq -o output/${DATA}.csv
	echo "Data is stored in output/${DATA}.csv"
	echo "Data stats are stored in output/${DATA}.csv.stats"	


rostom:DATA=rostomya-utf
rostom:
	echo "Tokenize sample data word list and extract unique words"
	cut -d\; -f1 samples/${DATA}.csv > output/${DATA}.unq
	python3 scripts/analyze_doc_rostomya.py -f output/${DATA}.unq -o output/${DATA}.csv
	echo "Data is stored in output/${DATA}.csv"
	echo "Data stats are stored in output/${DATA}.csv.stats"	

# Publish to github
publish:
	git push origin master 

