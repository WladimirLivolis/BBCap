### DESENVOLVIMENTO DE UMA TÉCNICA DE MEDIÇÃO ATIVA E NÃO-COOPERATIVA PARA AFERIR QUALIDADE DE BANDA LARGA FIXA

##### Etapas:

- I - *Traceroute*
- II - *Envio das sondas*
- III - *Cálculo da capacidade*

#### <<<<<<<<<< ALGORITMO >>>>>>>>>>
```
1. Executa traceroute para calcular o número de saltos K até o destino;
2. Envia 2 grupos de 50 trios de pacotes para o destino:
	2.1 Grupo 1:
		2.1.1 Para cada trio de pacotes do grupo 1:
			2.1.1.1 Pacote 1*   possui tamanho 1500 bytes (MTU) e TTL = K - 1;
			2.1.1.2 Pacote 2**  possui tamanho 500 bytes e TTL = K;
			2.1.1.3 Pacote 3*** possui tamanho ZERO e TTL = K;
			2.1.1.4 Retorna RTT = tempo entre o envio do primeiro pacote e a resposta ao terceiro pacote;
		2.1.2 Retorna menor RTT (rrt1).
	2.2 Grupo 2:
		2.2.1 Para cada trio de pacotes do grupo 2:
			2.2.1.1 Pacote 1*   possui tamanho 1500 bytes (MTU) e TTL = K - 1;
			2.2.1.2 Pacote 2**  possui tamanho 50 bytes e TTL = K;
			2.2.1.3 Pacote 3*** possui tamanho ZERO e TTL = K;
			2.2.1.4 Retorna RTT = tempo entre o envio do primeiro pacote e a resposta ao terceiro pacote;
		2.2.2 Retorna menor RTT (rrt2).
3. Calcula capacidade do enlace no último salto: C = (500-50)*8/(rrt1-rtt2) [CONDIÇÃO: rrt1 > rrt2].

*   Os pacotes 1 de cada trio de pacotes não geram resposta por possuirem TTL < K ou por serem pacotes malformados.
**  Os pacotes 2 de cada trio de pacotes não geram resposta por serem pacotes malformados.
*** Os pacotes 3 de cada trio de pacotes possuem tamanho igual ao tamanho de seus headers.
```

#### PSEUDO-CÓDIGOS:
```
--------------------------------------------------------
Algoritmo 1 - CalculaNumSaltos(destino)
--------------------------------------------------------
ttl <- 1
NumSaltosExcedido <- Falso
DestinoAlcançado <- Falso
NumMaxSaltos <- 30
enquanto (NÃO NumSaltosExcedido) E (NÃO DestinoAlcançado) faça
	enviaPacoteICMP(ttl, destino)
	resposta <- recebePacote()
	endereço <- obtemEndereco(resposta)
	se endereço IGUAL destino então
		DestinoAlcançado <- Verdadeiro
	senão
		ttl <- ttl + 1
		se ttl MAIOR NumMaxSaltos então
			NumSaltosExcedido <- Verdadeiro
		fim-se
	fim-se
fim-enquanto
se DestinoAlcançado então
	retorna ttl
senão
	retorna -1
fim-se
--------------------------------------------------------

--------------------------------------------------------
Algoritmo 2 - EnviaSondas(destino)
--------------------------------------------------------
NumSaltos <- CalculaNumSaltos(destino)

para i <- 1 até 50 faça
	enviaPacoteMalformado(1500, NumSaltos-1, destino)
	t1 <- tempo_atual()
	enviaPacoteMalformado(500, NumSaltos, destino)
	enviaPacoteICMP(0, NumSaltos, destino)
	respostaP3 <- recebePacote()
	t3 <- tempo_atual()
	rtt1[i] <- t3 - t1
fim-para
menor_rtt1 <- menorValor(rtt1)

para j <- 1 até 50 faça
	enviaPacoteMalformado(1500, NumSaltos-1, destino)
	t1 <- tempo_atual()
	enviaPacoteMalformado(50, NumSaltos, destino)
	enviaPacoteICMP(0, NumSaltos, destino)
	respostaP3 <- recebePacote()
	t3 <- tempo_atual()
	rtt2[j] <- t3 - t1
fim-para
menor_rrt2 <- menorValor(rtt2)

capacidade <- CalculaCapacidade(500,50,menor_rrt1,menor_rrt2)
retorna capacidade
--------------------------------------------------------

--------------------------------------------------------
Algoritmo 3 - CalculaCapacidade(Tam1, Tam2, rrt1, rtt2)
--------------------------------------------------------
cap <- (Tam1-Tam2)*8/(rtt1-rtt2)
retorna cap
--------------------------------------------------------
```
