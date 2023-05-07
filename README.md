# FlairStyle

FlairStyle is an online store that features a unique weather-based clothing selection feature. Additionally, each clothing item has a unique number or QR code that must be registered on our website to add it to your wardrobe.

## Weather-based Clothing Selection

Our website features a page where you can select clothes based on the current weather conditions. We will suggest clothing from your wardrobe if you already have it registered on our website. If not, we'll suggest purchasing it on our website.

## Tech Stack

FlairStyleShop are building using the following technologies:

- Python
- Django
- JavaScript
- HTML
- CSS

## Getting Started with FlairStyleShop

1. Clone the repository
   - To get started with the FlairStyleShop project, you'll need to clone the repository. You can do this by running the following command in your terminal:

     ```!/bin/bash
     git clone git@github.com:FlairStyle/FlairStyleShop.git
     ```

2. Install Poetry
   - Poetry is a package manager for Python that will make managing dependencies for this project much easier. You can install it by following the instructions on the Poetry website: <https://python-poetry.org/docs/#installation>

3. Set up code linters and formatters
   - The project is already configured with mypy, flake8, black, and isort. You just need to activate the virtual environment and install the dependencies. You can do this by running the following commands in your terminal from the project root directory:

     ```!/bin/bash
     # Activate the virtual environment
     poetry shell

     # Install the dependencies
     poetry install
     ```

4. Create a .env file
   - In order to run the project, you'll need to create a .env file in the root directory of the project. You can copy the .env-sample file and rename it to .env. Make sure to replace the `SECRET_KEY` value with a secret key that has been provided to you.

5. Run database migrations
   - The project is using SQLite as the database backend, so you don't need to set up a separate database server. You can simply run the following command in your terminal from the project root directory to apply the initial database migrations:

     ```!/bin/bash
     python manage.py migrate
     ```

6. Start the development server
   - Once you've completed the above steps, you can start the development server by running the following command in your terminal from the project root directory:

     ```!/bin/bash
     python manage.py runserver
     ```

   - This should start the server at `http://localhost:8000/`, which you can open in your web browser to see the project homepage.

### Set up for PyCharm

1. Configure PyCharm for Poetry
   - Open the project in PyCharm and go to `Settings > Project > Python Interpreter`.
   - Click on the gear icon and select `Add...`.
   - Choose `Poetry Environment` and select the virtual environment for this project (usually located in `.venv` in the project directory).
   - Click `OK` to save the changes.

2. Configure PyCharm for linters and formatters
   - In the same `Settings > Project > Python Interpreter` window, click on the gear icon again and select `Show All...`.
   - Go to `Tools > Python Integrated Tools`.
   - Under `Code Quality Tools`, set `Flake8` and `mypy` as the respective linters.
   - Under `Code Style`, set `Black` and `isort` as the respective formatters.
   - Click `Apply` to save the changes.

## Contributors

- Misha: misha2003200@gmail.com
- Kirill: lokhmanovkirill@gmail.com

For any business-related inquiries, please contact us at flairstyle_team@proton.me.

Feel free to contact us if you have any questions about the project or would like to contribute to its development.

Thank you for using FlairStyle!
