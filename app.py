from flask import Flask, request, jsonify, render_template
import ast

app = Flask(__name__)

USER_DATA = {
    "user_id": "john_doe_17091999",
    "email": "john@xyz.com",
    "roll_number": "ABCD123"
}

def process_array(arr):
    even_numbers = []
    odd_numbers = []
    alphabets = []
    special_chars = []
    sum_numbers = 0

    for item in arr:
        if isinstance(item, str):
            item_strip = item.strip()
            if item_strip.isalpha():
                alphabets.append(item_strip.upper())
            elif item_strip.isdigit():
                num = int(item_strip)
                sum_numbers += num
                if num % 2 == 0:
                    even_numbers.append(item_strip)
                else:
                    odd_numbers.append(item_strip)
            else:
                digits = ''.join(filter(str.isdigit, item_strip))
                chars = ''.join(filter(str.isalpha, item_strip))
                specials = ''.join(filter(lambda c: not c.isalnum(), item_strip))

                if digits:
                    num = int(digits)
                    sum_numbers += num
                    if num % 2 == 0:
                        even_numbers.append(digits)
                    else:
                        odd_numbers.append(digits)

                if chars:
                    alphabets.append(chars.upper())

                if specials:
                    special_chars.append(specials)
        elif isinstance(item, int):
            sum_numbers += item
            if item % 2 == 0:
                even_numbers.append(str(item))
            else:
                odd_numbers.append(str(item))

    all_alpha_chars = ''.join(alphabets)[::-1]
    concat_string = ''
    upper = True
    for ch in all_alpha_chars:
        concat_string += ch.upper() if upper else ch.lower()
        upper = not upper

    return {
        "is_success": True,
        "user_id": USER_DATA["user_id"],
        "email": USER_DATA["email"],
        "roll_number": USER_DATA["roll_number"],
        "even_numbers": even_numbers,
        "odd_numbers": odd_numbers,
        "alphabets": alphabets,
        "special_characters": special_chars,
        "sum": str(sum_numbers),
        "concat_string": concat_string
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    try:
        raw_data = request.data.decode("utf-8")
        
        # Backend sanitization of curly quotes
        raw_data = raw_data.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")

        data = ast.literal_eval(raw_data)
        if not isinstance(data, list):
            return jsonify({"error": "Input is not a list"}), 400
        
        result = process_array(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
