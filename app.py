from flask import Flask, render_template, request

app = Flask(__name__)

SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

START = 0.28
END = 10.00
STEP = (END - START) / (len(SYMBOLS) - 1)


def encode_text(message):
    output = []
    first = True

    for character in message.upper():

        if character == " ":
            output.append("  ")
            first = True
            continue

        if character in SYMBOLS:
            position = SYMBOLS.index(character)
            value = START + (position * STEP)
            value = round(value, 3)

            if not first:
                output.append(" ")

            output.append('"' + f"{value:.3f}" + '"')
            first = False

        else:
            if not first:
                output.append(" ")

            output.append('"' + character + '"')
            first = False

    return "".join(output)


@app.route("/", methods=["GET", "POST"])
def index():
    encoded = ""

    if request.method == "POST":
        text = request.form.get("text", "")
        encoded = encode_text(text)

    return render_template("index.html", encoded=encoded)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
