from typing import AnyStr
from gentopia.tools.basetool import *
import urllib.request
import PyPDF2
import io

class PDFReaderInput(BaseModel):
    pdf_url: str = Field(..., description="URL link to the PDF document")

class PDFReaderTool(BaseTool):
    name = "pdf_reader_tool"
    description = "A tool that reads text from PDF documents provided by a URL."
    args_schema: Optional[Type[BaseModel]] = PDFReaderInput

    def _run(self, pdf_url: AnyStr) -> str:
      
        request = urllib.request.Request(pdf_url, headers={'User-Agent': "Mozilla/5.0"})
        pdf_content = urllib.request.urlopen(request).read()
        pdf_stream = io.BytesIO(pdf_content)
        pdf_document = PyPDF2.PdfReader(pdf_stream)
        text_output = "\n\n".join(page.extract_text() for page in pdf_document.pages)
        return text_output

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Asynchronous execution not implemented.")

if __name__ == "__main__":

    pdf_url = "https://aclanthology.org/2022.sumeval-1.3.pdf" 
    reader = PDFReaderTool()
    extracted_text = reader._run(pdf_url)
    print(extracted_text)
