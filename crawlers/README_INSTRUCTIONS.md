# __Reddit Scraper Telegram Bot__
Projeto de um _bot_ para o aplicativo Telegram que envia uma mensagem com as _threads_ com maiores pontuações dos _subreddits_ enviados pelo usuário.

## __Índice__
- [Visão geral](#visão-geral)
- [_Setup_](#setup)
- [Rodando a Aplicação](#rodando-a-aplicação)
- [Maiores Desafios](#maiores-desafios)
- [Possíveis Melhorias](#possíveis-melhorias)

## __Visão Geral<a id='visão-geral'></a>__
Aplicação que roda um _bot_ do Telegram, escrito em Python, responsável por retornar as _threads_ mais curtidas de _subreddits_ enviados pelo usuário.

Essas _threads_ são colhidas por um _web scraper_ desenvolvido com o _framework_ Scrapy.

O _bot_ pode ser acessado clicando [aqui](https://t.me/reddit_top_threads_bot). Para solicitar as _threads_ com maiores pontuações é necessário utilizar o comando `/NadaPraFazer` seguindo dos _subreddits_ desejados separados por ponto-e-vírgula. Exemplo:
```
/NadaPraFazer worldnews;sports
```
![print de uma mensagem do telegram contendo o título, a pontuação e links de um subreddit](/assets/images/telegram_example.png "Print do Telegram")

_Observação_: a aplicação ainda não foi hospedada em um servidor on-line, então não é possível utilizar o _bot_ sem rodar a aplicação localmente. Veja como rodara a aplicação na seção [Rodando a Aplicação](rodando-a-aplicação) e mais detalhes na seção [Próximos Passos](#próximos-passos).

## **_Setup_**
Para rodar a aplicação é necessário fazer seu _build_. Para isso, na raiz do projeto (pasta `crawlers/`), rode o seguinte comando:
```
docker-compose build
```
Caso prefira rodar diretamente os arquivos utilizando o Python, é necessário ativar o ambiente virtual e instalar as dependências:
```
python3 -m venv .venv && source .venv/bin/activate
```
Em seguida:
```
pip install -r requirements.txt 
``` 

## __Rodando a Aplicação<a id='rodando-a-aplicação'></a>__
Para inicializar a aplicação, caso opte por rodá-la pelo Docker, basta executar um dos seguintes comandos:
```
docker-compose up
```
OU
```
docker-compose run app
```

Caso opte por rodar diretamente o _script_, após ativar o ambiente virtual e instalar as dependências (conforme descrito na seção anterior), é necessário entrar na pasta `reddit_telegram_bot`:
```
cd reddit_telegram_bot/
``` 
Em seguida, execute o seguinte comando:
```
python3 main.py
```
Independentemente da forma escolhida, uma vez que a aplicação estiver rodando, basta acessar o _bot_ no Telegram e enviar os comandos, conforme descrito na seção [Visão geral](#visão-geral).

_Observação_: 

É possível, também, executar somente o _scraper_ isoladamente. Ele vai imprimir no terminal os resultados do _scraping_, bem como salvá-los no arquivo `items.json` na pasta `results/`. Para isso, execute o comando:
```
python3 scraper_runner.py --subreddits="cats;sports"
```
As informações extraídas se parecerão com estas:
```
[
  {
    "subreddit_title": "sports",
    "items": [
      {
        "score": "27735",
        "subreddit": "sports",
        "title": "China orders athlete to delete photos that showed flooding in Olympic Village",
        "comments_url": "https://reddit.com/r/sports/comments/sr78oc/china_orders_athlete_to_delete_photos_that_showed/",
        "source_url": "https://www.yahoo.com/sports/winter-olympics-2022-china-orders-athlete-delete-photos-205502218-013229001.html"
      },
      {
        "score": "11052",
        "subreddit": "sports",
        "title": "USA\u2019s Erin Jackson becomes first Black woman to win Olympic speedskating gold",
        "comments_url": "https://reddit.com/r/sports/comments/srktgo/usas_erin_jackson_becomes_first_black_woman_to/",
        "source_url": "https://www.theguardian.com/sport/2022/feb/13/usas-erin-jackson-speedskating-500m-gold-winter-olympics-2022-beijing"
      }
    ]
  },
  ...
]
```

## __Maiores Desafios__
- ### Integração entre o _bot_ do Telegram e o _web scraper_
  Eu escolhi o Scrapy para fazer o desafio, pois é um _framework_ que eu já conhecia, apesar de tê-lo utilizado apenas uma vez. Contudo, ele impôs alguns desafios que, não fosse o tempo limitado já decorrido, teriam me levado a considerar usar outra solução.

  O Scrapy é um _framework_ bem fechado, sendo mais fácil rodar _scripts_ a partir de suas _pipelines_ (como, por exemplo, para salvar os dados em um banco) do que rodá-lo em outras aplicações. Tive problemas com os módulos `signals` e `twisted.internet.reactor` utilizados pelo Scrapy.
  
  No código do projeto, é possível verificar que, ao invés de instanciar a classe `ScraperRunner` e rodar seus métodos para fazer o _web scraping_, minha opção foi usar o módulo _subprocess_ para, literalmente, rodar o script Python do arquivo do _scraper_. Terminado o _scraping_, eu tenho que acessar o _json_ salvo para ler as informações e enviá-las ao _chat_ do Telegram. Infelizmente, encontrar essa solução me custou muito tempo e impediu que eu implementasse outras coisas importantes no tempo proposto, como o `deploy` do _bot_, por exemplo.

- ### Telegram Bot
  Outro desafio, embora bem menor se comparado ao anterior, foi me familiarizar com a construção de _bots_ do Telegram. Ao mesmo tempo, foi empolgante perceber como, com tão poucas linhas de código, é simples criar um _bot_.

## __Possíveis Melhorias<a id='possíveis-melhorias'></a>__
- ### Pensar em alternativas ao Scrapy
  Conforme explicado na seção anterior, talvez o Scrapy não tenha sido a melhor ferramenta para ser integrada ao _bot_. Seria interessante estudar como funcionam outras ferramentas de _web scraping_ para obter um resultado mais integrado e performático.

- ### Tratamento de erros e ampliação de casos de uso
  O tratamento de erros ficou muito simplificado e deixou de fazer algumas validações. Além disso, a aplicação deixou de cobrir vários casos de uso (por exemplo, o `/start` do _bot_). Então, seria importante mapear os erros não tratados e pensar em outras possíveis funcionalidades do _bot_.

- ### Testes
  Não foi escrito nenhum teste para a aplicação. Acredito que esse é um ponto essencial de melhoria, tanto pensando em testes unitários, como testes de integração, considerando a complexidade da aplicação que lida com serviços diferentes.

- ### _Deploy_
  É importante que o serviço de _bot_ fosse hospedado em um servidor em nuvem, para que pudesse ser utilizado por qualquer pessoa em qualquer momento. Talvez, hospedar o _scraper_ separadamente resolvesse os problemas de compatibilidade que eu tive que enfrentar, mas eu teria que estudar isso com mais calma. 
