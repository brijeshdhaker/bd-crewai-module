#
from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import UnstructuredURLLoader

#
class LoadManager:
    """Handles document embedding generation using SentenceTransformer"""
    
    documents = []

    def __init__(self, data_dir: str, inclusions=['pdf','txt','json','docx','csv','xlsx','docx']):
        """
        Initialize the document load manager
        
        Args:
            model_name: HuggingFace model name for sentence embeddings
        """
        self.data_dir = Path(data_dir).resolve()
        self.inclusions = inclusions
        self._load_documents()

    # "Internal" or Protected Convention
    def _load_documents(self) -> List[Any]:
        return LoadManager.from_directory(str(self.data_dir), self.inclusions)

    # Public: For external use
    @classmethod
    def from_directory(cls, dir: str, inclusions=['pdf','txt','json','docx','csv','xlsx','docx']): 
        """ 
        Load all supported files from the data directory and convert to LangChain document structure.
        Supported: PDF, TXT, CSV, Excel, Word, JSON 
        """
        _documents = []
        # Use project root data folder
        data_path = Path(dir).resolve()
        print(f"[DEBUG] Data path: {data_path}")
        if "pdf" in inclusions:
            # PDF files
            pdf_paths = list(data_path.glob('**/*.pdf'))
            pdf_files = [str(p) for p in pdf_paths]
            _pdfs = LoadManager.from_pdfs(pdf_files)
            _documents.extend(_pdfs)
        
        if "txt" in inclusions:
            # TEXT files
            txt_paths = list(data_path.glob('**/*.txt'))
            _files = [str(p) for p in txt_paths]
            _txts = LoadManager.from_txts(_files)
            _documents.extend(_txts)
        
        if "csv" in inclusions:
            # CSV files
            _paths = list(data_path.glob('**/*.csv'))
            _files = [str(p) for p in _paths]
            _pdfs = LoadManager.from_csvs(_files)
            _documents.extend(_pdfs)

        if "xlsx" in inclusions:
            # TEXT files
            _paths = list(data_path.glob('**/*.xlsx'))
            _files = [str(p) for p in _paths]
            _pdfs = LoadManager.from_xlsx(_files)
            _documents.extend(_pdfs)
        
        if "docx" in inclusions:
            # TEXT files
            _paths = list(data_path.glob('**/*.docx'))
            _files = [str(p) for p in _paths]
            _pdfs = LoadManager.from_docx(_files)
            _documents.extend(_pdfs)
        
        if "json" in inclusions:
            # JSON files
            json_paths = list(data_path.glob('**/*.json'))
            json_files = [str(p) for p in json_paths]
            _jsons = LoadManager.from_json(json_files)
            _documents.extend(_jsons)
        #
        print(f"[DEBUG] Total loaded documents: {len(_documents)}")
        return _documents

    @classmethod
    def from_docx(cls, pdf_paths: List[str]):
        _documents = []
        # docx urls
        print(f"[DEBUG] Found {len(pdf_paths)} page : {[str(f) for f in pdf_paths]}")
        for _path in pdf_paths:
            print(f"[DEBUG] Loading MS Word document from : {_path}")
            try:
                loader = Docx2txtLoader(str(_path))
                loaded = loader.load()
                print(f"[DEBUG] Loaded {len(loaded)} MS Word document from {_path}")
                _documents.extend(loaded)
            except Exception as e:
                print(f"[ERROR] Failed to load MS Word document {_path}: {e}")

        return _documents
    
    @classmethod
    def from_xlsx(cls, pdf_paths: List[str]):
        _documents = []
        # Web urls
        print(f"[DEBUG] Found {len(pdf_paths)} page : {[str(f) for f in pdf_paths]}")
        for _path in pdf_paths:
            print(f"[DEBUG] Loading MS Excel document from : {_path}")
            try:
                loader = UnstructuredExcelLoader(str(_path))
                loaded = loader.load()
                print(f"[DEBUG] Loaded {len(loaded)} MS Excel document from {_path}")
                _documents.extend(loaded)
            except Exception as e:
                print(f"[ERROR] Failed to load MS Excel document {_path}: {e}")

        return _documents
    
    @classmethod
    def from_csvs(cls, pdf_paths: List[str]):
        _documents = []
        # Web urls
        print(f"[DEBUG] Found {len(pdf_paths)} page : {[str(f) for f in pdf_paths]}")
        for _path in pdf_paths:
            print(f"[DEBUG] Loading csv document from : {_path}")
            try:
                loader = CSVLoader(str(_path))
                loaded = loader.load()
                print(f"[DEBUG] Loaded {len(loaded)} csv document from {_path}")
                _documents.extend(loaded)
            except Exception as e:
                print(f"[ERROR] Failed to load csv document {_path}: {e}")

        return _documents
    
    @classmethod
    def from_txts(cls, pdf_paths: List[str]):
        _documents = []
        # Web urls
        print(f"[DEBUG] Found {len(pdf_paths)} page : {[str(f) for f in pdf_paths]}")
        for _path in pdf_paths:
            print(f"[DEBUG] Loading text document from : {_path}")
            try:
                loader = TextLoader(str(_path))
                loaded = loader.load()
                print(f"[DEBUG] Loaded {len(loaded)} text documents from {_path}")
                _documents.extend(loaded)
            except Exception as e:
                print(f"[ERROR] Failed to load text documents {_path}: {e}")

        return _documents
    
    @classmethod
    def from_pdfs(cls, pdf_paths: List[str]):
        _documents = []
        # Web urls
        print(f"[DEBUG] Found {len(pdf_paths)} page : {[str(f) for f in pdf_paths]}")
        for _path in pdf_paths:
            print(f"[DEBUG] Loading pdf document from : {_path}")
            try:
                loader = PyPDFLoader(str(_path))
                loaded = loader.load()
                print(f"[DEBUG] Loaded {len(loaded)} PDF document from {_path}")
                _documents.extend(loaded)
            except Exception as e:
                print(f"[ERROR] Failed to load PDF document {_path}: {e}")

        return _documents
    
    @classmethod
    def from_json(cls, json_paths: List[str]):
        _documents = []
        # Web urls
        print(f"[DEBUG] Found {len(json_paths)} page : {[str(f) for f in json_paths]}")
        for _path in json_paths:
            print(f"[DEBUG] Loading json from : {_path}")
            try:
                loader = JSONLoader(str(_path), jq_schema=".results[].summary")
                loaded = loader.load()
                print(f"[DEBUG] Loaded {len(loaded)} JSON document from {_path}")
                _documents.extend(loaded)
            except Exception as e:
                print(f"[ERROR] Failed to load JSON document {_path}: {e}")

        return _documents
    
    @classmethod
    def from_web(cls, web_paths: List[str]):
        _documents = []
        # Web urls
        print(f"[DEBUG] Found {len(web_paths)} page : {[str(f) for f in web_paths]}")
        for web_path in web_paths:
            print(f"[DEBUG] Loading pages from web : {web_path}")
            try:
                loader = WebBaseLoader(web_paths=[web_path])
                loaded = loader.load()
                print(f"[DEBUG] Loaded {len(loaded)} Web document from {web_path}")
                _documents.extend(loaded)
            except Exception as e:
                print(f"[ERROR] Failed to load Web document from {web_path}: {e}")

        return _documents
    

    @classmethod
    def from_url(cls, web_paths: List[str]):
        _documents = []
        # Web urls
        print(f"[DEBUG] Found {len(web_paths)} page : {[str(f) for f in web_paths]}")
        for web_path in web_paths:
            print(f"[DEBUG] Loading pages from url: {web_path}")
            try:
                loader = UnstructuredURLLoader(urls=web_paths)
                loaded = loader.load()
                print(f"[DEBUG] Loaded {len(loaded)} Web documents from {web_path}")
                _documents.extend(loaded)
            except Exception as e:
                print(f"[ERROR] Failed to load Web document from {web_path}: {e}")

        return _documents
    
    # "Private" with Name Mangling (__name)
    def __setupLoader(self):
        """

        """

# Example usage
if __name__ == "__main__":
   
    #load_manager = LoadManager("docs")

    dir_douments = LoadManager.from_directory("docs", inclusions=['txt','json'])
    print(f"[*INFO] Total loaded documents: {len(dir_douments)}")

    #json_douments = LoadManager.from_json(['docs/json/articals.json'])
    #print(f"[*INFO] Total loaded documents: {len(json_douments)}")

    #web_douments = LoadManager.from_web(['https://educosys.com/#faq'])
    #print(f"[*INFO] Total loaded documents: {len(web_douments)}")
