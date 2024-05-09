from fastapi import APIRouter, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from app.dependencies.valida_mec import validar_diploma_mec
from app.schemas.upload_file import ValidationResult
import os



router = APIRouter()    


@router.post("/diploma_upload/", tags=["Diplomas"] ,status_code=status.HTTP_200_OK, response_model=ValidationResult)
async def valida_diploma_MEC(file: UploadFile):
    """
    A Rota Valida um diploma no MEC.\n
    Recebe um arquivo de diploma no formato XML, envia-o para o site do MEC para validação e retorna o resultado da validação.\n
    Site onde o é validado:\n 
    https://validadordiplomadigital.mec.gov.br/diploma \n
    Args:
        file.xml (UploadFile): O arquivo de diploma no formato XML.
    Returns:
        DiplomaValidationResult: O resultado da validação do diploma.\n
        "valido" : true - Indica um diploma XML validado no MEC que está em Conformidade\n
        "valido" : false - indica um diploma XML validado no MEC que está Inválido
    curl -X 'POST'  \n
    'http://127.0.0.1:8000/diploma_upload/'  \n
    -H 'accept: application/json'  \n
    -H 'Content-Type: multipart/form-data'  \n
    -F 'file=@diploma.xml;type=text/xml'            
    """

    try:
        #Verifica se o arquivo é um XML
        if file.content_type != "text/xml":
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Erro, arquivo com formato inválido, só é aceito 'text/xml'")


        #Dá um nome para o arquivo recebido

        file.filename='diploma.xml'

        # Determina o caminho onde salvar o arquivo. 
        uploads_directory = "uploads"
        os.makedirs(uploads_directory, exist_ok=True)  # Cria a pasta se não existir
        
        # Define o caminho completo do arquivo no diretório
        file_path = os.path.join(uploads_directory, file.filename)
        
        # Grava o conteúdo do arquivo no diretório chamado uploads
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        try:
            #Envia o arquivo para ser validado no MEC
            resultado = validar_diploma_mec(file_path)
            #Remove o arquivo da pasta
            os.remove(file_path)
            #Se o xml for inválido retorna false, se for verdadeiro retorna true
            return JSONResponse(content={"valido": resultado})
            
        except HTTPException as e:
            os.remove(file_path)
            raise e

    except HTTPException as e:
    
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    except Exception as e:  
    
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(e)})
   


@router.get("/")
async def read_root():
    return {"message": "Hello, World"}