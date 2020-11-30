# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def maior_que_direita(vetor):

	vetor_maior = []
	#vetor_maior = [i for i in vetor if vetor[i] > vetor[i+1]]
	for i in range(len(vetor)-1):
		if vetor[i] > vetor[i+1]:
			vetor_maior.append(vetor[i])
	vetor_maior.append(vetor[i+1])

	#if not vetor_maior:
		#vetor_maior = [vetor[len(vetor)-1]]

	print(vetor_maior)
	"""
	for elem in range(len(vetor)):
		if vetor[elem] > vetor[elem+1]:
			vetor_maior.append(vetor[elem])
	"""
	pass

def main():
    maior_que_direita([3, 13, 11, 2, 1, 9, 5])

    return

if __name__ == '__main__':
    main()
