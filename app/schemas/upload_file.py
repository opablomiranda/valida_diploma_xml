from pydantic import BaseModel


class ValidationResult(BaseModel):
    """
    Resultado da validação do diploma de graduação no MEC.
    """
    valido: bool
    """
    Valido Indica se o diploma é válido ou não. True e False
    """