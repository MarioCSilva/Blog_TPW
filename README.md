# BLOGWHERE
[https://brunobastos.pythonanywhere.com](https://brunobastos.pythonanywhere.com)

## Trabalho de Tecnologias de Programação Web

#### Bruno Bastos / Nmec: 93302
#### Mário Silva / Nmec: 93430


## Contas de Utilizadores:
|   USER    |   PASSWORD   |              NOTAS               |
| :-------: | :----------: | :------------------------------: |
| inescosta | randomquerty | Possui um Blog "Makeup" público. |
| ruilopes  | randomquerty | Possui um Blog "Gaming" privado. |
| joao1234  | randomquerty |                                  |


## Descrição do Website
O nosso site, Blogwhere, é uma rede social que permite aos utilizadores registados criarem blogs e fazerem posts nos mesmos.
Neste tipo de sistema a nosso ver não faz muito sentido que utilizadores não logados tenham acesso a qualquer funcionalidade portanto ao tentarem aceder a qualquer página sem estarem logados serão redirecionados para a página de login.

**Nota:**
```
    Em todos os campos dos formulários ou de inputs é feito sempre a verificação da existência de erros dentro das views e caso existam, estes são mostrados aos utilizadores, como por exemplo, o registo de users com usernames ou emails já presentes na base de dados, login errado, adicionar utilizadores não existentes como gestores de uma página, etc.
```


1. Todos os utilizadores que se registam neste site têm automaticamente o seu próprio blog com o tópico associado **Personal**.
    - As definições desta página de blog podem ser alteradas, tais como o <u>nome</u>, <u>descrição</u>, <u>tópicos abordados</u>, <u>visibilidade (Público ou Privado)</u>, <u>aceitar pedidos de acesso à página se for privada</u> e <u>gerir os subscritos desta página</u>.
    - As páginas podem ser **públicas** ou **privadas** sendo que a diferença entre elas é de que em páginas privadas é necessário ser subscrito da mesma para ter acesso ao conteudo desta.
    - <u>O facto da página ser **privada** não quer dizer que esta não aparece em resultados de pesquisa.</u> Outros utilizadores podem subscrever a página porém **terão de ser aceites pelo dono da página**, enquanto que uma página **pública** o pedido de subscrição é **aceite automaticamente**.
    - A página **pessoal** <u>não pode ser eliminada</u>.


2. Os utilizadores no entanto podem criar outras páginas.
    - Estas páginas de blog criadas podem ser costumizadas da mesma maneira que as páginas pessoais (são verificadas as permissões de acesso a estas definições).
    - Pode ter **vários donos** (a gestão da página é partilhada).
    - É possivel eliminá-la quando o desejar (apenas os utilizadores donos da página pode apagá-la).
    - Ao aceder a um blog caso o utilizador não seja público ou não seja subscritor não poderá ver o seu conteudo e aparecerá um aviso.
    - Poderá enviar um pedido de subscrição que aparecerá ao dono da página e este pode aceitá-lo caso assim o queria.
    - Os utilizadores donos de uma página são automáticamente considerados como subscritores dela mesma.
    - Caso o utilizador tenha acesso ao seu conteúdo, poderá também criar posts que serão guardados nesse blog.
    - Estes posts serão apenas visíveis na **página principal** caso o utilizador seja **subscritor** da página, no entanto pode aceder ao conteúdo acedendo diretamente à pagina do blog caso este seja público.


3. Posts:
    - Criando um post na página principal irá postá-lo na página pessoal do utilizador.
    - É possível ir para o profile ao clicar no nome ou imagem do utilizador que criou o post e também para a blog onde o post foi publicado.
    - Os posts podem ter uma imagem, titulo e texto associado no momento de sua criação (têm também um campo de data que regista a hora do post).
    - Podem ser criados através da página principal, o que é o mesmo que publicar através do seu Blog pessoal.
    - Outros utilizadores podem reagir a um post com likes (é realizado através de uma função AJAX para não ter que ser necessário o refresh da página atual).
    - Podem também comentar o post, e ver os comentários feitos.


4. Página principal:
    - É possível ver os posts de blogs dos quais o utilizador logado é subscritor.
    - Existem filtros de pesquisa para os posts como por exemplo pesquisar pelo nome do utilizador que o postou ou pelo título do post, ordenar por número de likes,comentários ou por data de inserção tanto ascendente como descendente.
    - Na mesma página, na tab dos Blogs, é possivel procurar por páginas de blogs pelo nome, filtrá-las pelos tópicos e ordená-las pelo número de subscritores ou de posts.


5. Utilizadores:
    - Podem sempre que quiserem, alterar as suas informações pessoais como o nome, data de aniversário, sexo, descrição e imagem de perfil na página do profile.
    - Achamos que estas informações não são necessárias para que um utilizador possa usufruir do website portanto não são pedidas no registro.
    - Caso o utilizador ainda não tenha alterado estas informações, serão usados valores default como None para o sexo e data de aniversario e o nome fica igual ao username.
    - Pode tambem alterar dados da conta como o email, password e username na página das **settings**.    
