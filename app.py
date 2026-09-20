from flask import Flask, render_template, request

app = Flask(__name__)

# Characters that use decimal encoding
SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

START = 0.28
END = 10.00
STEP = (END - START) / (len(SYMBOLS) - 1)


# Create the decimal → character lookup table
DECIMAL_MAP = {}

for position, character in enumerate(SYMBOLS):
    value = round(START + (position * STEP), 3)
    DECIMAL_MAP[f"{value:.3f}"] = character


def encode_text(message):
    output = []
    first = True

    for character in message.upper():

        # Space between words
        if character == " ":
            output.append("  ")
            first = True
            continue

        # Letters and numbers
        if character in SYMBOLS:
            position = SYMBOLS.index(character)
            value = round(START + (position * STEP), 3)

            if not first:
                output.append(" ")

            output.append(f'"{value:.3f}"')
            first = False

        # Punctuation stays unchanged
        else:
            if not first:
                output.append(" ")

            output.append(f'"{character}"')
            first = False

    return "".join(output)


def decode_text(encoded):
    output = []

    # Two spaces represent an original word space.
    # Temporarily protect them.
    encoded = encoded.replace("  ", " <SPACE> ")

    parts = encoded.split()

    for part in parts:

        if part == "<SPACE>":
            output.append(" ")
            continue

        # Remove quotation marks
        value = part.strip('"')

        # Decimal value
        if value in DECIMAL_MAP:
            output.append(DECIMAL_MAP[value])

        # Punctuation
        else:
            output.append(value)

    return "".join(output)


@app.route("/", methods=["GET", "POST"])
def index():

    encoded = ""
    decoded = ""

    if request.method == "POST":

        # Encoder
        text = request.form.get("text", "")

        if text:
            encoded = encode_text(text)

        # Decoder
        decode_input = request.form.get("decode", "")

        if decode_input:
            decoded = decode_text(decode_input)

    return render_template(
        "index.html",
        encoded=encoded,
        decoded=decoded
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
