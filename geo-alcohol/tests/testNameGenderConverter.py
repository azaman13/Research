"""
This is the module that tests different functions in the nameGenderConverter.py
"""
from nameGenderConverter import get_gender

import unittest


class TestGenderConverterMethods(unittest.TestCase):
# Dictionary of name as key and gender as value
    FEMALE_NAMES={
        "Emma" : "female","Olivia" : "female","Sophia" : "female",
        "Isabella" : "female","Ava" : "female","Mia" : "female","Emily" : "female",
        "Abigail" : "female","Madison" : "female","Charlotte" : "female",
        "Harper" : "female","Sofia" : "female","Avery" : "female",
        "Elizabeth" : "female","Amelia" : "female","Evelyn" : "female",
        "Ella" : "female","Chloe" : "female","Victoria" : "female","Aubrey" : "female",
        "Grace" : "female","Zoey" : "female","Natalie" : "female","Addison" : "female",
        "Lillian" : "female","Brooklyn" : "female","Lily" : "female","Hannah" : "female",
        "Layla" : "female","Scarlett" : "female","Aria" : "female","Zoe" : "female",
        "Samantha" : "female","Anna" : "female","Leah" : "female","Audrey" : "female",
        "Ariana" : "female","Allison" : "female","Savannah" : "female","Arianna" : "female",
        "Camila" : "female","Penelope" : "female","Gabriella" : "female","Claire" : "female",
        "Aaliyah" : "female","Sadie" : "female","Riley" : "female","Skylar" : "female",
        "Nora" : "female","Sarah" : "female","Hailey" : "female","Kaylee" : "female","Paisley" : "female",
        "Kennedy" : "female","Ellie" : "female","Peyton" : "female","Annabelle" : "female",
        "Caroline" : "female","Madelyn" : "female","Serenity" : "female",
        "Aubree" : "female","Lucy" : "female","Alexa" : "female","Alexis" : "female",
        "Nevaeh" : "female","Stella" : "female","Violet" : "female",
        "Genesis" : "female","Mackenzie" : "female","Bella" : "female",
        "Autumn" : "female","Mila" : "female","Kylie" : "female","Maya" : "female",
        "Piper" : "female","Alyssa" : "female","Taylor" : "female","Eleanor" : "female",
        "Melanie" : "female","Naomi" : "female","Faith" : "female","Eva" : "female",
        "Katherine" : "female","Lydia" : "female","Brianna" : "female","Julia" : "female",
        "Ashley" : "female","Khloe" : "female","Madeline" : "female","Ruby" : "female",
        "Sophie" : "female","Alexandra" : "female","London" : "female","Lauren" : "female",
        "Gianna" : "female","Isabelle" : "female","Alice" : "female","Vivian" : "female",
        "Hadley" : "female", "Jasmine": "female"
    }


    def test_first_names(self):
        for name, gender in self.FEMALE_NAMES.iteritems():
            result = get_gender(name)
            self.assertEquals(result.get('gender'), 'female')



if __name__ == '__main__':
    unittest.main()