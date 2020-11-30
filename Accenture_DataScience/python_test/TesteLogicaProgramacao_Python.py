## Abaixo se encontram as 4 quest�es do seu teste de L�gica de Programa��o.
## Implemente todas elas neste arquivo seguindo os padr�es da linguagem escolhida e utilizando os cabe�alhos das fun��es.
## As suas respostas ser�o corrigidas analisando a l�gica utilizada, a sua familiaridade com a linguagem e ser�o submetidas a casos de teste al�m dos exemplos presentes nesse arquivo.
## Vale lembrar que voc� tem at� 2 horas, a partir do recebimento do e-mail em hor�rio combinado anteriormente, para fazer o m�ximo de quest�es que conseguir.
## Por favor, confirme o recebimento deste teste antes de inici�-lo.
## Boa sorte!!


## Maior que os da sua direita.
# Crie uma fun��o que receba um vetor de n�meros inteiros positivos e retorne um vetor com cada n�mero que seja estritamente maior que todos os n�meros ap�s ele. Por exemplo, dado o vetor [5, 9, 8, 7], � retornado [9, 8, 7], pois 9 � maior que 8 e 7, 8 � maior que 7 e 7 � o �ltimo elemento, por consequ�ncia, n�o h� ningu�m maior que ele � sua direita. J� para o vetor [3, 3, 4], � retornado apenas [4], o 3 n�o � retornado pois n�o pode ser igual, apenas maior.


## Exemplos Python:
# >>> maior_que_direita([3, 13, 11, 2, 1, 9, 5])
# >>> [13, 11, 9, 5]
#
# >>> maior_que_direita([5, 5, 5, 5, 5, 5])
# >>> [5]
#
# >>> maior_que_direita([5, 9, 8, 7])
# >>> [9, 8, 7]
#
# >>> maior_que_direita([1, 2, 3])
# >>> [3]


def maior_que_direita(vetor):

	vetor_maior = []

	for i in range(len(vetor)-1):
		if vetor[i] > vetor[i+1]:
			vetor_maior.append(vetor[i])
	vetor_maior.append(vetor[i+1])

	return vetor_maior


## O Estranho do Grupo
# Escreva uma fun��o que recebe uma lista com no m�nimo tr�s palavras e retorne "Verdadeiro" caso exatamente uma palavra na lista tenha tamanho diferente em rela��o �s outras. Retorne Falso, caso contr�rio. Por exemplo, na lista ["Mais","Menos","Nada","Muito"] tem duas palavras com 4 letras e outras duas com 5, ent�o � retornado Falso. J� na lista ["c�co","�gua","casa","praia"], apenas uma palavra cont�m 5 letras e todas as outras cont�m 4.


## Exemplos Python:
# >>> estranho_grupo(["c�co","�gua","casa","praia"])
# >>> Verdadeiro
#
# >>> estranho_grupo(["prova","certo","errado"])
# >>> Verdadeiro
#
# >>> estranho_grupo(["vento","ventania","ventilador"])
# >>> Falso
#
# >>> estranho_grupo(["Mais","Menos","Nada","Muito"])
# >>> Falso


def estranho_grupo(vetor):
	from collections import Counter

	word_len = []
	# count = []

	for word in vetor:
		word_len.append(len(word))

	unique = list(set(word_len))

	if len(unique) != 2:
		return False

	ocurrences = Counter(word_len)
	if ocurrences[unique[0]] == 1:
		return True
	elif ocurrences[unique[1]] == 1:
		return True
	else:
		return False

	pass


## Dist�ncia Vogal
# Escreva uma fun��o que recebe uma string e retorne uma outra string onde cada caracter � trocado pela sua dist�ncia at� a vogal mais pr�xima. Por exemplo, para a palavra "chama" deve ser retornado "21010", pois o 'c' est� a 2 caracteres da vogal mais pr�xima, o 'a', o 'h' est� a 1 s�, e assim por diante. Vale destacar que quando o caracter em si � um vogal, � retornado um 0 para ele.


## Exemplos Python:
# >>> distancia_vogal("aaaaa")
# >>> "00000"
#
# >>> distancia_vogal("babbb")
# >>> "10123"
#
# >>> distancia_vogal("abcdabcd")
# >>> "01210123"
#
# >>> distancia_vogal("shopper")
# >>> "2101101"


def distancia_vogal(palavra):
	pass


## Menor Inteiro
# Dado uma lista de n�meros inteiros, crie uma fun��o que ache o menor n�mero inteiro positivo que � igualmente divisivel por todos os n�meros dentro da lista. Em outras palavras, encontre o menor m�ltiplo comum.


## Exemplos Python:
# >>> menor_inteiro([1, 2, 3, 4, 5, 6, 7, 8, 9])
# >>> 2520
#
# >>> menor_inteiro([5])
# >>> 5
#
# >>> menor_inteiro([5, 7, 11])
# >>> 385
#
# >>> menor_inteiro([5, 7, 11, 35, 55, 77])
# >>> 385


def menor_inteiro(numero):
	from math import gcd

	lcm = numero[0]

	for i in numero[1:]:
		lcm = lcm*i//gcd(lcm,i)

	return lcm
