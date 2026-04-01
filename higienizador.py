"""
Higienizador - Módulo de sanitização e validação de dados.

Demonstra o uso das bibliotecas bleach (sanitização de HTML) e
pydantic (validação de dados).
"""

import bleach
from pydantic import BaseModel, EmailStr, field_validator


# ---------------------------------------------------------------------------
# Sanitização de HTML com bleach
# ---------------------------------------------------------------------------

TAGS_PERMITIDAS = ["b", "i", "u", "em", "strong", "a", "p", "br"]
ATRIBUTOS_PERMITIDOS = {"a": ["href", "title"]}


def sanitizar_html(texto: str) -> str:
    """Remove tags HTML não permitidas de uma string."""
    return bleach.clean(
        texto,
        tags=TAGS_PERMITIDAS,
        attributes=ATRIBUTOS_PERMITIDOS,
        strip=True,
    )


def remover_html(texto: str) -> str:
    """Remove todas as tags HTML de uma string."""
    return bleach.clean(texto, tags=[], strip=True)


# ---------------------------------------------------------------------------
# Validação de dados com pydantic
# ---------------------------------------------------------------------------


class Contato(BaseModel):
    nome: str
    email: EmailStr
    telefone: str

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("O nome não pode ser vazio.")
        return v

    @field_validator("telefone")
    @classmethod
    def telefone_somente_digitos(cls, v: str) -> str:
        digitos = "".join(c for c in v if c.isdigit())
        if len(digitos) < 10:
            raise ValueError("O telefone deve ter pelo menos 10 dígitos.")
        return digitos
