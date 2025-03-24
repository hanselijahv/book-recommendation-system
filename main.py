import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import os

exports_folder = "data/models"

# Load Models and Data
popular_df = pickle.load(open(os.path.join(exports_folder, 'popular_books.pkl'), 'rb'))
pt = pickle.load(open(os.path.join(exports_folder, 'pivot_table.pkl'), 'rb'))
books = pickle.load(open(os.path.join(exports_folder, 'books.pkl'), 'rb'))
collaborative_filtering = pickle.load(open(os.path.join(exports_folder, 'collaborative_filtering.pkl'), 'rb'))

def recommend_books(book_name, num_recommendations=10):
    try:
        if book_name not in pt.index:
            return []

        index = pt.index.get_loc(book_name)
        similar_items = sorted(list(enumerate(collaborative_filtering[index])), key=lambda x: x[1], reverse=True)[1:num_recommendations+1]

        data = []
        for i in similar_items:
            temp_df = books[books['Book-Title'].str.lower() == pt.index[i[0]].lower()]
            if temp_df.empty:
                continue

            image_url = temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values[0]
            item = [
                temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0],
                temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0],
                image_url
            ]
            data.append(item)
        return data
    except Exception as e:
        return str(e)

def fetch_popular_books():
    return popular_df.head(50)[['Book-Title', 'Book-Author', 'Image-URL-L', 'avg_rating', 'num_ratings']]

with st.sidebar:
    selected=option_menu(
        menu_title="Menu",
        options=["Home", "Recommend Books"],
        icons=["house", "book"],
        default_index=0
    )

if selected == "Home":
    st.markdown(
        """
        <h1 style='text-align: center;'>Top 50 Popular Books</h1>
        """,
        unsafe_allow_html=True
    )
    top_books = fetch_popular_books()

    st.markdown(
        """
        <style>
        .book-container {
            text-align: center;
            padding: 10px;
            display: flex;
            flex-direction: column;
            align-items: center; /* Center content horizontally */
            justify-content: center; /* Center content vertically */
        }
        .book-container img {
            border-radius: 10px;
            width: 150px;
            height: 230px;
            object-fit: cover;
        }
        .book-title {
            font-weight: bold;
            font-size: 14px !important;
            margin-top: 10px !important;
            text-align: center;
            max-width: 150px;
        }
        .book-author, .book-rating {
            font-size: 12px !important;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    for i in range(0, len(top_books), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(top_books):
                with cols[j]:
                    st.markdown(f"""
                        <div class="book-container">
                            <img src="{top_books['Image-URL-L'].iloc[i + j]}" alt="{top_books['Book-Title'].iloc[i + j]}"/>
                            <p class="book-title">{top_books['Book-Title'].iloc[i + j]}</p>
                            <p class="book-author">by {top_books['Book-Author'].iloc[i + j]}</p>
                            <p class="book-rating">⭐ {top_books['avg_rating'].iloc[i + j]:.2f} (Votes: {top_books['num_ratings'].iloc[i + j]})</p>
                        </div>
                    """, unsafe_allow_html=True)


elif selected == "Recommend Books":
    st.markdown(
        """
        <h1 style='text-align: center;'>Book Recommender System</h1>
        """,
        unsafe_allow_html=True
    )

    book_names = pt.index.tolist()

    selected_books = st.selectbox(
        "Search or choose a book from the list below",
        book_names
    )

    if st.button('Show Recommendation'):
        data = recommend_books(selected_books, num_recommendations=10)

        if data:
            num_books = len(data)

            st.markdown(
                """
                <style>
                    .book-cover img {
                        height: 250px; 
                        object-fit: cover; 
                        border-radius: 3px; 
                    }
                    .book-title {
                        text-align: center; 
                        margin-top: 100px;
                        font-size: 12px !important; /* Adjust font size here */
                    }
                </style>
                """,
                unsafe_allow_html=True
            )

            for row in range(2):
                cols = st.columns(5)
                for col in range(5):
                    idx = row * 5 + col
                    if idx < num_books:
                        item = data[idx]
                        with cols[col]:
                            st.markdown(f"""
                                <div class="book-cover">
                                    <img src="{item[2]}" alt="{item[0]}" />
                                </div>
                                <p class="book-title">{item[0]}</p>
                            """, unsafe_allow_html=True)
        else:
            st.error("No similar books found. Try another title.")

