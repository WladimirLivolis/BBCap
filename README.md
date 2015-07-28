### DESENVOLVIMENTO DE UMA TÉCNICA DE MEDIÇÃO ATIVA E NÃO-COOPERATIVA PARA AFERIR QUALIDADE DE BANDA LARGA FIXA

##### Etapas:

- I   - *Traceroute*
- II  - *Envio das sondas*
- III - *Cálculo da capacidade*

#### <<<<<<<<<< ALGORITMO >>>>>>>>>>
```
1. Executa traceroute para calcular o número de saltos K até o destino;
2. Envia 2 grupos de trens de pacotes para o destino:
	2.1 Grupo 1:
		2.1.1 Para cada trem de pacotes do grupo 1:
			2.1.1.1 UM pacote (LOCOMOTIVA)* é enviado: tamanho = 1500 bytes (MTU) e TTL = K - 1;
			2.1.1.2 UM ou MAIS pacotes (VAGÕES)* são enviados: tamanho = 500 bytes e TTL = K;
			2.1.1.3 UM pacote (CABOOSE) é enviado: tamanho = 44 bytes e TTL = K;
			2.1.1.4 Retorna RTT = tempo entre o envio da locomotiva e a resposta ao envio do caboose;
		2.1.2 Retorna menor RTT (rrt1).
	2.2 Grupo 2:
		2.2.1 Para cada trem de pacotes do grupo 2:
			2.2.1.1 UM pacote (LOCOMOTIVA)* é enviado: tamanho = 1500 bytes (MTU) e TTL = K - 1;
			2.2.1.2 UM ou MAIS pacotes (VAGÕES)* são enviados: tamanho = 50 bytes e TTL = K;
			2.2.1.3 UM pacote (CABOOSE) é enviado: tamanho = 44 bytes e TTL = K;
			2.2.1.4 Retorna RTT = tempo entre o envio da locomotiva e a resposta ao envio do caboose;
		2.2.2 Retorna menor RTT (rrt2).
3. Calcula capacidade do enlace no último salto: C = N*(TAM1-TAM2)*8/(rrt1-rtt2),
                                                onde N = número de vagões por trem,
                                                    TAM1 = tamanho em bytes de um vagão no grupo 1,
                                                    TAM2 = tamanho em bytes de um vagão no grupo 2,
                                                    rrt1 > rrt2.

* Os pacotes LOCOMOTIVA e VAGÃO não geram resposta por serem pacotes ICMP ECHO REPLY.
```

#### PSEUDO-CÓDIGOS:
```
-------------------------------------------------------------
Algoritmo 1 - CalculaNumSaltos(destino)
-------------------------------------------------------------
ttl <- 1
NumSaltosExcedido <- Falso
DestinoAlcançado <- Falso
NumMaxSaltos <- 30
enquanto NÃO (NumSaltosExcedido OU DestinoAlcançado) faça
	envia_ICMP_Echo_Request(ttl, destino)
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
-------------------------------------------------------------

-------------------------------------------------------------
Algoritmo 2 - EnviaSondas(destino, NumTrens, NumVagoes)
-------------------------------------------------------------
NumSaltos <- CalculaNumSaltos(destino)

para i <- 1 até NumTrens faça
	envia_ICMP_Echo_Reply(1500, NumSaltos-1, destino)
	t1 <- tempo_atual()
	para j <- 1 até NumVagoes faça
	    envia_ICMP_Echo_Reply(500, NumSaltos, destino)
	fim-para
	envia_ICMP_Echo_Request(44, NumSaltos, destino)
	resposta <- recebePacote()
	t2 <- tempo_atual()
	rtt1[i] <- t2 - t1
fim-para
menor_rtt1 <- menorValor(rtt1)

para i <- 1 até NumTrens faça
	envia_ICMP_Echo_Reply(1500, NumSaltos-1, destino)
	t1 <- tempo_atual()
	para j <- 1 até NumVagoes faça
	    envia_ICMP_Echo_Reply(50, NumSaltos, destino)
	fim-para
	envia_ICMP_Echo_Request(44, NumSaltos, destino)
	resposta <- recebePacote()
	t2 <- tempo_atual()
	rtt2[i] <- t2 - t1
fim-para
menor_rrt2 <- menorValor(rtt2)

capacidade <- CalculaCapacidade(NumVagoes,500,50,menor_rrt1,menor_rrt2)
retorna capacidade
-------------------------------------------------------------

-------------------------------------------------------------
Algoritmo 3 - CalculaCapacidade(Num,Tam1, Tam2, rrt1, rtt2)
-------------------------------------------------------------
capacidade <- Num*(Tam1-Tam2)*8/(rtt1-rtt2)
retorna capacidade
-------------------------------------------------------------
```
