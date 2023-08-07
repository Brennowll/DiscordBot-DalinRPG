<a name="readme-top"></a>
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />

<h3 align="center">DalinRPG</h3>

  <p align="center">
    Uma solução para ajudar os mestres de jogos RPG no discord
    <br />
    <a href="https://github.com/Brennowll/DiscordBot-DalinRPG"><strong>Explore os docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Brennowll/DiscordBot-DalinRPG">Veja uma amostra</a>
    ·
    <a href="https://github.com/Brennowll/DiscordBot-DalinRPG/issues">Reporte um bug</a>
    ·
    <a href="https://github.com/Brennowll/DiscordBot-DalinRPG/issues">Faça um pull request</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Tabela de conteúdo</summary>
  <ol>
    <li>
      <a href="#about-the-project">Sobre o projeto</a>
      <ul>
        <li><a href="#built-with">Feito com</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Começando</a>
      <ul>
        <li><a href="#prerequisites">Requisitos</a></li>
        <li><a href="#installation">Instalação</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usos</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contribuindo</a></li>
    <li><a href="#license">Licença</a></li>
    <li><a href="#contact">Contato</a></li>
    <li><a href="#acknowledgments">Agradecimentos</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Sobre o projeto

 - Incrementar funcionalidades a um jogo de RPG feito na plataforma do Discord
 - Seu principal intuito é ajudar a mestragem, com cadastro de trilhas sonoras, loop e atribuição de apelidos para as mesmas
 - Outras funções: Rolagem de dados, sorteamento de objetos

<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>



### Built With

- <a href="https://www.python.org/">Python 3.x</a>
- <a href="https://discordpy.readthedocs.io/en/v2.1.0/">Discord.py[voice] 2.1.0</a>
- <a href="https://www.ffmpeg.org/">FFmpeg</a>

<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>



<!-- GETTING STARTED -->
## Começando

### Requisitos

* <a href="https://python.org.br/instalacao-windows/">Python 3.x</a>
* <a href="https://pt.wikihow.com/Instalar-o-FFmpeg-no-Windows">FFmpeg</a>


### Instalação

1. Clone o repositório
   ```sh
   git clone https://github.com/Brennowll/DiscordBot-DalinRPG.git
   ```
2. Instale as bibliotecas do requirements.txt
   ```sh
   pip install -r requirements.txt
   ```
3. Troque o token do bot no .env
4. Inicie o bot com o comando
   ```python3
   python3 Main.py
   ```

<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [ ] Rolagem de dados
    - [ ] /rolar = Rola dados na mesma frase (2d6+3d20+4d4+10)
    - [ ] /rolarum = Rola 1 tipo de dado
    - [ ] /rolarloop = Rola um amontoado de dados mais de uma vez
    - [ ] /sortdado = Sorteia um tipo de dado
- [ ] Trilha Sonora
    - [ ] /criartrilha = Cadastra uma música como trilha sonora
    - [ ] /trilha = Toca a trilha sonora cadastrada anteriormente a partir do apelido dado a ela (Em loop)
    - [ ] /ptrilha = Para a trilha sonora que está tocando
    - [ ] /deltrilha = Deleta uma trilha criada de escolha
    - [ ] /deltodtrilhas = Deleta todas as trilhas que você cadastrou
    - [ ] /vol = Altera o volume da trilha (0 - 150 limite)
- [ ] Utilitários
    - [ ] /calc = Calcula uma expressão matemática digitada (2x7+3/2)
    - [ ] /sort = sorteia algo entre os valores divididos com barra (um/dois/nome/lugar)
    - [ ] /mudarpref = (Somente para administradores do server) Muda o prefixo do DalinRPG para aquele server
    - [ ] Pingar/Mencionar o DalinRPG no chat = Mostra qual o prefixo do DalinRPG para o server
    - [ ] /ajuda (nome do comando) = Digitar o /ajuda com um comando mostra detalhadamente sobre um comando expecífico

Veja as [open issues](https://github.com/Brennowll/DiscordBot-DalinRPG/issues) para uma lista completa das propostas de melhorias (e problemas conhecidos).

<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

As contribuições são o que torna a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Quaisquer contribuições que você fizer são **muito apreciadas**.

Se você tiver uma sugestão para melhorar isso, fork o repositório e crie uma solicitação pull. Você também pode simplesmente abrir um problema com a tag "melhoria".
Não se esqueça de dar uma estrela ao projeto! Obrigado novamente!

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas alterações (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra uma Pull Request

<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>


<!-- CONTACT -->
## Contato

- bomtempobrenno@gmail.com

Link do projeto: [https://github.com/Brennowll/DiscordBot-DalinRPG](https://github.com/Brennowll/DiscordBot-DalinRPG)

<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Brennowll/DiscordBot-DalinRPG.svg?style=for-the-badge
[contributors-url]: https://github.com/Brennowll/DiscordBot-DalinRPG/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Brennowll/DiscordBot-DalinRPG.svg?style=for-the-badge
[forks-url]: https://github.com/Brennowll/DiscordBot-DalinRPG/network/members
[stars-shield]: https://img.shields.io/github/stars/Brennowll/DiscordBot-DalinRPG.svg?style=for-the-badge
[stars-url]: https://github.com/Brennowll/DiscordBot-DalinRPG/stargazers
[issues-shield]: https://img.shields.io/github/issues/Brennowll/DiscordBot-DalinRPG.svg?style=for-the-badge
[issues-url]: https://github.com/Brennowll/DiscordBot-DalinRPG/issues
[license-shield]: https://img.shields.io/github/license/Brennowll/DiscordBot-DalinRPG.svg?style=for-the-badge
[license-url]: https://github.com/Brennowll/DiscordBot-DalinRPG/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/brenno-bomtempo
[product-screenshot]: images/screenshot.png
