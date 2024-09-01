from deep_translator import GoogleTranslator
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

def translate_line(line, translator):
    if '=' in line:
        key, value = line.split('=', 1)
        try:
            # Translate the value
            translated_value = translator.translate(value.strip())
            return f"{key}={translated_value}\n"
        except Exception as e:
            logging.error(f"Translation error for line '{line}': {e}")
            return line  # Return the original line if translation fails
    else:
        return line  # Return the original line if it doesn't contain '='

def translate_file(input_file, output_file, src_lang='en', dest_lang='th', num_threads=12):
    translator = GoogleTranslator(source=src_lang, target=dest_lang)
    
    try:
        # Read the content of the input file
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        
        total_lines = len(lines)
        # Prepare to write the translated content
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    input_file = 'lang/cleaned_en_GB.lang'
    output_file = 'lang/th_TH.lang'
    translate_file(input_file, output_file)
    logging.info("Translation completed.")
