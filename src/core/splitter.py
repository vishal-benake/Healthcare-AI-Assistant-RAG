from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "; ",
            ", ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)

    # chunks = [
    #     chunk for chunk in chunks
    #     if chunk.page_content and chunk.page_content.strip()
    # ]

    chunks = [
    chunk for chunk in chunks
    if chunk.page_content and len(chunk.page_content.strip()) > 20
      ]

    return chunks