# Book Recommendation System

This is a Book Recommendation System built using Python, Flask, and machine learning. It leverages **cosine similarity** and **K-Nearest Neighbors (KNN)** algorithms to recommend books based on user input.

## Features
- Personalized book recommendations
- Collaborative filtering using KNN
- Content-based filtering using cosine similarity
- Interactive and user-friendly web interface

## Technologies Used
- **Python**
- **Flask** for the backend
- **Pandas** and **NumPy** for data manipulation
- **Scikit-Learn** for implementing KNN and cosine similarity
- **Gunicorn** for production deployment

## Deployment
The application is deployed on **Render**. You can access it using the following link:

[Book Recommendation System on Render]([https://your-app-url.onrender.com](https://book-recommendation-system-pil0.onrender.com/))

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your_username/book-recommendation-system.git
    cd book-recommendation-system
    ```

2. Create a virtual environment:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    source .venv/bin/activate  # On Linux/Mac
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the Flask application using Gunicorn:
    ```bash
    gunicorn app:app
    ```

2. Access the application at `http://localhost:8000`

## Usage
- Enter a book title to receive personalized recommendations.
- Browse through suggested books with relevant information like author names and cover images.

## Contributing
Contributions are welcome! Feel free to fork this repository, submit pull requests, or raise issues for any improvements.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, contact [Your Name](mailto:your-email@example.com).

Happy reading! 📚
