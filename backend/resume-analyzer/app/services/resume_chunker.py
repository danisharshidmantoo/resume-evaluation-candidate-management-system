from langchain_text_splitters import RecursiveCharacterTextSplitter


class ResumeChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_resume(self, resume_text: str):
        return self.text_splitter.split_text(resume_text)