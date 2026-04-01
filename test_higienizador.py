"""Testes para o módulo higienizador."""

import pytest
from pydantic import ValidationError

from higienizador import Contato, remover_html, sanitizar_html


# ---------------------------------------------------------------------------
# Testes - sanitizar_html
# ---------------------------------------------------------------------------


class TestSanitizarHtml:
    def test_permite_tags_validas(self):
        resultado = sanitizar_html("<b>negrito</b> e <i>itálico</i>")
        assert resultado == "<b>negrito</b> e <i>itálico</i>"

    def test_remove_tag_script(self):
        resultado = sanitizar_html("<script>alert('xss')</script>texto")
        assert "<script>" not in resultado
        assert "texto" in resultado

    def test_remove_atributo_onclick(self):
        resultado = sanitizar_html('<b onclick="alert(1)">clique</b>')
        assert "onclick" not in resultado
        assert "clique" in resultado

    def test_permite_link_com_href(self):
        resultado = sanitizar_html('<a href="https://exemplo.com">link</a>')
        assert 'href="https://exemplo.com"' in resultado

    def test_texto_simples_sem_alteracao(self):
        texto = "Olá, mundo!"
        assert sanitizar_html(texto) == texto


# ---------------------------------------------------------------------------
# Testes - remover_html
# ---------------------------------------------------------------------------


class TestRemoverHtml:
    def test_remove_todas_as_tags(self):
        resultado = remover_html("<p>parágrafo <b>negrito</b></p>")
        assert resultado == "parágrafo negrito"

    def test_texto_sem_html(self):
        texto = "sem tags"
        assert remover_html(texto) == texto


# ---------------------------------------------------------------------------
# Testes - Contato
# ---------------------------------------------------------------------------


class TestContato:
    def test_contato_valido(self):
        contato = Contato(
            nome="João Silva",
            email="joao@exemplo.com",
            telefone="(11) 98765-4321",
        )
        assert contato.nome == "João Silva"
        assert contato.email == "joao@exemplo.com"
        assert contato.telefone == "11987654321"

    def test_nome_vazio_invalido(self):
        with pytest.raises(ValidationError):
            Contato(nome="   ", email="a@b.com", telefone="11987654321")

    def test_email_invalido(self):
        with pytest.raises(ValidationError):
            Contato(nome="Ana", email="nao-e-email", telefone="11987654321")

    def test_telefone_curto_invalido(self):
        with pytest.raises(ValidationError):
            Contato(nome="Carlos", email="carlos@exemplo.com", telefone="123")

    def test_telefone_formatado_normalizado(self):
        contato = Contato(
            nome="Maria",
            email="maria@exemplo.com",
            telefone="+55 (21) 3333-4444",
        )
        assert contato.telefone == "552133334444"
