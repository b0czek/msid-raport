import argparse
import json
import openai
import csv

FIELDNAMES = ["id","floor_select", "furniture", "price", "builttype", "m", "rooms", "rent", "address"]

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process JSON file to extract addresses using OpenAI API.')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('output_file', type=str, help='Path to the output CSV file')
    parser.add_argument('api_key', type=str, help='OpenAI API Key')

    return parser.parse_args()

def extract_address(title, description):
    input_data = f"tytuł: {title}, opis: {description}"
    messages = [
        {"role": "system", "content": """Twoim zadaniem jest wyciągnąć adres mieszkania z przekazanych danych dotyczących oferty wynajmu mieszkania we Wrocławiu. 
                                        Odpowiadaj w formacie JSON w formie { "address":  } . 
                                        Bądź zwięzły i jeżeli nie znajdziesz informacji o adresie to daj null."""
        },
        {"role": "user", "content": f"{input_data}"}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
    )
    try:
        result = json.loads(response.choices[0].message.content.strip())
        return result.get("address")
    except (json.JSONDecodeError, KeyError):
        return None

def process_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, FIELDNAMES)
        writer.writeheader()

        for i, obj in enumerate(data):
            title = obj.get("title", "")
            description = obj.get("description", "")
            address = extract_address(title, description)
            if not address:
                continue

            obj["address"] = address
        
            del obj['title']
            del obj['description']
            writer.writerow(obj)
                
            print(f"Processed {i+1} / {len(data)} ({((i + 1) / len(data) * 100):.2f}%)")

def main():
    args = parse_arguments()
    
    openai.api_key = args.api_key

    process_json_file(args.input_file, args.output_file)

if __name__ == '__main__':
    main()