# SmartCart-Project E-Commerce Recommendation System

## Introduction
This project is an **E-Commerce Recommendation System** built using Flask with machine learning capabilities. The system provides personalized product recommendations using various recommendation techniques, including content-based, collaborative filtering, hybrid, and multi-model approaches. It is integrated into a user-friendly e-commerce website that allows users to browse, search, and interact with products.

## Features
- **User Authentication**: Secure user registration, login, and session management.
- **Product Browsing**: View dynamically rendered product cards with images, descriptions, prices, and ratings.
- **Personalized Recommendations**: 
  - Content-based recommendations based on product features and user preferences.
  - Collaborative filtering using user behavior data (e.g., ratings and interactions).
  - Hybrid and multi-model recommendations for improved accuracy and diversity.
- **User Feedback**: Users can provide ratings and likes to refine future recommendations.
- **Search Functionality**: Search products by name or category.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Machine Learning**: 
  - Libraries: NumPy, pandas, scikit-learn, TensorFlow
  - Algorithms: Matrix factorization, neighborhood-based methods, k-means clustering, hybrid model
- **Database**: MySQL 

## Demo
![image](https://github.com/user-attachments/assets/5dab9c00-5f3f-4b84-a886-b3805ff5df09)
![image](https://github.com/user-attachments/assets/db8434ce-6b3c-493a-9640-c3d0acb146b5)
![image](https://github.com/user-attachments/assets/7e26fcbc-5d11-40fb-b931-dd10f26e979e)
![image](https://github.com/user-attachments/assets/89c5b006-fb2e-4013-a45e-cc3366fe2b39)


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ecommerce-recommendation-system.git
   cd ecommerce-recommendation-system
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. Run the Flask app.
   ```bash
   flask run
5. Open browser and visit: http://127.0.0.1:5000
