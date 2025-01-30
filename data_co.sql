CREATE DATABASE vendas_dataco;
USE vendas_dataco;

-- Tabela de vendas
CREATE TABLE vendas (
	id_venda INT,
    produto VARCHAR(45),
    quantidade INT,
    preco_unitario DECIMAL(10,2),
    data_venda DATE
);

ALTER TABLE vendas MODIFY COLUMN id_venda INT AUTO_INCREMENT PRIMARY KEY;
ALTER TABLE vendas ADD COLUMN Comissão DECIMAL(10,2);

SELECT * FROM vendas;