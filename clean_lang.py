def clean_lang_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            if line.strip().startswith('##'):
                continue
            parts = line.split('#', 1)
            cleaned_line = parts[0].rstrip()
            
            if cleaned_line:
                file.write(cleaned_line + '\n')

if __name__ == "__main__":
    input_file = 'lang/en_GB.lang'
    output_file = 'lang/cleaned_en_GB.lang'
    clean_lang_file(input_file, output_file)
