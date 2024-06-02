from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
from pywebio.input import input, select
from pywebio.output import put_text, clear, put_table
from pywebio import start_server

# Lista de campeonatos e seus IDs
championships = {
    "UEFA Champions League": "3dd",
    "UEFA Europa League": "3dg",
    "England Premier League": "3dj",
    "England Championship": "3dk",
    "Netherlands Eredivisie": "3fp",
    "Netherlands Eerste Divisie": "3fr",
    "Germany Bundesliga": "3g6",
    "Germany 2": "3g9",
    "Germany 3": "3gc",
    "Belgium Pro League": "3kg",
    "Croatia 1": "3ln",
    "Denmark Superliga": "3ml",
    "Finland Veikkausliiga": "3nd",
    "France Ligue 1": "3nm",
    "Greece Super League": "3no",
    "Greece Football League": "3ok",
    "Italy Serie A": "3qi",
    "Italy Serie B": "3ql",
    "Norway Eliteserien": "3sk",
    "Norway Obos-Ligaen": "3sn",
    "Poland Ekstraklasa": "400",
    "Poland 1": "403",
    "Portugal Liga Portugal": "409",
    "Scotland Championship": "41m",
    "Scotland League One": "425",
    "Scotland League Two": "428",
    "Spain La Liga": "43o",
    "Spain La Liga 2": "43r",
    "Sweden Allsvenskan": "444",
    "Sweden Superettan": "44a",
    "Argentina Superliga": "469",
    "Brazil Serie A": "46l",
    "Brazil Serie B": "46o",
    "Brazil Serie C": "471",
    "Chile Primera Division": "477",
    "Colombia Liga BetPlay": "47g",
    "Mexico Liga MX": "4a0",
    "Uruguay Primera Division": "4ar",
    "USA Major League Soccer": "4b7",
    "Saudi Arabia Pro League": "4gr",
    "Japan J-League": "4hm",
    "China PR Super League": "4ie",
    "Japan J2-League": "4ji",
    "South America Copa Sudamericana": "4mp",
    "South America Copa Libertadores": "4n2",
    "Finland Kakkonen": "4on",
    "Brazil Paulista A1": "50j",
    "USA MLS Next Pro": "6e4",
    "Copa America": "4mn",
    "Copa do Brasil": "46r",
}

# Função para escolher um campeonato
def get_championship_choice():
    championship_names = list(championships.keys())
    champ_name = select("Escolha um campeonato:", options=championship_names)
    champ_id = championships[champ_name]
    return champ_name, champ_id

def main():
    # Configurar o serviço do ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Inicializar o navegador
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")  # Desabilitar bloqueio de pop-ups
    chrome_options.add_argument("--headless")  # Adicionar modo headless
    chrome_options.add_argument("--window-size=1920x1080")  # Adicionar tamanho da janela para evitar possíveis problemas de renderização
    driver = webdriver.Chrome(service=service, options=chrome_options)

    while True:
        clear()
        champ_name, champ_id = get_championship_choice()
        put_text(f"Você escolheu: {champ_name}")

        # Abrir a URL do campeonato escolhido
        league_url = f"https://cornerprobet.com/pt/league/{champ_id}"
        driver.get(league_url)

        # Aguardar o carregamento completo da página
        driver.implicitly_wait(10)  # Espera até 10 segundos ate que a pagina esteja carregada

        # Selecionar a tabela de classificação pelo XPath
        classification_xpath = '//*[@id="app"]/div[4]/section/div[2]/div[2]/div[2]'
        classification_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, classification_xpath))
        )

        # Pegar os dados da tabela de classificação
        classification_rows = classification_table.find_elements(By.TAG_NAME, "tr")

        # Criar um dicionário para mapear os times e suas posições
        team_positions = {}
        for index, row in enumerate(classification_rows, start=1):
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 1:
                team_name = columns[1].text
                team_positions[team_name] = index - 1  # Subtrair 1 para corrigir a posição

        # Selecionar a tabela de cantos pelo XPath
        corners_table_xpath = '//*[@id="app"]/div[4]/section/div[2]/div[3]/div[2]/div[1]/div[2]/table[1]'
        corners_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, corners_table_xpath))
        )

        # Rolar a página até o elemento da tabela de cantos
        driver.execute_script("arguments[0].scrollIntoView();", corners_table)

        # Pegar os dados da tabela de cantos
        corners_rows = corners_table.find_elements(By.TAG_NAME, "tr")

        # Criar um dicionário para mapear os times e suas estatísticas de cantos
        team_corners_stats = {}
        for row in corners_rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 4:  # Garantir que há colunas suficientes
                team_name = columns[0].text
                zero_to_ten_favor = float(columns[1].text.replace('%', '')) / 100
                zero_to_ten_against = float(columns[2].text.replace('%', '')) / 100
                corners_favor = float(columns[8].text)
                corners_against = float(columns[9].text)
                team_corners_stats[team_name] = {
                    '0-10 Favor': zero_to_ten_favor,
                    '0-10 Against': zero_to_ten_against,
                    'Corners Favor': corners_favor,
                    'Corners Against': corners_against
                }

        # Clicar no botão "Golos" para exibir a tabela de gols
        goals_button_xpath = '//button[contains(text(), "Golos")]'
        goals_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, goals_button_xpath))
        )

        # Rolar até o botão "Golos"
        driver.execute_script("arguments[0].scrollIntoView();", goals_button)
        time.sleep(2)  # Aguarde um momento para garantir que o botão está visível

        # Clicar no botão "Golos"
        goals_button.click()

        # Esperar a tabela de gols carregar
        time.sleep(3)  # Ajuste este tempo conforme necessário

        # Selecionar a tabela de gols pelo XPath
        goals_table_xpath = '//*[@id="app"]/div[4]/section/div[2]/div[3]/div[2]/div[2]/div[2]/table[1]'
        goals_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, goals_table_xpath))
        )

        # Rolar a página até o elemento da tabela de gols
        driver.execute_script("arguments[0].scrollIntoView();", goals_table)

        # Pegar os dados da tabela de gols
        goals_rows = goals_table.find_elements(By.TAG_NAME, "tr")

        # Criar um dicionário para mapear os times e suas estatísticas de gols
        team_goals_stats = {}
        for row in goals_rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 4:  # Garantir que há colunas suficientes
                team_name = columns[0].text
                over_0_5_ht = float(columns[1].text.replace('%', '')) / 100
                media_favor = float(columns[8].text)
                media_contra = float(columns[9].text)
                team_goals_stats[team_name] = {
                    'Over 0.5HT': over_0_5_ht,
                    'Media Favor': media_favor,
                    'Media Contra': media_contra
                }

        # Obter a data atual
        today = datetime.now().strftime("%Y-%m-%d")

        # Selecionar a tabela de jogos pelo XPath
        games_table_xpath = '//*[@id="app"]/div[4]/section/div[2]/div[1]/div[1]/div[2]/table'
        games_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, games_table_xpath))
        )

        # Pegar os dados da tabela de jogos
        games_rows = games_table.find_elements(By.TAG_NAME, "tr")

        # Processar os dados da tabela
        games_today = []
        for row in games_rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) >= 3:
                date_time_str = columns[0].text
                date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
                adjusted_date_time_obj = date_time_obj - timedelta(hours=4)  # Ajustar o fuso horário
                adjusted_date_time_str = adjusted_date_time_obj.strftime('%Y-%m-%d %H:%M')
                team1 = columns[1].text
                team2 = columns[3].text

                # Verificar se a data do jogo é a data atual
                if adjusted_date_time_str.startswith(today):
                    games_today.append((adjusted_date_time_str, team1, team2))

        # Mostrar os jogos de hoje com as posições e estatísticas de cantos e gols
        if games_today:
            put_text("\nJogos de hoje:")
            for game in games_today:
                game_time, team1, team2 = game
                team1_position = team_positions.get(team1, 'N/A')
                team2_position = team_positions.get(team2, 'N/A')
                team1_corners = team_corners_stats.get(team1, {'0-10 Favor': 'N/A', '0-10 Against': 'N/A', 'Corners Favor': 'N/A', 'Corners Against': 'N/A'})
                team2_corners = team_corners_stats.get(team2, {'0-10 Favor': 'N/A', '0-10 Against': 'N/A', 'Corners Favor': 'N/A', 'Corners Against': 'N/A'})
                team1_goals = team_goals_stats.get(team1, {'Over 0.5HT': 'N/A', 'Media Favor': 'N/A', 'Media Contra': 'N/A'})
                team2_goals = team_goals_stats.get(team2, {'Over 0.5HT': 'N/A', 'Media Favor': 'N/A', 'Media Contra': 'N/A'})

                formatted_game = (f"{game_time}\n"
                                  f"{team1}({team1_position}) x {team2}({team2_position})")

                put_text(formatted_game)

                # Lógica de sugestão de apostas
                suggestions = []
                if abs(team1_position - team2_position) > 5:
                    better_team = team1 if team1_position < team2_position else team2
                    suggestions.append(f"🏆: Vitória do {better_team}")

                total_corners_favor = team1_corners['Corners Favor'] + team2_corners['Corners Favor'] - 3
                if total_corners_favor > 0:
                    suggestions.append(f"⛳ {total_corners_favor:.1f} escanteios")

                avg_media_favor = (team1_goals['Media Favor'] + team2_goals['Media Favor']) / 2
                if avg_media_favor > 2.89:
                    suggestions.append("⚽️: Apostar em mais de 2,5 gols ou ambas marcam")
                elif avg_media_favor > 2.49:
                    suggestions.append("⚽️: Apostar em mais de 1,5 gols")
                elif avg_media_favor < 2.49:
                    suggestions.append("⚽️: Apostar em mais de 0,5 ou -3,5 gols")

                for suggestion in suggestions:
                    put_text(suggestion)
        else:
            put_text("\nNão há jogos para hoje.")

        # Perguntar se o usuário deseja escolher outro campeonato
        another_choice = select("Deseja escolher outro campeonato?", options=["Sim", "Não"])
        if another_choice == "Não":
            break

    # Fechar o navegador após a inspeção
    driver.quit()

if __name__ == "__main__":
    start_server(main, port=8080, debug=True)
