<link rel="stylesheet" href="style.css">

# Objetivos
- ## Desacoplar todos os modulos da aplicação
    - ## Modulo principal: (X)
        ### Responsável por gerar a tela e gerenciar os eventos como fechar a janela e movimentos;
    - ## Modulo de interface: 
        ### Responsável pela interação com o usuário.
    <div class="descricao">
    OBS: Atualmente temos somente duas classes chamadas ContextInterface e ContextFrame. Não sei bem o motivo disso, mas acho que a ideia aterior era que ao unir ambos formasse o modulo de interface.

    - ContextFrame: Responsável por gerenciar todas as ocorrencias do applicativo;
    - ContextInterface: Responsável pela entrada de dados.
    </div>
    <a href="application\applicationframe.py"> ContextFrame </a><br>
    <a href="application\applicationinterface.py"> ContextInterface </a>
            
    - ## Modulo de simulação:
        ### Responsável por realizarto todos os calculos internos 

- ## Criação de menu principal para a janela
- ## Iniciar desenvolvimento de simulação de força e campos magnéticos


# UPDATE
- ## Nova Arquitetura:
    - ## Camada gráfica:
        <div class="descricao">Resposável pela representação visual da aplicação.</div>
    - ## Camada de entrada:
        <div class="descricao">Responsável por gerar eventos sempre que o usuário interagir com o software.<div>
    - ## Camada de regras de negócio:
        <div class="descricao">Parte do software que executa os algoritmos da applicação.</div>
    - ## Dados
        <div class="descricao">Como o nome diz, é a parte responsável pelo armazenamento de dados.</div>

- ## Representasão gráfica de interação entre camadas
    ```mermaid
    graph TD;
        A(Camada gráfica);
        B(Camada de entrada);
        C(Camada de regras de negócio);
        D(Camada de dados);
        
        B-->|Eventos|C;
        C-->|Alterar|D;
        C-->|Renderizar|A;
        D-->|Renderizar|A;
    ```
