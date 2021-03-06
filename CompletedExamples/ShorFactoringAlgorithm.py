"""
Shor Factoring Algorithm

Simulates Shor's factoring algorithm on a classical machine.\n
Shor's factoring algorithm finds the factors of a composite number in
polynomial time :math:`O(\\log(N))`. For reference, using the classical Dixon's
factoring method, the optimal complexity is
:math:`O(\\exp(2\\sqrt{2}\\sqrt{\\log(N)\\log(\\log(N))}))`.\n
Further reading about Shor's factoring algorithm:\n
.. _Chemistry LibreTexts: https://chem.libretexts.org/Bookshelves/Physical_and_
    Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_
    Theoretical_Chemistry)/Quantum_Tutorials_(Rioux)/Quantum_Teleportation/
    381%3A_Factoring_Using_Shor's_Quantum_Algorithm
.. _minutephysics: https://www.youtube.com/watch?v=lvTqbM5Dq4Q
.. _Qiskit Lectures: https://www.youtube.com/watch?v=mAHC1dWKNYE
.. _Wikipedia: https://en.wikipedia.org/wiki/Shor%27s_algorithm
* `Chemistry LibreTexts`_
* `minutephysics`_
* `Qiskit Lectures`_
* `Wikipedia`_

Author: Alex Lim

Date of Initial Creation: October 20, 2021

"""

from random import randint

import numpy as np

from src.MiscFunctions import FactoringFunctions as FactorFuncs
from src.QuantumCircuitMatrix import QuantumCircuitMatrix as qcm

__author__ = "Alex Lim"
__credits__ = "Alex Lim"
__maintainer__ = "Alex Lim"


class ShorFactoringAlgorithm:
    """
    Simulates Shor's factoring algorithm on a classical machine.\n
    Shor's factoring algorithm finds the factors of a composite number in
    polynomial time :math:`O(\\log(N))`. For reference, using the classical
    Dixon's factoring method, the optimal complexity is
    :math:`O(\\exp(2\\sqrt{2}\\sqrt{\\log(N)\\log(\\log(N))}))`.\n
    Further reading about Shor's factoring algorithm:\n
    .. _Chemistry LibreTexts: https://chem.libretexts.org/Bookshelves/Physical_
        and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_
        and_Theoretical_Chemistry)/Quantum_Tutorials_(Rioux)/Quantum_
        Teleportation/381%3A_Factoring_Using_Shor's_Quantum_Algorithm
    .. _minutephysics: https://www.youtube.com/watch?v=lvTqbM5Dq4Q
    .. _Qiskit Lectures: https://www.youtube.com/watch?v=mAHC1dWKNYE
    .. _Wikipedia: https://en.wikipedia.org/wiki/Shor%27s_algorithm
    * `Chemistry LibreTexts`_
    * `minutephysics`_
    * `Qiskit Lectures`_
    * `Wikipedia`_
    """
    @staticmethod
    def c_amod15(a, power):
        """
        Controlled multiplication by a mod 15\n
        * Note: For example purposes, unnecessary for program to run

        :param a: Some number co-prime with 15
        :type a: int
        :param power: The number of times to repeat the controlled-U gate
        :type power: int
        :return: Controlled multiplication gate
        :rtype: np.ndarray
        """
        if a not in [2, 7, 8, 11, 13]:
            raise ValueError("'a' must be 2, 7, 8, 11 or 13")
        matrix_of_qubits = qcm.get_qubit_matrix(4)
        a = int(a)
        for iteration in range(power):
            if a in [2, 13]:
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 0, 1)
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 1, 2)
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 2, 3)
            if a in [7, 8]:
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 2, 3)
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 1, 2)
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 0, 1)
            if a == 11:
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 1, 3)
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 0, 2)
            if a in [7, 11, 13]:
                matrix_of_qubits = np.dot(np.kron(
                    qcm.Pauli_X_gate, np.identity(
                        int(matrix_of_qubits.shape[0] / qcm.Pauli_X_gate.shape[
                            0]))), matrix_of_qubits)
        return matrix_of_qubits

    @staticmethod
    def c_amodb(a, power, b):
        """
        Controlled multiplication by a mod b

        :param a: Some number co-prime with b
        :type a: int
        :param power: The number of times to repeat the controlled-U gate
        :type power: int
        :param b: The modulus
        :type b: int
        :return: Controlled multiplication gate
        :rtype: np.ndarray
        """
        if a not in [2, (b - 1) / 2, (b - 1) / 2 + 1, b - 4, b - 2]:
            raise ValueError("'a' must be 2, %i, %i, %i, or %i" %
                             (((b - 1) / 2), ((b - 1) / 2 + 1), b - 4, b - 2))
        matrix_of_qubits = qcm.get_qubit_matrix(4)
        a = int(a)
        for iteration in range(power):
            if a in [2, b - 2]:
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 0, 1)
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 1, 2)
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 2, 3)
            if a in [(b - 1) / 2, (b - 1) / 2 + 1]:
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 2, 3)
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 1, 2)
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 0, 1)
            if a == b - 4:
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 1, 3)
                matrix_of_qubits = qcm.\
                    applied_swap_gate(matrix_of_qubits, 0, 2)
            if a in [(b - 1) / 2, b - 4, b - 2]:
                matrix_of_qubits = np.dot(np.kron(
                    qcm.Pauli_X_gate, np.identity(
                        int(matrix_of_qubits.shape[0] / qcm.Pauli_X_gate.shape[
                            0]))), matrix_of_qubits)
        return matrix_of_qubits

    @staticmethod
    def qubitFactoringPeriodFinding(num: int = 15,
                                    a: int = 7,
                                    n_count: int = 8):
        """
        Uses Shor's factoring algorithm to compute the period

        :param num: A natural number
        :type num: int
        :param a: A guess factor
        :type a: int
        :param n_count: The number of counting qubits
        :type n_count: int
        :return: The period
        :rtype: int
        """
        QFT = qcm.quantum_Fourier_transform(n_count)
        QFT_dagger = qcm.invert_matrix(QFT)
        qc = np.zeros([n_count, n_count])
        for q in range(n_count):
            qc[q][q] += \
                (ShorFactoringAlgorithm.c_amodb(a, int(2**q), num))[q][q]
        qubit_matrix = \
            np.dot(np.kron(qc, np.identity(
                int(QFT_dagger.shape[0]/qc.shape[0]))), QFT_dagger)
        return int(qubit_matrix.sum(0).sum(0).real / 4)

    @staticmethod
    def qubitFactoringQiskit(num: int, limit: int = 1000,
                             show_errors: bool = False,
                             n_count: int = 8,
                             drawCircuitDiagram: bool = False):
        """
        Simulates Shor's factoring algorithm on a classical machine using
        Qiskit.\n
        This code is a modified version built using the following resources:\n
        .. _Qiskit textbook: https://qiskit.org/textbook/ch-algorithms/index.
            html
        .. _Qiskit lectures: https://www.youtube.com/watch?v=mAHC1dWKNYE
        * `Qiskit textbook`_
        * `Qiskit lectures`_

        :param num: A natural number
        :type num: int
        :param limit: The maximum number of attempts to find more factors,
            defaults to 1000 (the default for sys.getrecursionlimit())
        :param show_errors: Whether to show or ignore errors, defaults to False
        :type show_errors: bool
        :param n_count: The number of counting qubits, defaults to 8
        :type n_count: int
        :param drawCircuitDiagram: Whether to draw the circuit diagram,
            defaults to False
        :type drawCircuitDiagram: bool
        :return: The factorization of num
        :rtype: list
        """
        from QiskitExamples import QiskitShorFactoringAlgorithm as QkSFA
        return ShorFactoringAlgorithm.ShorFactoringAlgorithmClassical(
            num, limit, show_errors,
            QkSFA.QiskitShorFactoringAlgorithmGeneral, n_count,
            drawCircuitDiagram)

    @staticmethod
    def qubitFactoringQuantum(num: int, limit: int = 1000,
                              show_errors: bool = False):
        """
        Applies Shor's factoring algorithm to qubits

        :param num: A natural number
        :type num: int
        :param limit: The maximum number of attempts to find more factors,
            defaults to 1000 (the default for sys.getrecursionlimit())
        :param show_errors: Whether to show or ignore errors, defaults to False
        :type show_errors: bool
        :return: The factorization of num
        :rtype: list
        """
        return ShorFactoringAlgorithm.ShorFactoringAlgorithmClassical(
            num, limit, show_errors,
            ShorFactoringAlgorithm.qubitFactoringPeriodFinding)

    @staticmethod
    def ShorFactoringAlgorithmClassical(
            num: int, limit: int = 1000, show_errors: bool = False,
            func: type(FactorFuncs.period) = FactorFuncs.period, *args,
            quick_compute: bool = False):
        """
        Applies Shor's factoring algorithm using classical operations

        :param num: A natural number
        :type num: int
        :param limit: The maximum number of attempts to find more factors,
            defaults to 1000 (the default for sys.getrecursionlimit())
        :param show_errors: Whether to show or ignore errors, defaults to False
        :type show_errors: bool
        :param func: The period finding function to use with parameters
            (num, guessFactor),
            defaults to a classical period finding function at
            MiscFunctions.FactoringFunctions.period
        :type func: function
        :param args: The addition arguments to pass to func
        :param quick_compute: Whether to compute less factors with faster
            runtime, defaults to False
        :type quick_compute: bool
        :return: The factorization of num
        :rtype: list
        """
        factorization = list()
        while num % 2 == 0:
            factorization.append(2)
            num /= 2
        while num % 5 == 0:
            factorization.append(5)
            num /= 5
        for i in range(limit):
            if num == 1:
                factorization.append(int(num))
                while 1 in factorization:
                    factorization.remove(1)
                return sorted(factorization)
            if FactorFuncs.isqrt(num)**2 == num:
                factorization.append(int(np.sqrt(num)))
                factorization.append(int(np.sqrt(num)))
                num /= int(np.sqrt(num))**2
                factorization.append(int(num))
                while 1 in factorization:
                    factorization.remove(1)
                return sorted(factorization)
            guessFactor = num
            try:
                guessFactor = randint(3, int(num) - 1)
            except ValueError as message:
                if show_errors:
                    print("ValueError: ", message)
                continue
            try:
                if guessFactor != num and guessFactor % num != 0:
                    period = 1
                    try:
                        func_params = list()
                        func_params.append(num)
                        func_params.append(guessFactor)
                        for argv in args:
                            func_params.append(argv)
                        func_params = tuple(func_params)
                        period = func(*func_params)
                    except ValueError as message:
                        if show_errors:
                            print("ValueError: ", message)
                        continue
                    if period % 2 != 1:
                        if (guessFactor**(period / 2) + 1) % num != 0 and \
                                (guessFactor**(period / 2) - 1) % num != 0:
                            factorization.append(int(FactorFuncs.gcd(
                                int(guessFactor**(period / 2) + 1), num)))
                            factorization.append(int(FactorFuncs.gcd(
                                int(guessFactor**(period / 2) - 1), num)))
                            num /= FactorFuncs.gcd(
                                int(guessFactor**(period / 2) + 1), num)
                            num /= FactorFuncs.gcd(
                                int(guessFactor**(period / 2) - 1), num)
                            if period == 2:
                                factorization.append(int(FactorFuncs.gcd(
                                    int(guessFactor), num)))
                                num /= FactorFuncs.gcd(
                                    int(guessFactor), num)
                                factorization.append(int(FactorFuncs.gcd(
                                    int(guessFactor), num)))
                                num /= FactorFuncs.gcd(
                                    int(guessFactor), num)
                            if quick_compute:
                                factorization.append(int(num))
                                while 1 in factorization:
                                    factorization.remove(1)
                                return sorted(factorization)
            except OverflowError as message:
                if show_errors:
                    print("Unable to find factor #"
                          + str(len(factorization) + 1)
                          + " because ", message)
        factorization.append(int(num))
        while 1 in factorization:
            factorization.remove(1)
        return sorted(factorization)
