from django.test import TestCase
import unittest
from main.views import check_request, readCSV
# Définir une liste de langues pour tester avec la fonction check_request
LANGUE = ['fr', 'en', 'es']
FILE_PATH = 'main/data_txt/'

class TestCheckRequest(unittest.TestCase):

    def test_langue_existante(self):
        ln = 'fr'
        file_path = FILE_PATH+'home/home_'+ln+'.csv'
        result = check_request(ln, file_path)
        self.assertIsInstance(result, dict)
        self.assertIn('ln', result)
        self.assertEqual(result['ln'], ln)
        self.assertIn('title', result)

    def test_langue_non_existante(self):
        ln = 'de'
        file_path = FILE_PATH+'home/home_'+ln+'.csv'
        result = check_request(ln, file_path)
        self.assertEqual(result, 'error')

    def test_special_case_favicon(self):
        ln = 'favicon.ico'
        file_path = FILE_PATH+'home/home_fr.csv'
        result = check_request(ln, file_path)
        self.assertEqual(result, {})

    def test_autre_langue_existante(self):
        ln = 'en'
        file_path = FILE_PATH+'home/home_'+ln+'.csv'
        result = check_request(ln, file_path)
        self.assertIsInstance(result, dict)
        self.assertIn('ln', result)
        self.assertEqual(result['ln'], ln)
        self.assertIn('label', result)


class ReadCSVTestCase(unittest.TestCase):

    def test_fichier_valide_delimiteur_par_defaut(self):
        file_path = FILE_PATH+'blog/blog_fr.csv'
        result = readCSV(file_path)
        self.assertIsInstance(result, dict)
        self.assertIn('title', result)
        self.assertIn('label', result)
        self.assertEqual(result['title'], 'Bienvenu sur notre blog')
        self.assertEqual(result['label'], 'Voici la liste des articles:')

    def test_fichier_valide_delimiteur_personnalise(self):
        file_path = FILE_PATH+'article/en/article1.csv'
        delimiter = ';'
        result = readCSV(file_path, delimiter)
        self.assertIsInstance(result, dict)
        self.assertIn('title', result)
        self.assertIn('publication_date', result)
        self.assertEqual(result['title'], 'A digital world (en)')
        self.assertEqual(result['publication_date'], '28/05/2015')

    def test_fichier_inexistant(self):
        file_path = FILE_PATH+'blog/blog_ln.csv'
        result = readCSV(file_path)
        self.assertEqual(result, {})

    def test_erreur_format_csv(self):
        file_path = FILE_PATH+'article/en/article1.csv'
        result = readCSV(file_path)
        self.assertIsInstance(result, dict)
        self.assertNotEqual(len(result), 0)  # Assurez-vous que le dictionnaire contient des données valides

if __name__ == '__main__':
    unittest.main()
