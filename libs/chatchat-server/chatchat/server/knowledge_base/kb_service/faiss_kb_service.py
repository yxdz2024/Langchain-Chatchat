import os
import shutil
from typing import Dict, List, Tuple

from langchain.docstore.document import Document
<<<<<<< HEAD:server/knowledge_base/kb_service/faiss_kb_service.py
from typing import List, Dict, Optional, Tuple
import logging
=======

from chatchat.settings import Settings
from chatchat.server.file_rag.utils import get_Retriever
from chatchat.server.knowledge_base.kb_cache.faiss_cache import (
    ThreadSafeFaiss,
    kb_faiss_pool,
)
from chatchat.server.knowledge_base.kb_service.base import KBService, SupportedVSType
from chatchat.server.knowledge_base.utils import KnowledgeFile, get_kb_path, get_vs_path
>>>>>>> 40994eb6c3c8aeb9af4d52123abfb471a3f27b9c:libs/chatchat-server/chatchat/server/knowledge_base/kb_service/faiss_kb_service.py


class FaissKBService(KBService):
    vs_path: str
    kb_path: str
    vector_name: str = None

    def vs_type(self) -> str:
        return SupportedVSType.FAISS

    def get_vs_path(self):
        return get_vs_path(self.kb_name, self.vector_name)

    def get_kb_path(self):
        return get_kb_path(self.kb_name)

    def load_vector_store(self) -> ThreadSafeFaiss:
        return kb_faiss_pool.load_vector_store(
            kb_name=self.kb_name,
            vector_name=self.vector_name,
            embed_model=self.embed_model,
        )

    def save_vector_store(self):
        self.load_vector_store().save(self.vs_path)

    def get_doc_by_ids(self, ids: List[str]) -> List[Document]:
        with self.load_vector_store().acquire() as vs:
            #print("yxdz-get_doc_by_ids-vs")
            #print(vs)
            return [vs.docstore._dict.get(id) for id in ids]

    def del_doc_by_ids(self, ids: List[str]) -> bool:
        with self.load_vector_store().acquire() as vs:
            vs.delete(ids)

    def do_init(self):
        self.vector_name = self.vector_name or self.embed_model.replace(":", "_")
        self.kb_path = self.get_kb_path()
        self.vs_path = self.get_vs_path()

    def do_create_kb(self):
        if not os.path.exists(self.vs_path):
            os.makedirs(self.vs_path)
        self.load_vector_store()

    def do_drop_kb(self):
        self.clear_vs()
        try:
            shutil.rmtree(self.kb_path)
        except Exception:
<<<<<<< HEAD:server/knowledge_base/kb_service/faiss_kb_service.py
                ...

    def do_search(self,
                  query: str,
                  top_k: int,
                  score_threshold: float = SCORE_THRESHOLD,
                  ) -> List[Tuple[Document, float]]:
        embed_func = EmbeddingsFunAdapter(self.embed_model)
        logging.info("yxdz-embed_func")
        logging.info(embed_func)
        logging.info("yxdz-query")
        logging.info(query)


        embeddings = embed_func.embed_query(query)


        # logging.info("yxdz-embeddings")
        # logging.info(embeddings)

        # logging.info(top_k)
        # logging.info(score_threshold)
        with self.load_vector_store().acquire() as vs:
            
            docs2 = vs.similarity_search_with_score_by_vector(embeddings, k=top_k, score_threshold=score_threshold)
            #不使用向量
            docs1 = vs.similarity_search_with_score(query,k=top_k, score_threshold=score_threshold)

            docs3 = vs.max_marginal_relevance_search(query,k=top_k, lambda_mult=score_threshold)

            docs4= vs.max_marginal_relevance_search_by_vector(embeddings,k=top_k, lambda_mult =score_threshold)

            #docs5=vs._similarity_search_with_relevance_scores(query,k=top_k)

            print("yxdz-r1")
            print(docs1)
            
            print("yxdz-r2")
            print(docs2)

            print("yxdz-r3-max_marginal_relevance_search")
            print(docs3)

            print("yxdz-r4-max_marginal_relevance_search-embed")
            print(docs4)

            #print("yxdz-r5-similarity_search_with_relevance_scores")
            #print(docs5)


        return docs1

    def do_add_doc(self,
                   docs: List[Document],
                   **kwargs,
                   ) -> List[Dict]:
        data = self._docs_to_embeddings(docs) # 将向量化单独出来可以减少向量库的锁定时间
        
        logging.info("yxdz-do_add_doc-data")
        logging.info(data)

=======
            pass

    def do_search(
        self,
        query: str,
        top_k: int,
        score_threshold: float = Settings.kb_settings.SCORE_THRESHOLD,
    ) -> List[Tuple[Document, float]]:
        with self.load_vector_store().acquire() as vs:
            retriever = get_Retriever("ensemble").from_vectorstore(
                vs,
                top_k=top_k,
                score_threshold=score_threshold,
            )
            docs = retriever.get_relevant_documents(query)
        return docs

    def do_add_doc(
        self,
        docs: List[Document],
        **kwargs,
    ) -> List[Dict]:
        texts = [x.page_content for x in docs]
        metadatas = [x.metadata for x in docs]
>>>>>>> 40994eb6c3c8aeb9af4d52123abfb471a3f27b9c:libs/chatchat-server/chatchat/server/knowledge_base/kb_service/faiss_kb_service.py
        with self.load_vector_store().acquire() as vs:
            embeddings = vs.embeddings.embed_documents(texts)
            ids = vs.add_embeddings(
                text_embeddings=zip(texts, embeddings), metadatas=metadatas
            )
            if not kwargs.get("not_refresh_vs_cache"):
                vs.save_local(self.vs_path)
<<<<<<< HEAD:server/knowledge_base/kb_service/faiss_kb_service.py
                logging.info("yxdz-self.vs_path")
                logging.info(self.vs_path)
            


        doc_infos = [{"id": id, "metadata": doc.metadata} for id, doc in zip(ids, docs)]        
        torch_gc()
=======
        doc_infos = [{"id": id, "metadata": doc.metadata} for id, doc in zip(ids, docs)]
>>>>>>> 40994eb6c3c8aeb9af4d52123abfb471a3f27b9c:libs/chatchat-server/chatchat/server/knowledge_base/kb_service/faiss_kb_service.py
        return doc_infos

    def do_delete_doc(self, kb_file: KnowledgeFile, **kwargs):
        with self.load_vector_store().acquire() as vs:
            ids = [
                k
                for k, v in vs.docstore._dict.items()
                if v.metadata.get("source").lower() == kb_file.filename.lower()
            ]
            if len(ids) > 0:
                vs.delete(ids)
            if not kwargs.get("not_refresh_vs_cache"):
                vs.save_local(self.vs_path)
        return ids

    def do_clear_vs(self):
        with kb_faiss_pool.atomic:
            kb_faiss_pool.pop((self.kb_name, self.vector_name))
        try:
            shutil.rmtree(self.vs_path)
        except Exception:
            ...
        os.makedirs(self.vs_path, exist_ok=True)

    def exist_doc(self, file_name: str):
        if super().exist_doc(file_name):
            return "in_db"

        content_path = os.path.join(self.kb_path, "content")
        if os.path.isfile(os.path.join(content_path, file_name)):
            return "in_folder"
        else:
            return False


if __name__ == "__main__":
    faissService = FaissKBService("test")
    faissService.add_doc(KnowledgeFile("README.md", "test"))
    faissService.delete_doc(KnowledgeFile("README.md", "test"))
    faissService.do_drop_kb()
    print(faissService.search_docs("如何启动api服务"))
