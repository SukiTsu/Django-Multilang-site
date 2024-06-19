# Django Blog Project

## Description
Creation of a Django site displaying articles. Users can select articles of interest and change the site language.

### Prerequisites
See requirement.txt

### Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/SukiTsu/Django-Multilang-site.git
    cd Django-Multilang-site
    ```

2. **Create a virtual environment**
    ```bash
    python3 -m venv .env
    ```

3. **Activate the virtual environment**
    ```bash
    .env\Scripts\activate
    ```

4. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run migrations**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional)**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**
    ```bash
    python manage.py runserver
    ```

8. **Access the application**
    Open your browser and go to `http://127.0.0.1:8000`

## Usage

### Add Article
In the data_txt/article directory, select one of the sub-directories (corresponding to the different languages) and write your articles in a new csv file. It's important to respect partern:
-the first line corresponds to the article title. You must specify title; before writing the title.
-the second line corresponds to the article content. You must specify content; before writing the article content.
-the last line corresponds to the publication date. You must specify publication_date; before writing the date.
It's best not to include ' in the article content or title.