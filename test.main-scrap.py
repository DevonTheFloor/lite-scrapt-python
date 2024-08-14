import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup

# Imaginons que la fonction `extraire` est définie dans un module nommé `mon_module`
from mon_module import extraire

class TestExtraire(unittest.TestCase):
    @patch('mon_module.requests.get')
    def test_extraire_elements(self, mock_get):
        # HTML de test à retourner par la requête simulée
        html = """
        <html>
            <body>
                <ul>
                    <li class="gem-c-document-list__item"><a href="#">Document 1</a></li>
                    <li class="gem-c-document-list__item"><a href="#">Document 2</a></li>
                    <li class="gem-c-document-list__item"><a href="#">Document 3</a></li>
                </ul>
            </body>
        </html>
        """
        # Configurer le mock pour retourner ce HTML
        mock_response = Mock()
        mock_response.content = html.encode('utf-8')
        mock_get.return_value = mock_response

        # Appeler la fonction `extraire` avec une URL fictive
        url = 'http://example.com'
        elements = extraire(url)

        # Vérifier que 3 éléments ont été extraits
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0].text, 'Document 1')
        self.assertEqual(elements[1].text, 'Document 2')
        self.assertEqual(elements[2].text, 'Document 3')

    @patch('mon_module.requests.get')
    def test_extraire_aucun_element(self, mock_get):
        # HTML sans aucun élément correspondant
        html = """
        <html>
            <body>
                <ul>
                    <li class="autre-classe"><a href="#">Document 1</a></li>
                </ul>
            </body>
        </html>
        """
        # Configurer le mock pour retourner ce HTML
        mock_response = Mock()
        mock_response.content = html.encode('utf-8')
        mock_get.return_value = mock_response

        # Appeler la fonction `extraire` avec une URL fictive
        url = 'http://example.com'
        elements = extraire(url)

        # Vérifier que la liste retournée est vide
        self.assertEqual(len(elements), 0)

    @patch('mon_module.requests.get')
    def test_extraire_requete_erreur(self, mock_get):
        # Configurer le mock pour lever une exception
        mock_get.side_effect = requests.exceptions.RequestException

        # Appeler la fonction et vérifier qu'elle lève l'exception
        url = 'http://example.com'
        with self.assertRaises(requests.exceptions.RequestException):
            extraire(url)

if __name__ == '__main__':
    unittest.main()
