from fastapi import Request, status

async def log_requests(req: Request, call_next):
    # Abrir o arquivo de log em modo de escrita
    with open("request_logs.txt", "a") as log_file:
        # Log da requisição
        log_file.write(f"Recebida requisição: {req.method} {req.url}\n")
        log_file.write("Cabeçalhos:\n")
        for name, value in req.headers.items():
            log_file.write(f"{name}: {value}\n")
        
        # Corpo da requisição
        body_bytes = await req.body()

        if body_bytes:
            log_file.write("Corpo da requisição:" + body_bytes.decode() + "\n")

        # Continuar com o processamento da requisição
        response = await call_next(req)

        # Log da resposta
        log_file.write(f"Enviando resposta: {response.status_code}\n")
        return response
