import concurrent
import logging
import random
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Type, Union

from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.html_bs import BSHTMLLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader

FILE_LOADER_TYPE = Union[
    Type[UnstructuredFileLoader], Type[TextLoader], Type[BSHTMLLoader], Type[CSVLoader]
]
logger = logging.getLogger(__name__)


class CustomDirectoryLoader(BaseLoader):
    """
    CustomDirectoryLoader is a versatile document loader that extracts documents from files
    contained in directories. It extends the BaseLoader class from LangChain and supports
    loading documents using different loaders based on file patterns (globs).

    Attributes:
        path (str): Path to the directory.
        loader_map (Dict[str, FILE_LOADER_TYPE]): Mapping of file patterns (globs) to loader classes.
        loader_kwargs_map (Optional[Dict[str, dict]]): Mapping of file patterns (globs) to keyword arguments for loaders.
        metadata_map (Optional[Dict[str, Dict[str, Any]]]): Mapping of file patterns (globs) to metadata dictionaries.
        default_metadata (Optional[Dict[str, Any]]): Default metadata to apply to all documents.
        recursive (bool): Whether to search directories recursively. Defaults to False.
        max_depth (Optional[int]): Maximum depth of directory traversal. If None, no limit is applied.
        silent_errors (bool): Whether to ignore errors silently. Defaults to False.
        load_hidden (bool): Whether to load hidden files. Defaults to False.
        show_progress (bool): Whether to show a progress bar during loading. Defaults to False.
        use_multithreading (bool): Whether to use multithreading for loading. Defaults to False.
        max_concurrency (int): Maximum number of concurrent threads. Defaults to 4.
        exclude (Union[Sequence[str], str]): Patterns to exclude from loading.
        sample_size (int): Maximum number of files to load. If 0, no limit is applied.
        randomize_sample (bool): Whether to randomize the sample of files loaded.
        sample_seed (Union[int, None]): Seed for randomizing the sample of files.
        output_store_map (Optional[Dict[str, Dict[str, Any]]]): Mapping of file patterns (globs) to output storage configurations.
        default_output_store (Optional[Dict[str, Any]]): Default output storage configuration for documents not matching any specific pattern.
    """

    def __init__(
        self,
        path: str,
        loader_map: Dict[str, FILE_LOADER_TYPE],
        loader_kwargs_map: Optional[Dict[str, Dict[str, Any]]] = None,
        metadata_map: Optional[Dict[str, Dict[str, Any]]] = None,
        default_metadata: Optional[Dict[str, Any]] = None,
        recursive: bool = False,
        max_depth: Optional[int] = None,
        silent_errors: bool = False,
        load_hidden: bool = False,
        show_progress: bool = False,
        use_multithreading: bool = False,
        max_concurrency: int = 4,
        exclude: Union[Sequence[str], str] = (),
        sample_size: int = 0,
        randomize_sample: bool = False,
        sample_seed: Union[int, None] = None,
        output_store_map: Optional[Dict[str, Dict[str, Any]]] = None,
        default_output_store: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the CustomDirectoryLoader with the specified parameters.

        Args:
            path (str): Path to the directory.
            loader_map (Dict[str, FILE_LOADER_TYPE]): Mapping of file patterns (globs) to loader classes.
            loader_kwargs_map (Optional[Dict[str, dict]]): Mapping of file patterns (globs) to keyword arguments for loaders.
            metadata_map (Optional[Dict[str, Dict[str, Any]]]): Mapping of file patterns (globs) to metadata dictionaries.
            default_metadata (Optional[Dict[str, Any]]): Default metadata to apply to all documents.
            recursive (bool): Whether to search directories recursively. Defaults to False.
            max_depth (Optional[int]): Maximum depth of directory traversal. If None, no limit is applied.
            silent_errors (bool): Whether to ignore errors silently. Defaults to False.
            load_hidden (bool): Whether to load hidden files. Defaults to False.
            show_progress (bool): Whether to show a progress bar during loading. Defaults to False.
            use_multithreading (bool): Whether to use multithreading for loading. Defaults to False.
            max_concurrency (int): Maximum number of concurrent threads. Defaults to 4.
            exclude (Union[Sequence[str], str]): Patterns to exclude from loading.
            sample_size (int): Maximum number of files to load. If 0, no limit is applied.
            randomize_sample (bool): Whether to randomize the sample of files loaded.
            sample_seed (Union[int, None]): Seed for randomizing the sample of files.
            output_store_map (Optional[Dict[str, Dict[str, Any]]]): Mapping of file patterns (globs) to output storage configurations.
            default_output_store (Optional[Dict[str, Any]]): Default output storage configuration for documents not matching any specific pattern.
        """
        self.path = path
        self.loader_map = loader_map
        self.loader_kwargs_map = loader_kwargs_map or {}
        self.metadata_map = metadata_map or {}
        self.default_metadata = default_metadata or {}
        self.recursive = recursive
        self.max_depth = max_depth
        self.silent_errors = silent_errors
        self.load_hidden = load_hidden
        self.show_progress = show_progress
        self.use_multithreading = use_multithreading
        self.max_concurrency = max_concurrency
        self.exclude = exclude
        self.sample_size = sample_size
        self.randomize_sample = randomize_sample
        self.sample_seed = sample_seed
        self.output_store_map = output_store_map or {}
        self.default_output_store = default_output_store or {}

    def load(self) -> List[Document]:
        """
        Load documents from the directory and return them as a list.

        Returns:
            List[Document]: List of loaded documents.
        """
        return list(self.lazy_load())

    def lazy_load(self) -> Iterator[Document]:
        """
        Lazily load documents from the directory.

        Returns:
            Iterator[Document]: An iterator over the loaded documents.
        """
        p = Path(self.path)
        if not p.exists():
            raise FileNotFoundError(f"Directory not found: '{self.path}'")
        if not p.is_dir():
            raise ValueError(f"Expected directory, got file: '{self.path}'")

        paths = p.rglob("**/*") if self.recursive else p.glob("*")
        items = [
            path for path in paths
            if not (self.exclude and any(path.match(glob) for glob in self.exclude))
            and path.is_file() and (self.load_hidden or not path.name.startswith('.'))
            and (self.max_depth is None or len(path.relative_to(p).parts) <= self.max_depth)
        ]

        if self.sample_size > 0:
            if self.randomize_sample:
                randomizer = random.Random(self.sample_seed if self.sample_seed else None)
                randomizer.shuffle(items)
            items = items[:min(len(items), self.sample_size)]

        pbar = None
        if self.show_progress:
            try:
                from tqdm import tqdm
                pbar = tqdm(total=len(items))
            except ImportError:
                logger.warning("To log the progress of CustomDirectoryLoader you need to install tqdm")

        if self.use_multithreading:
            futures = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrency) as executor:
                for i in items:
                    futures.append(
                        executor.submit(self._lazy_load_file_to_non_generator(self._lazy_load_file), i, p, pbar)
                    )
                for future in concurrent.futures.as_completed(futures):
                    for item in future.result():
                        yield item
        else:
            for i in items:
                yield from self._lazy_load_file(i, p, pbar)

        if pbar:
            pbar.close()

    def _lazy_load_file_to_non_generator(self, func: Callable) -> Callable:
        """
        Convert a generator function to a non-generator function.

        Args:
            func (Callable): The generator function to convert.

        Returns:
            Callable: A non-generator function.
        """
        def non_generator(item: Path, path: Path, pbar: Optional[Any]) -> List:
            return [x for x in func(item, path, pbar)]
        return non_generator

    def _lazy_load_file(self, item: Path, path: Path, pbar: Optional[Any]) -> Iterator[Document]:
        """
        Load a file and yield its documents.

        Args:
            item (Path): The file path.
            path (Path): The directory path.
            pbar (Optional[Any]): The progress bar object.

        Yields:
            Iterator[Document]: An iterator over the documents in the file.
        """
        if item.is_file():
            for pattern, loader_cls in self.loader_map.items():
                if item.match(pattern):
                    try:
                        loader_kwargs = self.loader_kwargs_map.get(pattern, {})
                        loader = loader_cls(str(item), **loader_kwargs)
                        for subdoc in loader.lazy_load():
                            # Apply specific and default metadata
                            specific_metadata = self.metadata_map.get(pattern, {})
                            subdoc.metadata.update(self.default_metadata)
                            subdoc.metadata.update(specific_metadata)
                            yield subdoc
                    except Exception as e:
                        if self.silent_errors:
                            logger.warning(f"Error loading file {str(item)}: {e}")
                        else:
                            raise e
                    finally:
                        if pbar:
                            pbar.update(1)


if __name__ == "__main__":
    loader_map = {
        "*.txt": TextLoader,
        "*.html": BSHTMLLoader,
        "*.csv": CSVLoader,
    }

    loader_kwargs_map = {
        "*.txt": {"encoding": "utf-8"},
        "*.csv": {"csv_args": {"delimiter": ","}},
    }

    metadata_map = {
        "*.txt": {"bar": 0},
        "*.html": dict(),
        "*.csv": {"source": "foo"}
    }

    loader = CustomDirectoryLoader(
        path="./source_data_dir",
        loader_map=loader_map,
        loader_kwargs_map=loader_kwargs_map,
        metadata_map=metadata_map,
        recursive=True,
        max_depth=3
    )

    documents = loader.load()

    for doc in documents:
        print(f"File: {doc.metadata['source']}")
        print(doc.page_content)
        print(doc.metadata)
        print("\n---\n")

