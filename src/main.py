#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from random import random
from random import randint
import filereader

debug = False


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
			prefix = words[i: i + 1];
			body = words[i + 1: i + order]
			key = " ".join(prefix + body)
			postfix = words[i + order:i + order + 1] #it is single
			key_value.append((key, prefix, body, postfix))

		#-hack? -no
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
				if debug: print "Added next node to: ", self.nodes[kv[0]].token, " this node: ", " ".join(
					kv[2] + [postfix]), " with probability: ", probability, " with reference: ", postfix
				self.nodes[kv[0]].add_node(self.nodes[" ".join(kv[2] + [postfix])], probability, postfix)


def main():
	words = filereader.read_grf()

	markov = Markov(words, 3)
	rnd = randint(0, len(markov.nodes) - 1)
	node = markov.nodes.values()[rnd];
	while not (node.token[0].isupper()):
		rnd = randint(0, len(markov.nodes) - 1)
		node = markov.nodes.values()[rnd];

	print node.token,

	dots = 0
	for i in range(10000):
		next_node = node.next_node()
		if len(node.next) == 0: return #final node
		next_token = next_node[1]
		print next_token,
		node = next_node[0]
		if next_token == ".": dots += 1
		if dots == 3: return #enough


if __name__ == '__main__':
	main()
