
from ..desktop import MakoTaskWarriorDatabase 

import unittest 

class TestMaoTaskWarriorDatabase(unittest.TestCase):
    
    def setUp(self):
        self.db = MakoTaskWarriorDatabase("test_data/db/task/")

    def test_project_download(self):
        projects = self.db.downloadProjects()
        self.assertEqual(len(projects), 2)

    def test_project_upload(self):
        # when we download projects, upload them to another database and download them again, we should get the same objects
        projects = self.db.downloadProjects()
        db2 = MakoTaskWarriorDatabase("test_data/db/task2/")
        db2.uploadProjects(projects)
        projects2 = db2.downloadProjects()
        self.assertEqual(len(projects), len(projects2))
