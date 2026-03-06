#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
sys.path.append(".") # noqa
import random

import operator as opfunc
import functools

from unittest import TestCase, main

from assembler.tokens import MAX_INT, MIN_INT, BITS
from assembler.assemble import assemble


NUM_TESTS = 100
MAX_SHIFT = BITS // 2
MIN_TEST = MIN_INT // 10   # right now we don't want to overflow!
MAX_TEST = MAX_INT // 10   # right now we don't want to overflow!
MAX_MUL = 10000  # right now we don't want to overflow!
MIN_MUL = -10000  # right now we don't want to overflow!
REGISTER_SIZE = BITS

class AssembleTestCase(TestCase):

    #####################
    # Two Operand Tests #
    #####################

    def two_op_test(self,
                    machine, operand_reg_names,
                    operator, instr,
                    result_reg_name=None,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST,):
      """
      This common test_two_op was written by looking at the same
      fn across the other test_assemble files. 
      """
      for i in range(0, NUM_TESTS):
          a = random.randint(low1, high1)
          b = random.randint(low2, high2)
          print(f'Using operands {a} and {b}')
          correct = operator(a, b)
          if len(operand_reg_names) != 2:
            raise TypeError('Expected two register names.')
          operand1, operand2 = operand_reg_names
          machine.registers[operand1] = a
          machine.registers[operand2] = b
          match machine.flavor:
            case 'intel':
              assemble(instr + f" {operand1.lower()}, {operand2.lower()}", machine)
              self.assertEqual(machine.registers[operand1], correct)
            case 'att':
              assemble(instr + f" %{operand2.lower()}, %{operand1.lower()}", machine)
              self.assertEqual(machine.registers[operand1], correct)
            case _: # Works for MIPS variants and RISC
              assemble("40000" + instr + f" {operand1}, {operand2}, {result_reg_name}", machine)
              self.assertEqual(machine.registers[result_reg_name], correct)
