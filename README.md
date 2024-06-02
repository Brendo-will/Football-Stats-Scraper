# Football-Stats-Scraper

Este projeto é um web scraper construído em Python que utiliza o Selenium para coletar dados de campeonatos de futebol de um site específico. O objetivo principal é obter informações detalhadas sobre os jogos, posições dos times, estatísticas de cantos e gols e sugerir possíveis apostas baseadas nesses dados.

Funcionalidades
Escolha do Campeonato: O usuário pode escolher entre uma lista de campeonatos de futebol internacionais.
Coleta de Dados:
Posições dos Times: Captura a posição atual dos times na tabela de classificação.
Estatísticas de Cantos: Obtém as estatísticas de cantos dos times.
Estatísticas de Gols: Coleta dados sobre gols, incluindo porcentagem de gols no primeiro tempo e média de gols a favor e contra.
Sugestão de Apostas: Baseado nos dados coletados, o programa sugere possíveis apostas para os jogos do dia.
Interface Simples: Interação com o usuário via terminal para escolha de campeonatos e visualização de resultados.
Tecnologias Utilizadas
Python: Linguagem de programação principal.
Selenium: Para automação do navegador e scraping.
webdriver-manager: Para gerenciar o ChromeDriver.
datetime: Para manipulação de datas e horários.
time: Para pausas e esperas no código.

Como Usar
Instalação de Dependências:

Certifique-se de ter o Python instalado em sua máquina.
Instale as bibliotecas necessárias:
selenium
webdriver-manager

Estrutura do Código
Lista de Campeonatos: Um dicionário contendo os nomes dos campeonatos e seus respectivos IDs.
Função get_championship_choice: Permite ao usuário escolher um campeonato.
Função main: Contém a lógica principal do scraper:
Configuração do ChromeDriver e opções do navegador.
Coleta de dados das tabelas de classificação, cantos e gols.
Processamento e exibição dos jogos do dia, incluindo sugestões de apostas.
Loop para permitir a escolha de múltiplos campeonatos.
Exemplo de Uso
Ao executar o script, o usuário verá uma lista de campeonatos e poderá escolher um digitando o número correspondente. O programa então acessará a página do campeonato escolhido, coletará os dados relevantes e exibirá os jogos do dia com sugestões de apostas baseadas nas estatísticas coletadas.

Considerações Finais
Este projeto serve como uma ferramenta útil para entusiastas de futebol e apostas, permitindo uma análise detalhada de dados de diversos campeonatos de futebol. A utilização do Selenium permite uma coleta precisa e dinâmica dos dados diretamente do site.

Futuras Melhorias
Melhoria na Interface: Implementar uma interface gráfica para melhorar a interação do usuário.
Mais Campeonatos: Adicionar suporte a mais campeonatos e ligas de futebol.
Otimização de Performance: Melhorar o tempo de execução e eficiência do scraper.
