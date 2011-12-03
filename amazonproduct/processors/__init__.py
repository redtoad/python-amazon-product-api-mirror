
# paginator types
ITEMS_PAGINATOR = 'ItemPage'
RELATEDITEMS_PAGINATOR = 'RelatedItemPage'


class BaseProcessor (object):

    def parse(self, fp):
        raise NotImplementedError

    @classmethod
    def load_paginator(cls, paginator_type):
        return None

    @classmethod
    def parse_cart(cls, node):
        """
        Returns an instance of :class:`amazonproduct.contrib.Cart` based on
        information extracted from ``node``.

        Obviously, this has to be implemented in each subclass of
        :class:`BaseProcessor`.
        """
        raise NotImplementedError


class BaseResultPaginator (object):

    """
    Wrapper class for paginated results. This class will call the passed
    function iteratively until either the specified limit is reached or all
    result pages are fetched.
    """

    counter = None

    def __init__(self, fun, *args, **kwargs):
        """
        :param limit: limit fetched pages to this amount (restricted to a
        maximum of 10 pages by API itself).
        """
        self.fun = fun
        self.args, self.kwargs = args, kwargs
        self.limit = kwargs.pop('limit', 10)

        # fetch first page to get pagination parameters
        self._first_page = self.page(1)

    def __iter__(self):
        """
        Iterate over all paginated results of ``fun``.
        """
        # return cached first page
        yield self._first_page
        while self.current < self.pages and self.current < self.limit:
            yield self.page(self.current + 1)

    def __len__(self):
        """
        Returns the number of total results.
        """
        return self.results

    def page(self, index):
        """
        Fetch single page from results.
        """
        self.kwargs[self.counter] = index
        root = self.fun(*self.args, **self.kwargs)
        self.current, self.pages, self.results = self.extract_data(root)
        return root

    def extract_data(self, node):
        """
        Extracts pagination data from XML node.
        """
        raise NotImplementedError
