from googletrans import Translator

def translate_to_thai(text):
    translator = Translator()
    translated = translator.translate(text, dest='th')
    return translated.text

def translate_lang_file(input_file, output_file):
    translator = Translator()
    
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        leng = len(lines)
        x = 1
        for line in lines:
            if line.strip().startswith('##'):
                file.write(line)
                continue
            
            parts = line.split('#', 1)
            key_value = parts[0].rstrip()
            
            if key_value:
                if '=' in key_value:
                    key, value = key_value.split('=', 1)
                    translated_value = translate_to_thai(value)
                    file.write(f"{key}={translated_value}\n")
                else:
                    file.write(line)
            print(f'Translate {x}/{leng}')
            x += 1

if __name__ == "__main__":
    input_file = 'lang/cleaned_en_GB.lang'
    output_file = 'lang/th_th.lang'
    translate_lang_file(input_file, output_file)