#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys

sys.path.append(".")  # noqa
import random

import operator as opfunc
import functools

from unittest import TestCase, main

from assembler.tokens import MAX_INT, MIN_INT, BITS
from assembler.assemble import assemble


NUM_TESTS = 100
MAX_SHIFT = BITS // 2
MIN_TEST = MIN_INT // 10  # right now we don't want to overflow!
MAX_TEST = MAX_INT // 10  # right now we don't want to overflow!
MAX_MUL = 10000  # right now we don't want to overflow!
MIN_MUL = -10000  # right now we don't want to overflow!
REGISTER_SIZE = BITS


class AssembleTestCase(TestCase):
    def __init__(self, machine, register_names, stack_top, stack_bottom, base=None):
        self.machine = machine
        self.register_names = register_names
        self.stack_top = stack_top
        self.stack_bottom = stack_bottom
        self.base = base

    #####################
    # Two Operand Tests #
    #####################

    def two_op_test(
        self,
        operator,
        instr,
        result_reg_name=None,
        low1=MIN_TEST,
        high1=MAX_TEST,
        low2=MIN_TEST,
        high2=MAX_TEST,
    ):
        """
        This common test_two_op was written by looking at the same
        fn across the other test_assemble files.
        """
        for i in range(0, NUM_TESTS):
            a = random.randint(high1, low1)
            b = random.randint(low2, high2)
            print(f"Using operands {a} and {b}")
            correct = operator(a, b)
            if len(self.register_names) != 2:
                raise TypeError("Expected two register names.")
            operand1, operand2 = self.register_names
            self.machine.registers[operand1] = a
            self.machine.registers[operand2] = b
            match self.machine.flavor:
                case "intel":
                    assemble(
                        instr + f" {operand1.lower()}, {operand2.lower()}", self.machine, base=self.base
                    )
                    self.assertEqual(self.machine.registers[operand1], correct)
                case "att":
                    assemble(
                        instr + f" %{operand2.lower()}, %{operand1.lower()}",
                        self.machine,
                        base=self.base
                    )
                    self.assertEqual(self.machine.registers[operand1], correct)
                case _:  # Works for MIPS variants and RISC
                    assemble(
                        "40000" + instr + f" {operand1}, {operand2}, {result_reg_name}",
                        self.machine,
                        base=self.base
                    )
                    self.assertEqual(self.machine.registers[result_reg_name], correct)

    def test_add(self):
        self.two_op_test(opfunc.add, "add")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "sub")

    def test_imul(self):
        self.two_op_test(
            opfunc.mul, "imul", low1=MIN_MUL, high1=MAX_MUL, low2=MIN_MUL, high2=MAX_MUL
        )

    def test_and(self):
        self.two_op_test(opfunc.and_, "and")

    def test_or(self):
        self.two_op_test(opfunc.or_, "or")

    def test_xor(self):
        self.two_op_test(opfunc.xor, "xor")

    def test_shl(self):
        self.two_op_test(
            opfunc.lshift, "shl", low1=MIN_MUL, high1=MAX_MUL, low2=0, high2=MAX_SHIFT
        )

    def test_shr(self):
        self.two_op_test(
            opfunc.rshift, "shr", low1=MIN_MUL, high1=MAX_MUL, low2=0, high2=MAX_SHIFT
        )

    ###################
    # Single Op Tests #
    ###################

    def one_op_test(self, operator, instr):
        for i in range(NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            correct = operator(a)
            self.machine.registers["EAX"] = a
            assemble(instr + " %eax", self.machine, base=self.base)
            self.assertEqual(self.machine.registers["EAX"], correct)

    def test_not(self):
        self.one_op_test(opfunc.inv, "not")

    def test_neg(self):
        self.one_op_test(opfunc.neg, "neg")

    def test_inc(self):
        inc = functools.partial(opfunc.add, 1)
        self.one_op_test(inc, "inc")

    def test_dec(self):
        dec = functools.partial(opfunc.add, -1)
        self.one_op_test(dec, "dec")

    ##################
    # Push / Pop     #
    ##################

    def test_push_and_pop(self):
        # Note: size(correct_stack) = size(stack + memory)
        correct_stack = [None] * (self.stack_top + 1)

        # Traverse the stack registers.
        for i in range(self.stack_top, self.stack_bottom - 1, -1):
            a = random.randint(MIN_TEST, MAX_TEST)
            correct_stack[i] = a
            self.machine.registers["EAX"] = a
            assemble("push %eax", self.machine, base=self.base)

        for i in range(self.stack_bottom, self.stack_top + 1):
            assemble("pop %ebx", self.machine, base=self.base)
            self.assertEqual(self.machine.registers["EBX"], correct_stack[i])

    ##################
    # Other          #
    ##################

    def test_mov(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            correct = a
            self.machine.registers["EAX"] = a
            assemble("mov $" + str(a) + ", %eax", self.machine, base=self.base)
            self.assertEqual(self.machine.registers["EAX"], correct)

    def test_idiv(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            d = random.randint(MIN_TEST, MAX_TEST)
            b = 0
            while b == 0:  # Divisor can't be zero.
                b = random.randint(MIN_TEST, MAX_TEST)
            correct_quotient = (opfunc.lshift(d, REGISTER_SIZE) + a) // b
            correct_remainder = (opfunc.lshift(d, REGISTER_SIZE) + a) % b
            self.machine.registers["EAX"] = a
            self.machine.registers["EDX"] = d
            self.machine.registers["EBX"] = b
            assemble("idiv %ebx", self.machine, base=self.base)
            self.assertEqual(self.machine.registers["EAX"], correct_quotient)
            self.assertEqual(self.machine.registers["EDX"], correct_remainder)

    def test_cmp_eq(self):
        self.machine.registers["EAX"] = 1
        self.machine.registers["EBX"] = 1
        self.machine.flags["ZF"] = 0
        self.machine.flags["SF"] = 0
        assemble("cmp %ebx, %eax", self.machine, base=self.base)
        self.assertEqual(self.machine.flags["ZF"], 1)
        self.assertEqual(self.machine.flags["SF"], 0)

    def test_cmp_l(self):
        self.machine.registers["EAX"] = 0
        self.machine.registers["EBX"] = 1
        self.machine.flags["ZF"] = 0
        self.machine.flags["SF"] = 0
        assemble("cmp %ebx, %eax", self.machine, base=self.base)
        self.assertEqual(self.machine.flags["ZF"], 0)
        self.assertEqual(self.machine.flags["SF"], 1)
