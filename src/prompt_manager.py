import json

from .utils.prompt_manager.build_prompt import build_prompt
from .utils.prompt_manager.build_prompt_cohere import build_prompt_cohere
from .utils.prompt_manager.analyze_briefing_for_strategy import analyze_briefing_for_strategy
from .utils.prompt_manager.build_image_prompt import build_image_prompt

from .utils.prompt_manager.get_token_count import get_token_count

class PromptManager:
    """
    Gerencia a construção de prompts otimizados para LLMs como o Google Gemini.
    """

    def __init__(self, client_profile: dict, niche_guidelines: dict):
        """
        Inicializa o PromptManager com o perfil do cliente e as diretrizes de nicho.
        """
        self.client_profile = client_profile
        self.niche_guidelines = niche_guidelines

    def build_prompt(self, content_type: str, weekly_themes: list[str], weekly_goal: str, campaign_type: str, strategic_analysis: dict = None) -> str:
        """
        Constrói o prompt completo para a API do Gemini, utilizando a função build_prompt refatorada.

        Args:
            client_profile (dict): O perfil do cliente.
            niche_guidelines (dict): As diretrizes de nicho.
            content_type (str): O tipo de conteúdo a ser gerado (ex: 'instagram_post').
            weekly_themes (list[str]): Uma lista de temas a serem abordados na semana.
            weekly_goal (str): O objetivo principal do conteúdo para a semana.
            campaign_type (str): O tipo de campanha (e.g., "lancamento", "autoridade").
            strategic_analysis (dict): O resultado da análise estratégica do briefing.

        Returns:
            str: O prompt completo formatado para a API do Gemini.
        """
        return build_prompt(self.client_profile, self.niche_guidelines, content_type, weekly_themes, weekly_goal, campaign_type, strategic_analysis)

    def build_prompt_cohere(self, content_type: str, weekly_themes: list[str], weekly_goal: str, campaign_type: str, strategic_analysis: dict = None) -> str:
        """
        Constrói o prompt completo para a API do Cohere, utilizando a função build_prompt_cohere refatorada.

        Args:
            content_type (str): O tipo de conteúdo a ser gerado (ex: 'instagram_post').
            weekly_themes (list[str]): Uma lista de temas a serem abordados na semana.
            weekly_goal (str): O objetivo principal do conteúdo para a semana.
            campaign_type (str): O tipo de campanha (e.g., "lancamento", "autoridade").
            strategic_analysis (dict): O resultado da análise estratégica do briefing.

        Returns:
            str: O prompt completo formatado para a API do Cohere.
        """
        return build_prompt_cohere(self.client_profile, self.niche_guidelines, content_type, weekly_themes, weekly_goal, campaign_type, strategic_analysis)

    def analyze_briefing_for_strategy(self) -> dict:
        """
        Analisa o briefing do cliente e as diretrizes de nicho para extrair informações estratégicas.

        Returns:
            dict: Um dicionário com informações estratégicas analisadas.
        """
        return analyze_briefing_for_strategy(
            client_profile=self.client_profile,
            niche_guidelines=self.niche_guidelines
        )

    def build_image_prompt(self, client_profile: dict, post_content: dict) -> str:
        """
        Constrói um prompt detalhado para uma IA de geração de imagens/vídeos com base no conteúdo do post.

        Args:
            client_profile (dict): Dicionário contendo o perfil do cliente.
            post_content (dict): Dicionário contendo o conteúdo de um post (ex: legenda_principal, formato_sugerido).

        Returns:
            str: O prompt visual detalhado para a IA de geração de imagens.
        """
        return build_image_prompt(client_profile, post_content)

    def get_token_count(self, prompt_text: str) -> int:
        """
        Estima o número de tokens de um prompt. Esta é uma estimativa simples
        baseada no número de palavras.

        Args:
            prompt_text (str): O texto do prompt.

        Returns:
            int: Número estimado de tokens.
        """
        return get_token_count(prompt_text)