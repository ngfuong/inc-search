import os

from types import GeneratorType

from inc_search._utils import gen_source


class FSA:
    """
    Base Class which defines the common methods for Trie.
    """

    __slots__ = '_id', '_num_of_words', 'root'

    def __init__(self, root):
        self._id = 1
        self._num_of_words = 1
        self.root = root

    def __contains__(self, word):
        """ Returns true if the word is present else false

        Parameters
        ----------
        word: str
            The word to be searched

        Returns
        -------
        boolean
            Whether the word is present
        """
        if word == '':
            return True  # The root is an empty string. So it is always present
        if word is None:
            return False
        node = self.root
        for i, letter in enumerate(word):
            if letter in node.children:
                node = node[letter]
                if node.eow and i == len(word) - 1:
                    return True
            else:
                return False
        return False

    def __contains_prefix(self, prefix):
        """ Checks whether the prefix is present. If yes, returns (True, node) where the prefix ends else returns (False, None)

        Parameters
        ----------
        prefix: str
            The Prefix string

        Returns
        -------
        tuple: (exists, node)
            If yes, returns (True, node) where the prefix ends else returns (False, None)
        """
        if prefix == '':
            return True, self.root
        if prefix is None:
            return False, None
        node = self.root
        for _, letter in enumerate(prefix):
            if letter in node.children:
                node = node[letter]
            else:
                return False, None
        return True, node

    def contains_prefix(self, prefix):
        """ Returns a boolean indicating the presence of prefix

        Parameters
        ----------
        prefix: str
            The Prefix string

        Returns
        -------
        boolean
            True, if present, else False.
        """
        contains, _ = self.__contains_prefix(prefix)
        return contains

    def search_with_prefix(self, prefix, with_count=False):
        """ Returns a list of words which share the same prefix as passed in input. The words are by default sorted in the increasing order of length.

        Parameters
        ----------
        prefix: str
            The Prefix string

        Returns
        -------
        list
            A list of words which share the same prefix as passed in input
        """
        if not prefix:
            return []
        _, node = self.__contains_prefix(prefix)
        if node is None:
            return []
        return FSA.__words_with_wildcard(node, '*', 0, prefix, with_count=with_count)

    def add(self, word, count=1):
        pass

    def add_all(self, source):
        """ Add a collection of words from any of the following passed in input

        Words which are not of type string are not inserted in the Trie

        Parameters
        ----------
        source: list, set, tuple, generator, file
            Words to be added
        """
        if isinstance(source, (GeneratorType, str, list, tuple, set)):
            pass
        elif hasattr(source, 'read'):
            pass
        else:
            raise ValueError(
                "Source type {0} not supported ".format(type(source)))

        if isinstance(source, str) and not os.path.exists(source):
            raise IOError("File does not exists")

        if isinstance(source, str) or hasattr(source, 'read'):
            source = gen_source(source)

        for word in source:
            if type(word) == str:
                self.add(word)

    def get_word_count(self):
        """ Returns the number of words in Trie data structure

        Returns
        -------
        int
            Number of words in Trie data structure
        """
        return max(0, self._num_of_words - 1)
