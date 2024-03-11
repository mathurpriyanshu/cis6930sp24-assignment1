import os
import argparse
import spacy
import glob

def redact_text(input_files, output_dir, censor_flags, stats_output):

    print("Input files:", input_files)
    print("Output directory:", output_dir)
    print("Censor flags:", censor_flags)
    print("Stats output:", stats_output)
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")
    
    # Initialize statistics
    stats = {"total_files": 0, "censored_items": {}}
    
    for input_file in input_files:
        print("Processing file:", input_file)
        with open(input_file, 'r') as f:
            text = f.read()
        
        # Process text with spaCy
        doc = nlp(text)
        
        # Initialize list to store censored items
        censored_items = []
        
        # Iterate over entities and censor based on flags
        for ent in doc.ents:
            if "names" in censor_flags and ent.label_ == "PERSON":
                censored_items.append(ent.text)
                text = text.replace(ent.text, "█")
                
            if "dates" in censor_flags and ent.label_ == "DATE":
                censored_items.append(ent.text)
                text = text.replace(ent.text, "█")
                
            if "phones" in censor_flags and ent.label_ == "PHONE":
                censored_items.append(ent.text)
                text = text.replace(ent.text, "█")

            if "address" in censor_flags and ent.label_ == "ADDRESS":
                censored_items.append(ent.text)
                text = text.replace(ent.text, "█")
                
        # Write censored text to new file
        output_file = os.path.join(output_dir, os.path.basename(input_file) + ".censored")
        with open(output_file, 'w') as f:
            f.write(text)
        
        # Update statistics
        stats["total_files"] += 1
        stats["censored_items"][os.path.basename(input_file)] = censored_items
    
    # Write statistics to output file or stderr/stdout
    with open(stats_output, 'w') as f:
        f.write("Total files processed: {}\n".format(stats["total_files"]))
        for file, items in stats["censored_items"].items():
            f.write("File: {}\n".format(file))
            f.write("Censored items: {}\n".format(", ".join(items)))
            f.write("\n")

def main():
    parser = argparse.ArgumentParser(description='Text redaction system')
    parser.add_argument('--input', nargs='+', help='Input files or glob pattern')
    parser.add_argument('--output', help='Output directory for censored files')
    parser.add_argument('--names', action='store_true', help='Censor names')
    parser.add_argument('--dates', action='store_true', help='Censor dates')
    parser.add_argument('--phones', action='store_true', help='Censor phone numbers')
    parser.add_argument('--address', action='store_true', help='Censor addresses')
    parser.add_argument('--stats', help='Statistics output file or special file (stderr, stdout)')
    
    args = parser.parse_args()
    print("Parsed arguments:", args)
    
    input_files = glob.glob("./docs/input/*.txt")
    output_dir = glob.glob(args.output)
    censor_flags = []
    if args.names:
        censor_flags.append("names")
    if args.dates:
        censor_flags.append("dates")
    if args.phones:
        censor_flags.append("phones")
    if args.address:
        censor_flags.append("address")
    stats_output = args.stats
    
    redact_text(input_files, output_dir, censor_flags, stats_output)

if __name__ == "__main__":
    main()
