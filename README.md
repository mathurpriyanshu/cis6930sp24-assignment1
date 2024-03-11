
Name: Priyanshu Mathur

# Assignment Description
This Assignment is designed to censor sensitive personal information such as name, address, phone number, etc. Documents such as police reports, court transcripts, and hospital records all contain sensitive information.


# How to install
1. Clone the repository on your system:
    
$ git clone https://github.com/mathurpriyanshu/cis6930sp24-assignment1.git

    

2. Install prerequisites:
$ pipenv run python -m spacy download en_core_web_sm


# How to run
Branch to be used: main 

Command to run: 

pipenv run python censoror.py --input '*.txt' \
                    --names --dates --phones --address\
                    --output 'files/' \
                    --stats stderr

# Functions


1. **redact_text**: This function is responsible for reading input text files, processing them to redact sensitive information, and writing the redacted text to new files. It takes the following parameters:
   - `input_files`: A list of input file paths or a glob pattern representing input files.
   - `output_dir`: The directory where the redacted files will be saved.
   - `censor_flags`: A list of censor flags indicating the types of sensitive information to be redacted (e.g., names, dates).
   - `stats_output`: The file or special file (stderr, stdout) where statistics about the redaction process will be written.

   The function loads the spaCy model for English language processing, iterates over each input file, reads its content, processes it with spaCy to identify named entities, redacts the sensitive information based on the censor flags, writes the redacted text to new files with the same names but appended with ".censored", and generates statistics about the redaction process.

2. **main**: This is the entry point of the script. It parses command-line arguments using the argparse module, specifies the expected arguments, and invokes the `redact_text` function with the parsed arguments. The function takes no parameters.

The code helps in automating the redaction process of sensitive information from text files by providing a command-line interface for specifying input files, output directory, types of sensitive information to be redacted, and the location to write the statistics. It utilizes the spaCy library for named entity recognition to identify and redact sensitive information.
