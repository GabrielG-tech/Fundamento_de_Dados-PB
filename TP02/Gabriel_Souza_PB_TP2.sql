DROP DATABASE IF EXISTS empresa;
CREATE DATABASE empresa;
USE empresa;

CREATE TABLE funcionarios(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    departamento VARCHAR(30) NOT NULL,
    salario FLOAT NOT NULL,
    data_contratacao DATE NOT NULL
);

INSERT INTO funcionarios (nome, cargo, departamento, salario, data_contratacao) VALUES
    ("Lucas Oliveira", "Gerente de Recursos Humanos", "RH", 10000, "2024-04-01"),
    ("João Silva", "Analista de Marketing", "Marketing", 4500, "2023-03-15"),
    ("Maria Santos", "Engenheiro de Software", "TI", 8000, "2022-12-20"),
    ("Ana Rodrigues", "Gerente de Vendas", "Vendas", 9500, "2022-11-10"),
    ("Carlos Oliveira", "Analista Financeiro", "Financeiro", 5800, "2023-01-28"),
    ("Pedro Costa", "Desenvolvedor Web", "TI", 7000, "2022-11-05"),
    ("Juliana Pereira", "Analista de Recursos Humanos", "RH", 5000, "2024-03-12"),
    ("Ricardo Santos", "Analista de Sistemas", "TI", 6000, "2023-02-18"),
    ("Fernanda Oliveira", "Gerente de Marketing", "Marketing", 8500, "2022-12-03"),
    ("Gabriel Fernandes", "Analista de Suporte Técnico", "TI", 4800, "2023-03-25"),
    ("Larissa Souza", "Designer Gráfico", "Marketing", 4800, "2024-03-20"),
    ("Lucas Almeida", "Analista de Qualidade", "Qualidade", 5200, "2023-03-08"),
    ("Mariana Lima", "Analista de Comunicação", "Marketing", 5000, "2023-01-15"),
    ("Gabriel Souza", "Estagiário", "TI", 2000, "2024-01-01"),
    ("Amanda Santos", "Gerente de Produção", "Produção", 8000, "2022-11-30"),
    ("Paulo Gomes", "Analista de Vendas", "Vendas", 5500, "2023-02-10"),
    ("Rodrigo Costa", "Analista de Negócios", "Vendas", 6000, "2023-03-05"),
    ("Luiza Oliveira", "Analista de Recursos Humanos", "RH", 4800, "2022-12-20"),
    ("Guilherme Fernandes", "Engenheiro de Dados", "TI", 7500, "2024-04-06"),
    ("Camila Silva", "Analista de Marketing Digital", "Marketing", 5000, "2022-12-10"),
    ("Felipe Santos", "Desenvolvedor Mobile", "TI", 5800, "2023-01-05"),
    ("Isabela Almeida", "Analista Financeiro", "Financeiro", 5100, "2023-02-20"),
    ("Vanessa Silva", "Gerente de Contas", "Vendas", 10000, "2022-10-15"),
    ("Natália Oliveira", "Analista de Suporte ao Cliente", "TI", 4800, "2023-03-10"),
    ("Cristiano Silva", "Analista de Pesquisa de Mercado", "Marketing", 5500, "2022-12-05"),
    ("André Santos", "Analista de Segurança da Informação", "TI", 6200, "2022-09-20"),
    ("Patrícia Lima", "Analista Contábil", "Financeiro", 5300, "2023-01-10"),
    ("Marcelo Oliveira", "Coordenador de Projetos", "TI", 6900, "2023-02-25"),
    ("Diego Pereira", "Gerente de Operações", "Produção", 8500, "2022-12-20"),
    ("Renato Costa", "Analista de Logística", "Produção", 6000, "2023-03-20");

# 1. Consultar todos os funcionários da empresa

# 2. Consultar os funcionários ordenados por nome

# 3. Consultar o nome e o salário dos funcionários ordenados por salário em ordem decrescente

# 4. Consultar o nome e o departamento dos funcionários do departamento de TI

# 5. Consultar o nome, o salário e o departamento dos funcionários com salário maior ou igual a 6000 e que sejam do departamento de TI

# 6. Consultar os funcionários com o sobrenome "Souza"

# 7. Consultar o número de funcionários por departamento ordenado por número de funcionários em ordem decrescente

# 8. Consultar os departamentos com mais de cinco funcionários

# 9. Consultar o(s) funcionário(s) com o maior salário, utilizando subquery

# 10. Consultar o nome e a data de contratação dos funcionários contratados no ano de 2022

# 11. Consultar o número de cargos por departamento exibindo apenas os departamentos com mais de quatro cargos e ordenado por cargos em ordem decrescente

# 12. Consultar os funcionários que foram contratados entre janeiro e junho de 2023, utilizando BETWEEN

# 13. Consultar o(s) funcionário(s) com data de contratação mais antiga, utilizando subquery

# 14. Calcular a média salarial por departamento e exibir os departamentos que tenham média maiores ou iguais a 6000

# 15. Calcular a diferença salarial entre o funcionário com o maior salário e o com o menor salário

# SELECT nome, quantidade from produtos where quantidade = (select min(quantidade) from produtos);