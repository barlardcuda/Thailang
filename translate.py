from deep_translator import GoogleTranslator
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

def translate_line(line, translator):
    if '=' in line:
        key, value = line.split('=', 1)
        try:
            translated_value = translator.translate(value.strip())
            return f"{key}={translated_value}\n"
        except Exception as e:
            logging.error(f"Translation error for line '{line}': {e}")
            return line
    else:
        return line

def translate_file(input_file, output_file, src_lang='en', dest_lang='th', num_threads=12):
    translator = GoogleTranslator(source=src_lang, target=dest_lang)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        
        total_lines = len(lines)
        with open(output_file, 'w', encoding='utf-8') as outfile:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                future_to_line = {executor.submit(translate_line, line, translator): line for line in lines}
                for index, future in enumerate(as_completed(future_to_line), start=1):
                    try:
                        result = future.result()
                        outfile.write(result)
                    except Exception as e:
                        logging.error(f"Error processing line: {e}")
                    logging.info(f'{index}/{total_lines} lines processed')

    except FileNotFoundError:
        logging.error(f"File not found: {input_file}")
    except IOError as e:
        logging.error(f"IO error: {e}")

import os

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    d = input('\nNode =  ')
    input_file = os.path.abspath(f'lang/cut/{d}.lang')
    output_file = os.path.abspath(f'lang/output/{d}.lang')

    # Log absolute paths and current working directory
    logging.debug(f"Current working directory: {os.getcwd()}")
    logging.debug(f"Input file path: {input_file}")
    logging.debug(f"Output file path: {output_file}")

    # Check if the input file exists
    if not os.path.isfile(input_file):
        logging.error(f"File not found: {input_file}")
    else:
        translate_file(input_file, output_file)
        logging.info("Translation completed.")