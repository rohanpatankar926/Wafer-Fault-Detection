import unittest
from main import app
import os


class TestToPerform(unittest.TestCase):
    def setUp(self):
        pass
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_page(self):
        response = self.app.get('/', follow_redirects=True)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_page1(self):
        response1 = self.app.get('/main', follow_redirects=True)
        print(response1)
        self.assertEqual(response1.status_code, 200)
        

    def test_page2(self):
        response2 = self.app.get('/data', follow_redirects=True)
        print(response2)
        self.assertEqual(response2.status_code, 200)
    
    def test_page3(self):
        response3 = self.app.get('/saved_models', follow_redirects=True)
        print(response3)
        self.assertEqual(response3.status_code, 200)
    
    def test_page4(self):
        response3 = self.app.get('/upload', follow_redirects=True)
        print(response3)
        self.assertEqual(response3.status_code, 200)
    
    def test_page5(self):
        response4 = self.app.get('/logs', follow_redirects=True)
        print(response4)
        self.assertEqual(response4.status_code, 200)
        
    def test_page6(self):
        response5 = self.app.get('/stream/train', follow_redirects=True)
        print(response5)
        self.assertEqual(response5.status_code, 200)

        

if __name__ == '__main__':
    unittest.main()
