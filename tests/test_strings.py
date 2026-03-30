#!/usr/bin/env python3
"""Test string handling with bstr (length-prefixed strings)"""
import subprocess
import pytest
import tempfile
import os
from conftest import ROOT, PYTHON, TRANSPILE, run_bf, PREPROCESS

def transpile(source):
    # Write source to temp file for preprocess
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(source)
        f.flush()
        temp_file = f.name
    
    try:
        # First preprocess
        pre_result = subprocess.run([PYTHON, PREPROCESS, temp_file],
                                   capture_output=True, text=True)
        if pre_result.returncode != 0:
            print(f"Preprocess error: {pre_result.stderr}")
            return ""
        
        # Parse preprocessed file from output like "Pre-processed: x.py -> x.pre.py"
        pre_file = None
        for line in pre_result.stdout.strip().split('\n'):
            if '->' in line:
                pre_file = line.split('->')[-1].strip()
                break
        
        if pre_file and os.path.exists(pre_file):
            with open(pre_file) as f:
                preprocessed = f.read()
        else:
            preprocessed = source
        
        # Then transpile
        result = subprocess.run([PYTHON, TRANSPILE], input=preprocessed, 
                               capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Transpile error: {result.stderr}")
            return ""
        return result.stdout
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass


class TestStringLiterals:
    """Phase 1: String literal variables - basic building blocks"""

    def test_string_assign_no_output(self):
        """Assigning a string should not produce output"""
        bf = transpile('s = "hi"')
        output = run_bf(bf)
        assert output == "", f"Expected '', got '{output}'"

    def test_string_print_variable(self):
        """Print a string variable"""
        bf = transpile('s = "hi"\nprint(s)')
        output = run_bf(bf)
        assert output == "hi", f"Expected 'hi', got '{output}'"

    def test_string_two_chars(self):
        """String with two characters"""
        bf = transpile('s = "ab"\nprint(s)')
        output = run_bf(bf)
        assert output == "ab", f"Expected 'ab', got '{output}'"

    def test_string_three_chars(self):
        """String with three characters"""
        bf = transpile('s = "abc"\nprint(s)')
        output = run_bf(bf)
        assert output == "abc", f"Expected 'abc', got '{output}'"

    def test_string_empty(self):
        """Empty string should print nothing"""
        bf = transpile('s = ""\nprint(s)')
        output = run_bf(bf)
        assert output == "", f"Expected '', got '{output}'"

    def test_string_hello(self):
        """Classic hello world test"""
        bf = transpile('s = "Hello"\nprint(s)')
        output = run_bf(bf)
        assert output == "Hello", f"Expected 'Hello', got '{output}'"

    def test_string_space(self):
        """String with space character"""
        bf = transpile('s = "a b"\nprint(s)')
        output = run_bf(bf)
        assert output == "a b", f"Expected 'a b', got '{output}'"

    def test_string_print_twice(self):
        """Print same string twice"""
        bf = transpile('s = "hi"\nprint(s)\nprint(s)')
        output = run_bf(bf)
        assert output == "hihi", f"Expected 'hihi', got '{output}'"


class TestStringMultiple:
    """Multiple string variables"""

    def test_two_string_vars(self):
        """Two different string variables"""
        bf = transpile('a = "hi"\nb = "yo"\nprint(a)\nprint(b)')
        output = run_bf(bf)
        assert output == "hiyo", f"Expected 'hiyo', got '{output}'"

    def test_string_var_reuse(self):
        """Reassign and print"""
        bf = transpile('s = "one"\nprint(s)\ns = "two"\nprint(s)')
        output = run_bf(bf)
        assert output == "onetwo", f"Expected 'onetwo', got '{output}'"


class TestStringConcat:
    """Phase 2: String concatenation (compile-time)"""

    def test_string_concat_two(self):
        """Concatenate two string literals"""
        bf = transpile('print("hello" + "world")')
        output = run_bf(bf)
        assert output == "helloworld", f"Expected 'helloworld', got '{output}'"

    def test_string_concat_three(self):
        """Concatenate three string literals"""
        bf = transpile('print("a" + "b" + "c")')
        output = run_bf(bf)
        assert output == "abc", f"Expected 'abc', got '{output}'"

    def test_string_concat_with_char(self):
        """Concatenate string with chr()"""
        bf = transpile('print("hi" + chr(33))')
        output = run_bf(bf)
        assert output == "hi!", f"Expected 'hi!', got '{output}'"


class TestStringProperties:
    """Phase 3: String properties (len, indexing)"""

    def test_len_simple(self):
        """Get length of a string"""
        bf = transpile('s = "hi"\nn = len(s)\nprint(chr(n + 48))')
        output = run_bf(bf)
        # n=2, chr(50)='2' - convert digit to ASCII for printing
        assert output == "2", f"Expected '2', got '{output}'"

    def test_len_empty(self):
        """Length of empty string is 0"""
        bf = transpile('s = ""\nn = len(s)\nprint(chr(n + 48))')
        output = run_bf(bf)
        # n=0, chr(48)='0' - convert digit to ASCII for printing
        assert output == "0", f"Expected '0', got '{output}'"

    def test_index_first(self):
        """First character of string"""
        bf = transpile('s = "abc"\nc = s[0]\nprint(chr(c))')
        output = run_bf(bf)
        # 'a' = 97
        assert output == "a", f"Expected 'a', got '{output}'"

    def test_index_second(self):
        """Second character of string"""
        bf = transpile('s = "abc"\nc = s[1]\nprint(chr(c))')
        output = run_bf(bf)
        # 'b' = 98
        assert output == "b", f"Expected 'b', got '{output}'"


class TestStringInput:
    """Phase 4: String input (final stage)"""

    def test_input_single_char(self):
        """Input a single character into string"""
        bf = transpile('s = input()\nprint(s)')
        output = run_bf(bf, 'A')
        assert output == "A", f"Expected 'A', got '{output}'"

    def test_input_multiple_chars(self):
        """Input multiple characters into string"""
        bf = transpile('s = input()\nprint(s)')
        output = run_bf(bf, 'test')
        assert output == "test", f"Expected 'test', got '{output}'"

    def test_input_echo(self):
        """Input and echo back"""
        bf = transpile('name = input()\nprint("Hello " + name)')
        output = run_bf(bf, 'Bob')
        assert output == "Hello Bob", f"Expected 'Hello Bob', got '{output}'"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
