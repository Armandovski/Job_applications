def estranho_grupo(vetor):
	from collections import Counter

	word_len = []
	count = []

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


	"""
	if len(set(word_len)) == 2:
		return True
	else:
		return False
	"""
	pass

def main():
	value = estranho_grupo(["Mais","Menos","Nada","Muito"])

	print(value)
	return

if __name__ == '__main__':
	main()
