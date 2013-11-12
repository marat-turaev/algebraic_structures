# -*- coding: utf-8 -*-
from __future__ import division
from random import random
from random import randint
import filereader

class MarkovNode(object):
	def __init__(self, token):
		self.token = token
		self.next = []
	def add_node(self, node, probability, reference_word):
		self.next.append((node, probability, reference_word))
	def next_node(self):
		rnd = random()
		for node in self.next:
			if rnd <= node[1]:
				return (node[0], node[2])
			rnd -= node[1]

class Markov(object):
	def __init__(self, words, order):
		self.order = order
		self.nodes = {}
		matrix = {}
		key_value = [] 
		for i in range(len(words) - order):
			prefix = words[i : i+1];
			body = words[i+1 : i+order]
			key = " ".join(prefix + body)
			postfix = words[i+order:i+order+1] #it is single
			key_value.append((key, prefix, body, postfix))

		#hack?
		last = " ".join(words[-order:]);
		self.nodes[last] = MarkovNode(last)

		for kv in key_value:
			self.nodes[kv[0]] = MarkovNode(kv[0])
		for kv in key_value:
			matrix[kv[0]] = {}
		for kv in key_value:
			matrix[kv[0]][kv[3][0]] = 0
		for kv in key_value:
			matrix[kv[0]][kv[3][0]] += 1
		for kv in key_value:
			if len(self.nodes[kv[0]].next) != 0: continue
			total_references = sum(matrix[kv[0]].values())
			for postfix in matrix[kv[0]].keys():
				probability = matrix[kv[0]][postfix] / total_references;
				print "Added next node to: ", self.nodes[kv[0]].token, " this node: ", " ".join(kv[2] + [postfix]), " with probability: ", probability, " with reference: ", postfix
				self.nodes[kv[0]].add_node(self.nodes[" ".join(kv[2] + [postfix])], probability, postfix)

def main():

	# words = ["a", "b", ",", "a", "b", "c", ",", "b"]
	words = filereader.read_grf()

	markov = Markov(words, 2)
	rnd = randint(0, len(markov.nodes)-1)
	node = markov.nodes.values()[rnd];	
	while not (node.token.startswith('Доказать') or node.token.startswith('Пусть')):
		rnd = randint(0, len(markov.nodes)-1)
		node = markov.nodes.values()[rnd];	

	# node = markov.nodes.itervalues().next();#markov.nodes["a"];
	print node.token, 

	for i in range(100):
		next_node = node.next_node()
		if len(node.next) == 0: return #final node
		print next_node[1],
		node = next_node[0]



if __name__ == '__main__':
	main()