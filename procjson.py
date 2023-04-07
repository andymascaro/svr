import json
import re

def fix_json_numbers(match):
    before_decimal = match.group(1) or '0'
    after_decimal = match.group(3) or '0'
    return f"{before_decimal}.{after_decimal}"

def replace_inner_quotes(match):
    return match.group(0).replace('"', "'")

def fix_json_formatting(json_str):
    # Remove single-line comments (//comment)
    json_str = re.sub(r'//.*', '', json_str)

    # Remove multi-line comments (/* hey heres a comment */)
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)

    # Fix numbers
    json_str = re.sub(r'(?:(\d)|(\s|-))\.(?:(\d)|(\s))', fix_json_numbers, json_str)

    # Remove whitespace before opening brackets ([ and {)
    json_str = re.sub(r'\s*([\[\{])\s*', r'\1', json_str)

    # Remove whitespace after closing brackets (] and })
    json_str = re.sub(r'\s*([\]\}])\s*', r'\1', json_str)

    # Remove whitespace around commas
    json_str = re.sub(r'\s*,\s*', ',', json_str)

    # Remove whitespace around :
    json_str = re.sub(r'\s*:\s*', ':', json_str)

    # Remove trailing commas before closing brackets (] and })
    json_str = re.sub(r',\s*([\]\}])', r'\1', json_str)



    # Replace single quotes with double quotes
    json_str = re.sub(r'\'', r'"', json_str)

    # Replace any remaining double quotes inside double-quoted strings with single quotes
    json_str = re.sub(r'(?<=":").+?(?=",)', replace_inner_quotes, json_str)

    # Wrap any non-number value in double quotes
    #json_str = re.sub(r':\s*([^"])([^\d\s,]+)([^"])', r': "\2"', json_str)

    return json_str

def fix_json_file(input_file, output_file):
    with open(input_file, 'r') as f:
        json_str = f.read()

    fixed_json_str = fix_json_formatting(json_str)

    try:
        fixed_json = json.loads(fixed_json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    #with open(output_file, 'w') as f:
    #    f.write(fixed_json_str)
    
    with open(output_file, 'w') as f:
        json.dump(fixed_json_str, f, indent=2)

if __name__ == "__main__":
    input_file = "items.json"
    output_file = "itemsgood.json"
    fix_json_file(input_file, output_file)
