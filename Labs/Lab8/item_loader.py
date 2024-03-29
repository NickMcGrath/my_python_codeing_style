"""
This module contains all the classes that are responsible or have
something to do with the creation of LibraryItems. Classes currently
implemented:
    - FactoryMapper
      Client facing class used to retrieve the right factory class
"""
import abc
import pandas
from items import *


class LibraryItemFactory(abc.ABC):
    """
    A Base Class for a library factory to extend. Contains method to get
    items from the path provided.
    """

    def __init__(self, path):
        """
        Initialize a factory with a path to the file needed to create a
        factory item.
        :param path: path to file containing content's needed to create
        library items
        """
        self.path = path

    @abc.abstractmethod
    def get_next_item(self):
        """
        Generator.
        Reads the excel file and iterate over each row of the data
        frame. The details from these rows should be used to create and
        yield the corresponding Library Item.
        :return: generator
        """
        pass


class MangaFactory(LibraryItemFactory):
    """
    Manga Factory, creates Manga library items from file path provided.
    """
    def get_next_item(self):
        """
        Generator.
        Reads the excel file and iterate over each row of the data
        frame. The details from these rows should be used to create and
        yield the corresponding Manga item.
        :return: generator
        """
        excel_df = pandas.read_excel(self.path)
        for row in excel_df.iterrows():
            row_dic = row[1].to_dict()
            yield Manga(**row_dic)


class GameFactory(LibraryItemFactory):
    """
    Game Factory, creates Manga library items from file path provided.
    """
    def get_next_item(self):
        """
        Generator.
        Reads the excel file and iterate over each row of the data
        frame. The details from these rows should be used to create and
        yield the corresponding Game item.
        :return: generator
        """
        excel_df = pandas.read_excel(self.path)
        for row in excel_df.iterrows():
            row_dic = row[1].to_dict()
            yield Game(**row_dic)


class MovieFactory(LibraryItemFactory):
    """
    Movie Factory, creates Manga library items from file path provided.
    """
    def get_next_item(self):
        """
        Generator.
        Reads the excel file and iterate over each row of the data
        frame. The details from these rows should be used to create and
        yield the corresponding Movie item.
        :return: generator
        """
        excel_df = pandas.read_excel(self.path)
        for row in excel_df.iterrows():
            row_dic = row[1].to_dict()
            yield Movie(**row_dic)


class FactoryMapper:
    """
    FactoryMapper contains the class methods to prompt the user for the
    type of item they wish to acquire and returns a factory that can
    provide the items selected.
    """

    # TODO: Populate factory_map
    factory_map = {
        1: MangaFactory,
        2: GameFactory,
        3: MovieFactory
    }
    """
    Factory map is a dictionary of type {int, FactoryClass}
    """

    @classmethod
    def execute_factory_menu(cls):
        """
        Prompts the user to select the type of items they wish to load an
        returns the appropriate factory.
        :return: object of type LibraryItemFactory
        """
        print("Item Loader")
        print("-----------")
        print("What kind of items would you like to load?")
        print("1. Manga")
        print("2. Games")
        print("3. Movies")
        user_choice = int(input("Enter your choice (1-3):"))
        factory_type = cls.factory_map[user_choice]

        file_name = input("\nEnter file name of the excel file to load from:")
        return factory_type(file_name)


if __name__ == '__main__':
    df = pandas.read_excel("games_data.xlsx")
