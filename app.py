from flask import Flask, render_template, request
from data_processing import df, model, get_recommends  # Import data & functions

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = None

    if request.method == "POST":
        book_title = request.form.get("book_title", "").strip()

        # ✅ Print available titles before searching
        print("DEBUG: Checking for", book_title)
        print("DEBUG: Available titles sample:", df.index[:10])

        if book_title:
            result = get_recommends(book_title, df, model)
            print("DEBUG: get_recommends output:", result)

            if result and isinstance(result, (list, tuple)) and len(result) > 1:
                recommendations = result[1]  # Extract recommended books
            else:
                recommendations = ["No recommendations found."]

    return render_template("index.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
