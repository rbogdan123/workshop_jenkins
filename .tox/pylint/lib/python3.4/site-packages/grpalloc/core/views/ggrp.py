#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The algorithm for calculating groups.

(c) 2015 by Detlef Kreuz.
"""

from __future__ import (
    division, absolute_import, print_function, unicode_literals)

import math
import random


ACCEPTABLE_BADNESS = 0.01


def group_sizes(number_of_participants, max_group_size):
    """Return a vector of group sizes."""
    assert number_of_participants > 0
    number_of_groups, remaining = divmod(
        number_of_participants, max_group_size)
    if remaining > 0:
        number_of_groups += 1
    average_group_size, remaining = divmod(
        number_of_participants, number_of_groups)
    return [average_group_size] * (number_of_groups - remaining) + [
        average_group_size + 1] * remaining


# pylint: disable=too-few-public-methods
class Person(object):
    """Class for persons with their data and their dis/likes."""

    def __init__(self, _id, data):
        """Run when an instance of Person is created."""
        self._id = _id
        self.data = data
        self.likes = set()
        self.dislikes = set()

    def __repr__(self):
        """Print person with his or her id, data and likes."""
        return "Person(%s, (%s)), {%s}, {%s})" % (
            self._id, ",".join(str(v) for v in self.data),
            ",".join(str(v) for v in sorted(p.id for p in self.likes)),
            ",".join(str(v) for v in sorted(p.id for p in self.dislikes)))

    def __str__(self):
        """Return s string with his or her id and data."""
        return "Person %s%s" % (self._id, self.data)

    def __eq__(self, other):
        """Return boolean whether the id is the same."""
        return self._id == other.id

    def __hash__(self):
        """Return hash of the id."""
        return hash(self._id)


def create_data(tuple_size, max_points):
    """Create some random data for simulating data entered by users."""
    result = []
    max_rand = max_points
    for _ in range(tuple_size - 1):
        points = random.randint(1, max_rand) if max_rand > 0 else 0
        result.append(points)
        max_rand -= points
    result.append(max_rand)
    random.shuffle(result)
    return tuple(result)


def group_value(group):
    """Summarize the personality data of all persons in a group."""
    group_data = [person.data for person in group]
    return [sum(member) for member in zip(*group_data)]


class Candidate(object):
    """Class for the candidates (groups)."""

    def __init__(self, total_value, partition, assignment):
        """Run when an instance of Candidate is created."""
        self.total_value = total_value
        self.expected_value = sum(total_value) / len(total_value)
        self.partition = partition
        self.assignment = assignment
        self.badness = self._badness()

    def _badness(self):
        """Return the badness in dependence of the assignment."""
        badness = sum(self.group_badness(group) for group in self.groups())
        return badness / len(self.assignment)

    def groups(self):
        """Return a generator of all groups."""
        start_pos = 0
        for group_size in self.partition:
            yield self.assignment[start_pos:start_pos + group_size]
            start_pos += group_size

    def group_badness(self, group):
        """Return the badness of one group."""
        # First, the badness concerning the 8 roles.
        variance = sum(
            [abs(t - g) ** 2 for t, g in zip(
                self.total_value, group_value(group))])
        badness = max(
            0.9 * ACCEPTABLE_BADNESS, math.sqrt(variance) / self.expected_value
            )

        # Second, adjust badness with respect to likes and dislikes.
        group_set = set(group)
        for person in group:
            for like in person.likes:
                if like in group_set:
                    badness /= 1.05
            for dislike in person.dislikes:
                if dislike in group_set:
                    badness *= 1.1
        return badness

    def mutate(self, mutations):
        """Return a new candidate that is a mutation of the current one."""
        mutated_assignment = list(self.assignment)
        for _ in range(mutations):
            pos_1 = random.randint(0, len(mutated_assignment) - 1)
            pos_2 = random.randint(0, len(mutated_assignment) - 1)
            mutated_assignment[pos_1], mutated_assignment[pos_2] = \
                mutated_assignment[pos_2], mutated_assignment[pos_1]
        return Candidate(self.total_value, self.partition, mutated_assignment)

    def crossover(self, other):
        """Return a child based on the current and the other candidate."""
        if len(self.partition) < 2 or self == other:
            return None
        split_pos = random.randint(1, len(self.assignment) - 2)
        new_child = self.assignment[0:split_pos]
        new_child_set = set(new_child)
        for person in other.assignment:
            if person not in new_child_set:
                new_child.append(person)
        return Candidate(self.total_value, self.partition, new_child)


def build_initial_population(participants, max_group_size, population_size):
    """Return the population."""
    total_value = group_value(participants)
    partition = group_sizes(len(participants), max_group_size)
    assignment = list(participants)
    population = []
    for _ in range(population_size):
        random.shuffle(assignment)
        candidate = Candidate(total_value, partition, assignment)
        population.append(candidate)
    return population


def best_of_population(population):
    """Return the result of the best population."""
    result = population[0]
    for candidate in population:
        if candidate.badness < result.badness:
            result = candidate
    return result


def crossover_population(population, crossover_count):
    """Cross the population and return it."""
    new_population = list(population)  # Copy previous population
    for _ in range(crossover_count):
        candidate = random.choice(population)
        child = candidate.crossover(random.choice(population))
        if child is not None:
            new_population.append(child)
    return new_population


def mutate_population(population, mutations):
    """Mutate the population."""
    random.shuffle(population)
    for i in range(min(mutations, len(population))):
        population[i] = population[i].mutate(i)


def reduce_population(population, population_size):
    """Reduce the population."""
    while len(population) > population_size:
        cand_pos_1 = random.randint(0, len(population) - 1)
        while True:
            cand_pos_2 = random.randint(0, len(population) - 1)
            if cand_pos_1 != cand_pos_2:
                break
        diff = population[cand_pos_1].badness - population[cand_pos_2].badness
        if diff > 0:
            del population[cand_pos_1]
        elif diff < 0:
            del population[cand_pos_2]
        else:
            del population[random.choice([cand_pos_1, cand_pos_2])]


# pylint: disable=invalid-name
def partition_group(participants, max_group_size):
    """Return the calculated groups."""
    MAX_POPULATION_SIZE = max(20, int(len(participants) * 2))
    MIN_POPULATION_SIZE = max(10, int(len(participants) / 5))
    MIN_CROSSOVER_COUNT = 5
    MIN_MUTATIONS = 3
    MAX_NO_IMPROVEMENTS = 100

    population_size = int((MAX_POPULATION_SIZE - MIN_POPULATION_SIZE) / 2)
    population = build_initial_population(
        participants, max_group_size, population_size)
    best_candidate = population[0]
    waiting = 0
    for _ in range(2000):
        candidate = best_of_population(population)
        if candidate.badness < ACCEPTABLE_BADNESS:
            break
        if best_candidate.badness < candidate.badness:
            population.append(best_candidate)
            continue
        if best_candidate.badness != candidate.badness:
            population_size = max(
                population_size - waiting + 1, MIN_POPULATION_SIZE)
            best_candidate = candidate
            waiting = 0
            continue
        waiting += 1
        if waiting > MAX_NO_IMPROVEMENTS:
            break
        if waiting > 5:
            population_size = min(population_size + 1, MAX_POPULATION_SIZE)

        crossover_count = max(MIN_CROSSOVER_COUNT, population_size)
        mutations = max(MIN_MUTATIONS, int(population_size / 5))

        population = crossover_population(population, crossover_count)
        mutate_population(population, mutations)
        reduce_population(population, population_size)
    return candidate


def main(participants, max_group_size):
    """The function who gets called from the project. Return the groups."""
    return partition_group(participants, max_group_size)
