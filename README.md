# Meal Plan App

## Overview
The Meal Plan App is a web application designed to help users plan their meals efficiently. This app allows users to explore various recipes, create personalized meal plans, and generate shopping lists based on the chosen recipes.

## Features
- **Recipe Search**: Easily search through a variety of recipes based on ingredients, diet preferences, and cuisine types.
- **Meal Planning**: Create meal plans for the week, allowing users to choose what to eat each day.
- **Shopping List**: Automatically generate a shopping list based on the meal plan.
- **User Accounts**: Users can create accounts to save their meal plans and favorite recipes.
- **Responsive Design**: Mobile-friendly layout for ease of use on any device.

## Installation Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/eriverods/meal_plan_app.git
   cd meal_plan_app
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Deployment Guides
### Streamlit Cloud
1. Commit and push your changes to the main branch of your repository.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account and select the `meal_plan_app` repository.
4. Click on the “Deploy” button to launch your app.
5. Your app will be live once the deployment process completes, and you will be provided a link to access it.

### Docker
1. Ensure you have Docker installed on your machine.
2. Build the Docker image:
   ```bash
   docker build -t meal_plan_app .
   ```
3. Run the Docker container:
   ```bash
   docker run -p 8501:8501 meal_plan_app
   ```
4. Access the app by navigating to `http://localhost:8501` in your web browser.

## Usage Instructions
- Open the app in your browser after deployment.
- Use the search feature to find recipes.
- Add recipes to your meal plan and customize your meals for the week.
- Generate and download your shopping list for easy grocery shopping.

## Troubleshooting
- **App not loading**: Check your internet connection and ensure the app is deployed correctly.
- **Recipe search returns no results**: Make sure your search criteria are correct. Try using different ingredients or keywords.
- **Deployment issues on Streamlit Cloud**: Ensure all dependencies are listed in `requirements.txt` and that there are no errors in the logs.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
