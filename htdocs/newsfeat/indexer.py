import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import codecs

class Indexer:
    """
    Wraps the MeTA search engine and its rankers.
    """
    def __init__(self, root, idx_path):
        """
        Create/load a MeTA inverted index based on the provided config file and
        set the default ranking algorithm to Okapi BM25.
        """
        self.root = root
        self.idx_path = idx_path

    def index(self):

        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), \
                        content=TEXT, textdata=TEXT(stored=True))
        if not os.path.exists(self.idx_path):
            os.mkdir(self.idx_path)

        # Creating a index writer to add document as per schema
        ix = create_in(self.idx_path, schema)
        writer = ix.writer()

        filepaths = [os.path.join(self.root, i) for i in os.listdir(self.root)]
        for path in filepaths:
            with codecs.open(path, "r", "utf-8") as f:
                content = f.read()
                writer.add_document(title=unicode(path.split("/")[1]), path=unicode(path.split("/")[0]), \
                                    content=content, textdata=content)
        writer.commit()
        return "true"
