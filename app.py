from flask import Flask,render_template,request, jsonify
import pickle
import numpy as np
import os

exports_folder = "exports"

popular_df = pickle.load(open(os.path.join(exports_folder, 'popular.pkl'), 'rb'))
pt = pickle.load(open(os.path.join(exports_folder, 'pt.pkl'), 'rb'))
books = pickle.load(open(os.path.join(exports_folder, 'books.pkl'), 'rb'))
collaborative_filtering = pickle.load(open(os.path.join(exports_folder, 'collaborative_filtering.pkl'), 'rb'))

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('HomePage.html',
                           book_name =popular_df['Book-Title'].to_list(),
                           author=popular_df['Book-Author'].to_list(),
                           image=popular_df['Image-URL-L'].to_list(),
                           votes=popular_df['num_ratings'].to_list(),
                           rating=popular_df['avg_rating'].to_list()
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('RecommendPage.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input', '').strip().lower()  # Normalize input

    # Convert the index of pt to lowercase for case-insensitive matching
    pt_index_lower = {title.lower(): title for title in pt.index}

    # Debugging print
    print("User Input:", user_input)
    print("Available Books (First 10):", list(pt_index_lower.keys())[:10])

    # Check if the user input is a valid book title in the dataset
    if user_input not in pt_index_lower:
        print("Book NOT found in dataset.")  # Debugging line
        return render_template('RecommendPage.html', error="Book not found in the dataset. Try another title.")

    print("Book FOUND in dataset.")  # Debugging line

    # Get the actual title in the original case
    actual_title = pt_index_lower[user_input]

    # Get recommendations
    index = np.where(pt.index == actual_title)[0][0]
    similar_items = sorted(list(enumerate(collaborative_filtering[index])), key=lambda x: x[1], reverse=True)[1:11]

    data = []
    for i in similar_items:
        # Ensure case-insensitive matching when searching for similar books
        temp_df = books[books['Book-Title'].str.lower() == pt.index[i[0]].lower()]

        # Check if the book exists in the dataset
        if temp_df.empty:
            continue

        # Use a placeholder image if the 'Image-URL-M' is missing
        image_url = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]
        if not image_url:  # If image URL is empty, use a placeholder
            image_url = 'https://via.placeholder.com/150'  # Placeholder image URL

        item = [
            temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0],
            temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0],
            image_url
        ]

        data.append(item)

    return render_template('RecommendPage.html', data=data, user_input=actual_title)





@app.route('/get_books', methods=['GET'])
def get_books():
    query = request.args.get('term', '').lower()
    if not query:
        return jsonify([])

    # Use pt for autocomplete suggestions instead of the raw books dataset
    matching_books = [title for title in pt.index if query in title.lower()]

    return jsonify(matching_books[:5])  # Limit to 5 suggestions


if __name__ == '__main__':
    app.run(debug=True)