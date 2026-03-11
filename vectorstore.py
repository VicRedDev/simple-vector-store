import chromadb
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter
from config import VECTORSTORE_PATH, MULTI_PROCESSING_LIMIT
from ai import AI
from ui import showEmbeddingProgress

def getTextPieces(text: str):
    raw_text_pieces = text.split('\n')
    raw_text_pieces_lengths = [len(raw_text_piece) for raw_text_piece in raw_text_pieces]
    raw_piece_lengths_medium = sum(raw_text_pieces_lengths) // len(raw_text_pieces_lengths)
    max_piece_length = raw_piece_lengths_medium * 10

    text_pieces = []
    pieces = 1
    while len(raw_text_pieces) > 0:
        possible_piece = '\n'.join(raw_text_pieces[:pieces+1])
        if len(possible_piece) < max_piece_length and pieces < len(raw_text_pieces):
            pieces += 1
        else:
            text_pieces.append('\n'.join(raw_text_pieces[:pieces]))
            for i in range(pieces):
                raw_text_pieces.pop(0)
            pieces = 1

    return text_pieces

def textPieceToContent(text_piece: str, file_name: str, index: int):
    return {
        'document': text_piece, 
        'metadata': {
            'file': file_name
        }, 
        'id': f'{file_name}#{index}',
    }

def textPiecesToContents(text_pieces: list[str], file_name: str):
    contents = []
    for index, piece in enumerate(text_pieces):
        content = textPieceToContent(piece, file_name, index)
        contents.append(content)
    
    return contents


class VectorStore:
    def __init__(self):
        self.ai_client = AI()
        self.chromadb_client = chromadb.PersistentClient(
            path = f"./vectorstores/{VECTORSTORE_PATH}"
        )
        self.chromadb_collection = self.chromadb_client.get_or_create_collection(
            name = VECTORSTORE_PATH,
        )

    def _safeMultiprocessingLimit(self):
        try:
            return max(1, int(MULTI_PROCESSING_LIMIT))
        except (TypeError, ValueError):
            return 1

    def _embedTimed(self, index: int, document: str):
        started_at = perf_counter()
        embedding = self.ai_client.embed(document)
        elapsed = perf_counter() - started_at
        return index, embedding, elapsed

    def upsert(self, contents: list[dict[str, str | dict]]):
        if len(contents) == 0:
            return

        documents = [content['document'] for content in contents]
        metadatas = [content['metadata'] for content in contents]
        ids = [content['id'] for content in contents]

        total_embeddings = len(documents)
        max_workers = min(total_embeddings, self._safeMultiprocessingLimit())
        embeddings = [None] * total_embeddings
        embedding_times = []
        processed = 0

        showEmbeddingProgress(
            total = total_embeddings,
            processed = processed,
            avg_time_seconds = 0.0,
            eta_seconds = 0.0,
        )

        with ThreadPoolExecutor(max_workers = max_workers) as executor:
            futures = [
                executor.submit(self._embedTimed, index, document)
                for index, document in enumerate(documents)
            ]

            for future in as_completed(futures):
                index, embedding, elapsed = future.result()
                if embedding is False:
                    raise RuntimeError(f'Failed to generate embedding for document index {index}')

                embeddings[index] = embedding
                embedding_times.append(elapsed)
                processed += 1

                avg_time = sum(embedding_times) / len(embedding_times)
                eta = (total_embeddings - processed) * avg_time
                showEmbeddingProgress(
                    total = total_embeddings,
                    processed = processed,
                    avg_time_seconds = avg_time,
                    eta_seconds = eta,
                )

        if any(embedding is None for embedding in embeddings):
            raise RuntimeError('Failed to generate all embeddings for upsert')

        self.chromadb_collection.upsert(
            documents = documents,
            embeddings = embeddings,
            metadatas = metadatas,
            ids = ids,
        )

    def query(self, texts: list[str], k: int = 5):
        query_embeddings = [self.ai_client.embed(text) for text in texts]

        if query_embeddings is False:
            raise RuntimeError('Failed to generate embeddings for query')

        results = self.chromadb_collection.query(
            query_embeddings = query_embeddings,
            n_results = k,
        )
        return results
