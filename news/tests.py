from django.test import TestCase
from .models import Editor,Article,tags

# Create your tests here.
class EditorTestClass(TestCase):

    # set up method
    def setUp(self):
        self.gavin = Editor(first_name = 'Esa', last_name = 'Gavin', email = 'gavinkariuki@gmail.com')
    
    # Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.gavin,Editor))
