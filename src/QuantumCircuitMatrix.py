"""
Quantum Circuit Matrix

Creates quantum circuits in the form of matrices.\n
Further reading about quantum logic gates:\n
.. _CWI Thesis On Quantum Computation Theory: https://www.illc.uva.nl/Research/
    Publications/Dissertations/DS-2002-04.text.pdf
.. _Wikipedia: https://en.wikipedia.org/wiki/Quantum_logic_gate
* `CWI Thesis On Quantum Computation Theory`_
* `Wikipedia`_

Author: Alex Lim

Date of Initial Creation: October 19, 2021

"""

import math

import numpy as np

from src.MiscFunctions import MiscFunctions as Misc

__author__      = "Alex Lim"
__credits__     = "Alex Lim"
__maintainer__  = "Alex Lim"


class QuantumCircuitMatrix:
    """
    Creates quantum circuits in the form of matrices.\n
    Further reading about quantum logic gates:\n
    .. _CWI Thesis On Quantum Computation Theory: https://www.illc.uva.nl/
        Research/Publications/Dissertations/DS-2002-04.text.pdf
    .. _Wikipedia: https://en.wikipedia.org/wiki/Quantum_logic_gate
    * `CWI Thesis On Quantum Computation Theory`_
    * `Wikipedia`_
    """
    def __init__(self):
        """Initializes quantum gates for use in this class"""
        self.one_qubit_identity_gate = None
        self.two_qubit_identity_gate = None
        self.Pauli_X_gate = None
        self.Pauli_Y_gate = None
        self.Pauli_Z_gate = None
        self.CNOT_gate = None
        self.Hadamard_gate = None
        self.H1_gate = None
        self.swap_gate = None

    @staticmethod
    def get_bra(*args: int or np.ndarray or str or bytes,
                qubit_string: str = "",
                show_errors: bool = False):
        """
        Gets the specified bra

        :param args: An individual bra
        :type args: int or np.ndarray or str or bytes
        :param qubit_string: A string of qubit bras
        :type qubit_string: str
        :param show_errors: Whether to show or ignore errors, defaults to False
        :type show_errors: bool
        :return: The combined bra, defaults to ⟨0|
        :rtype: np.ndarray
        """
        zero_bra = np.array([[1, 0]])  # ⟨0|
        one_bra = np.array([[0, 1]])   # ⟨1|
        plus_bra = zero_bra / np.sqrt(2) + one_bra / np.sqrt(2)   # ⟨+|
        minus_bra = zero_bra / np.sqrt(2) - one_bra / np.sqrt(2)  # ⟨-|
        bra = 1
        if len(args) != 0:
            for argv in args[::-1]:
                if isinstance(argv, np.ndarray):
                    bra = np.kron(argv, bra)
                elif isinstance(argv, str):
                    braTEMP = QuantumCircuitMatrix.get_bra(qubit_string=argv)
                    bra = np.kron(braTEMP, bra)
                elif not isinstance(argv, int):
                    try:
                        argv = int(argv)
                    except TypeError as message:
                        if show_errors:
                            print("TypeError: ", message)
                        continue
                if isinstance(argv, int):
                    if argv == 0:
                        bra = np.kron(zero_bra, bra)
                    elif argv == 1:
                        bra = np.kron(one_bra, bra)
                    else:
                        num_qubits = 1
                        while QuantumCircuitMatrix.\
                                qubits_to_bits(num_qubits) < argv:
                            num_qubits += 1
                        bra = np.kron(QuantumCircuitMatrix.
                                      get_qubit_vector(num_qubits, argv), bra)
        if len(qubit_string) != 0:
            braTEMP = 1
            for q in qubit_string:
                if q == "0":
                    q_bra = zero_bra
                elif q == "1":
                    q_bra = one_bra
                elif q == "+":
                    q_bra = plus_bra
                elif q == "-":
                    q_bra = minus_bra
                else:
                    raise ValueError("get_bra does not support \"%s\". "
                                     "Please try get_qubit_vector "
                                     "or directly use numpy ndarrays." % q)
                braTEMP = np.kron(q_bra, braTEMP)
            if not isinstance(bra, np.ndarray) and bra == 1:
                bra = braTEMP
            else:
                bra = np.kron(braTEMP, bra)
        if not isinstance(bra, np.ndarray) and bra == 1:
            return zero_bra
        return bra

    @staticmethod
    def get_ket(*args: int or np.ndarray or str or bytes,
                qubit_string: str = "",
                show_errors: bool = False):
        """
        Gets the specified ket

        :param args: An individual ket
        :type args: int or np.ndarray or str or bytes
        :param qubit_string: A string of qubit kets
        :type qubit_string: str
        :param show_errors: Whether to show or ignore errors, defaults to False
        :type show_errors: bool
        :return: The combined ket, defaults to |0⟩
        :rtype: np.ndarray
        """
        zero_ket = np.array([[1],
                             [0]])  # |0⟩
        one_ket = np.array([[0],
                            [1]])   # |1⟩
        plus_ket = zero_ket / np.sqrt(2) + one_ket / np.sqrt(2)   # |+⟩
        minus_ket = zero_ket / np.sqrt(2) - one_ket / np.sqrt(2)  # |-⟩
        ket = 1
        if len(args) != 0:
            for argv in args[::-1]:
                if isinstance(argv, np.ndarray):
                    ket = np.kron(argv, ket)
                elif isinstance(argv, str):
                    ketTEMP = QuantumCircuitMatrix.get_ket(qubit_string=argv)
                    ket = np.kron(ketTEMP, ket)
                elif not isinstance(argv, int):
                    try:
                        argv = int(argv)
                    except TypeError as message:
                        if show_errors:
                            print("TypeError: ", message)
                        continue
                if isinstance(argv, int):
                    if argv == 0:
                        ket = np.kron(zero_ket, ket)
                    elif argv == 1:
                        ket = np.kron(one_ket, ket)
                    else:
                        num_qubits = 1
                        while QuantumCircuitMatrix. \
                                qubits_to_bits(num_qubits) < argv:
                            num_qubits += 1
                        ket = np.kron(QuantumCircuitMatrix.
                                      get_qubit_vector(num_qubits, argv), ket)
        if len(qubit_string) != 0:
            ketTEMP = 1
            for q in qubit_string:
                if q == "0":
                    q_ket = zero_ket
                elif q == "1":
                    q_ket = one_ket
                elif q == "+":
                    q_ket = plus_ket
                elif q == "-":
                    q_ket = minus_ket
                else:
                    raise ValueError("get_ket does not support \"%s\". "
                                     "Please try get_qubit_vector "
                                     "or directly use numpy ndarrays." % q)
                ketTEMP = np.kron(q_ket, ketTEMP)
            if isinstance(ket, int) and ket == 1:
                ket = ketTEMP
            else:
                ket = np.kron(ketTEMP, ket)
        if isinstance(ket, int) and ket == 1:
            return zero_ket
        return ket

    @staticmethod
    def identity_gate(numQubits: int = 1):
        """
        Creates the identity gate using outer products.\n
        The identity gate is the identity matrix.

        :param numQubits: The number of qubits, defaults to 1
        :type numQubits: int
        :return: The identity gate
        :rtype: np.ndarray
        """
        return sum(QuantumCircuitMatrix.identity_gate_helper(numQubits))

    @staticmethod
    def identity_gate_helper(numQubits: int):
        """Helper method for identity_gate"""
        zero_prod = np.kron(QuantumCircuitMatrix.get_ket(0),
                            QuantumCircuitMatrix.get_bra(0))  # ⟨0|0⟩
        one_prod = np.kron(QuantumCircuitMatrix.get_ket(1),
                           QuantumCircuitMatrix.get_bra(1))   # ⟨1|1⟩
        if numQubits == 1:
            return [zero_prod, one_prod]
        identity_gate_list = list()
        for q in QuantumCircuitMatrix.identity_gate_helper(numQubits-1):
            identity_gate_list.append(np.kron(q, zero_prod))  # q ⊗ ⟨0|0⟩
            identity_gate_list.append(np.kron(q, one_prod))   # q ⊗ ⟨1|1⟩
        return identity_gate_list

    ### Identity gates ###
    """The identity gate is the identity matrix"""
    # Identity gate for a single qubit
    one_qubit_identity_gate = np.array([[1, 0],
                                        [0, 1]])
    """Identity gate for a single qubit"""
    # Identity gate for two qubits
    two_qubit_identity_gate = np.array([[1, 0, 0, 0],
                                        [0, 1, 0, 0],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]])
    """Identity gate for two qubits"""

    @staticmethod
    def Pauli_X_Gate():
        """
        Creates the Pauli-X gate using outer products:
        :math:`X = |1⟩⟨0| + |0⟩⟨1|`\n
        The Pauli gates (X, Y, Z) are the three Pauli matrices
        and act on a single qubit.\n
        The Pauli X, Y, and Z equate, respectively,
        to a rotation around the x, y, and z axes of the Bloch sphere
        by :math:`\pi` radians.

        :return: Pauli-X gate for a single qubit (equivalent to the NOT gate
            for classical computers with respect to the standard basis |0⟩,
            |1⟩)
        :rtype: np.ndarray
        """
        zero_bra = QuantumCircuitMatrix.get_bra(0)
        one_bra = QuantumCircuitMatrix.get_bra(1)
        zero_ket = QuantumCircuitMatrix.get_ket(0)
        one_ket = QuantumCircuitMatrix.get_ket(1)
        return np.kron(zero_bra, one_ket) + np.kron(zero_ket, one_bra)

    @staticmethod
    def Pauli_Y_Gate():
        """
        Creates the Pauli-Y gate using outer products:
        :math:`i|1⟩⟨0| - i|0⟩⟨1|`\n
        The Pauli gates (X, Y, Z) are the three Pauli matrices
        and act on a single qubit.\n
        The Pauli X, Y, and Z equate, respectively,
        to a rotation around the x, y, and z axes of the Bloch sphere
        by :math:`\pi` radians.

        :return: Pauli-Y gate for a single qubit
        :rtype: np.ndarray
        """
        zero_bra = QuantumCircuitMatrix.get_bra(0)
        one_bra = QuantumCircuitMatrix.get_bra(1)
        zero_ket = QuantumCircuitMatrix.get_ket(0)
        one_ket = QuantumCircuitMatrix.get_ket(1)
        return 1j * (np.kron(one_ket, zero_bra) - np.kron(zero_ket, one_bra))

    @staticmethod
    def Pauli_Z_Gate():
        """
        Creates the Pauli-Z gate using outer products:
        :math:`|0⟩⟨0| - |1⟩⟨1|`\n
        The Pauli gates (X, Y, Z) are the three Pauli matrices
        and act on a single qubit.\n
        The Pauli X, Y, and Z equate, respectively,
        to a rotation around the x, y, and z axes of the Bloch sphere
        by :math:`\pi` radians.

        :return: Pauli-Z gate for a single qubit
        :rtype: np.ndarray
        """
        zero_bra = QuantumCircuitMatrix.get_bra(0)
        one_bra = QuantumCircuitMatrix.get_bra(1)
        zero_ket = QuantumCircuitMatrix.get_ket(0)
        one_ket = QuantumCircuitMatrix.get_ket(1)
        return np.kron(zero_ket, zero_bra) - np.kron(one_ket, one_bra)

    @staticmethod
    def CU_Gate(U: np.ndarray):
        """
        Creates the controlled U gate using outer products:
        :math:`|0⟩⟨0| ⊗ |0⟩⟨0| + |0⟩⟨0| ⊗ |1⟩⟨1| + |1⟩⟨1| ⊗ U`\n

        :param U: A unitary qubit gate
        :type U: np.ndarray
        :return: The controlled U gate with the first qubit as the control
        :rtype: np.ndarray
        """
        zero_prod = np.kron(QuantumCircuitMatrix.get_bra(0),
                            QuantumCircuitMatrix.get_ket(0))  # ⟨0|0⟩
        one_prod = np.kron(QuantumCircuitMatrix.get_bra(1),
                           QuantumCircuitMatrix.get_ket(1))   # ⟨1|1⟩
        return np.kron(zero_prod, zero_prod)\
               + np.kron(zero_prod, one_prod)\
               + np.kron(one_prod, U)

    @staticmethod
    def CNOT_Gate():
        """
        Creates the controlled NOT gate using outer products:
        :math:`|0⟩⟨0| ⊗ |0⟩⟨0| + |0⟩⟨0| ⊗ |1⟩⟨1| + |1⟩⟨1| ⊗ X`\n
        maps the basis states |a,b⟩ ⟼ |a, a ⊕ b⟩, where ⊕ is XOR.

        :return: CNOT gate (or controlled Pauli-X gate)
        :rtype: np.ndarray
        """
        Pauli_X_gate = QuantumCircuitMatrix.Pauli_X_Gate()
        return QuantumCircuitMatrix.CU_Gate(Pauli_X_gate)

    @staticmethod
    def CY_Gate():
        """
        Creates the controlled Y gate using outer products:
        :math:`|0⟩⟨0| ⊗ |0⟩⟨0| + |0⟩⟨0| ⊗ |1⟩⟨1| + |1⟩⟨1| ⊗ Y`\n

        :return: CY gate (or controlled Pauli-Y gate)
        :rtype: np.ndarray
        """
        Pauli_Y_gate = QuantumCircuitMatrix.Pauli_Y_Gate()
        return QuantumCircuitMatrix.CU_Gate(Pauli_Y_gate)

    @staticmethod
    def CZ_Gate():
        """
        Creates the controlled Z gate using outer products:
        :math:`|0⟩⟨0| ⊗ |0⟩⟨0| + |0⟩⟨0| ⊗ |1⟩⟨1| + |1⟩⟨1| ⊗ Z`\n

        :return: CZ gate (or controlled Pauli-Z gate)
        :rtype: np.ndarray
        """
        Pauli_Z_gate = QuantumCircuitMatrix.Pauli_Z_Gate()
        return QuantumCircuitMatrix.CU_Gate(Pauli_Z_gate)

    ### Pauli gates ###
    # Pauli-X gate for a single qubit
    # (equivalent to the NOT gate for classical computers
    # with respect to the standard basis |0⟩, |1⟩)
    Pauli_X_gate = np.array([[0, 1],
                             [1, 0]])
    """
    Pauli-X gate for a single qubit (equivalent to the NOT gate for classical
    computers with respect to the standard basis |0⟩, |1⟩)\n
    The Pauli gates (X, Y, Z) are the three Pauli matrices
    and act on a single qubit.\n
    The Pauli X, Y, and Z equate, respectively,
    to a rotation around the x, y, and z axes of the Bloch sphere
    by :math:`\pi` radians.
    """

    # Pauli-Y gate for a single qubit
    Pauli_Y_gate = np.array([[0, -1j],
                             [1j, 0]])
    """
    Pauli-Y gate for a single qubit\n
    The Pauli gates (X, Y, Z) are the three Pauli matrices
    and act on a single qubit.\n
    The Pauli X, Y, and Z equate, respectively,
    to a rotation around the x, y, and z axes of the Bloch sphere
    by :math:`\pi` radians.
    """

    # Pauli-Z gate for a single qubit
    Pauli_Z_gate = np.array([[1, 0],
                             [0, -1]])
    """
    Pauli-Z gate for a single qubit\n
    The Pauli gates (X, Y, Z) are the three Pauli matrices
    and act on a single qubit.\n
    The Pauli X, Y, and Z equate, respectively,
    to a rotation around the x, y, and z axes of the Bloch sphere
    by :math:`\pi` radians.
    """

    # CNOT gate (or controlled Pauli-X gate)
    # maps the basis states |a,b⟩ ⟼ |a, a ⊕ b⟩, where ⊕ is XOR.
    CNOT_gate = np.kron(np.diag([1, 0]), one_qubit_identity_gate) + \
                np.kron(np.diag([0, 1]), Pauli_X_gate)
    """
    CNOT gate (or controlled Pauli-X gate)\n
    maps the basis states |a,b⟩ ⟼ |a, a ⊕ b⟩, where ⊕ is XOR.
    """

    # CY gate (or controlled Pauli-Y gate)
    CY_gate = np.kron(np.diag([1, 0]), one_qubit_identity_gate) + \
              np.kron(np.diag([0, 1]), Pauli_Y_gate)
    """CY gate (or controlled Pauli-Y gate)"""

    # CZ gate (or controlled Pauli-Z gate)
    CZ_gate = np.kron(np.diag([1, 0]), one_qubit_identity_gate) + \
              np.kron(np.diag([0, 1]), Pauli_Z_gate)
    """CZ gate (or controlled Pauli-Z gate)"""

    ### Hadamard gate ###
    @staticmethod
    def Hadamard_Gate():
        """
        Creates the Hadamard gate using outer products:
        :math:`H = |+⟩⟨0| + |-⟩⟨1|`\n
        Represents a rotation of :math:`\pi` about the axis
        :math:`(\\hat{x}+\\hat{z})/\\sqrt{2}` at the Bloch sphere.\n
        Maps the basis states
        (ie: creates a superposition if given a basis state):\n
        :math:`|0⟩ ⟼ (|0⟩+|1⟩)/\\sqrt{2}`\n
        :math:`|1⟩ ⟼ (|0⟩-|1⟩)/\\sqrt{2}`

        :return: The Hadamard gate for a single qubit
        :rtype: np.ndarray
        """
        zero_bra = QuantumCircuitMatrix.get_bra("0")
        one_bra = QuantumCircuitMatrix.get_bra("1")
        plus_ket = QuantumCircuitMatrix.get_ket("+")
        minus_ket = QuantumCircuitMatrix.get_ket("-")
        return np.kron(plus_ket, zero_bra) + np.kron(minus_ket, one_bra)

    # Hadamard gate for a single qubit
    Hadamard_gate = np.array([[1, 1],
                              [1, -1]]) / np.sqrt(2)
    """
    Hadamard gate for a single qubit\n
    Represents a rotation of :math:`\pi` about the axis
    :math:`(\\hat{x}+\\hat{z})/\\sqrt{2}` at the Bloch sphere.\n
    Maps the basis states
    (ie: creates a superposition if given a basis state):\n
    :math:`|0⟩ ⟼ (|0⟩+|1⟩)/\\sqrt{2}`\n
    :math:`|1⟩ ⟼ (|0⟩-|1⟩)/\\sqrt{2}`
    """

    # Hadamard transformation for a single qubit (or the Hermitian)
    H1_gate = np.kron(Hadamard_gate, one_qubit_identity_gate)
    """Hadamard transformation for a single qubit (or the Hermitian)"""

    @staticmethod
    def Swap_Gate():
        """
        Creates the swap gate using outer products:
        :math:`H = |00⟩⟨00| + |10⟩⟨01| + |01⟩⟨10| + |11⟩⟨11|`\n
        Swaps two qubits with respect to the basis |00⟩, |01⟩, |10⟩, |11⟩

        :return: The swap gate
        :rtype: np.ndarray
        """
        get_bra = QuantumCircuitMatrix.get_bra
        get_ket = QuantumCircuitMatrix.get_ket
        zero_zero_bra = get_bra("00")  # ⟨00|
        zero_one_bra = get_bra("01")   # ⟨01|
        one_zero_bra = get_bra("10")   # ⟨10|
        one_one_bra = get_bra("11")    # ⟨11|
        zero_zero_ket = get_ket("00")  # |00⟩
        zero_one_ket = get_ket("01")   # |01⟩
        one_zero_ket = get_ket("10")   # |10⟩
        one_one_ket = get_ket("11")    # |11⟩
        return np.kron(zero_zero_ket, zero_zero_bra)\
               + np.kron(one_zero_ket, zero_one_bra)\
               + np.kron(zero_one_ket, one_zero_bra)\
               + np.kron(one_one_ket, one_one_bra)

    ### Swap gate ###
    swap_gate = np.array([[1, 0, 0, 0],
                          [0, 0, 1, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 1]])
    """Swaps two qubits with respect to the basis |00⟩, |01⟩, |10⟩, |11⟩"""

    @staticmethod
    def qubits_to_bits(numQubits: int):
        """
        Converts the processing power of qubits to bits

        :param numQubits: The number of qubits
        :type numQubits: int
        :return: The equivalent number of bits
        :rtype: int
        """
        return 2**numQubits

    @staticmethod
    def bits_to_qubits(numBits: int):
        """
        Converts the processing power of bits to qubits

        :param numBits: The number of bits
        :type numBits: int
        :return: The equivalent number of qubits
        :rtype: int
        """
        return math.ceil(np.log2(numBits))

    @staticmethod
    def identityGate(numQubits: int):
        """
        The identity gate is the identity matrix

        :param numQubits: The number of qubits
        :type numQubits: int
        :return: The identity gate (in matrix form)
        :rtype: np.ndarray
        """
        numBits = QuantumCircuitMatrix.qubits_to_bits(numQubits)
        return np.identity(numBits)

    @staticmethod
    def get_qubit_matrix(numQubits: int, *args: int):
        """
        creates a square matrix for qubits

        :param numQubits: The number of entangled qubits
        :type numQubits: int
        :param args: The qubits to switch from 0 to 1, defaults to 0
        :type args: int
        :return: The square matrix for qubits
        :rtype: np.ndarray
        """
        numBits = QuantumCircuitMatrix.qubits_to_bits(numQubits)
        qubit_matrix = np.zeros([numBits, numBits])
        for argv in args:
            qubit_matrix[argv, argv] = 1
        if len(args) == 0:
            qubit_matrix[0, 0] = 1
        return qubit_matrix

    @staticmethod
    def get_qubit_vector(numQubits: int, *args: int):
        """
        creates a column vector for qubits

        :param numQubits: The number of entangled qubits
        :type numQubits: int
        :param args: The qubits to switch from 0 to 1, defaults to 0
        :type args: int
        :return: The column vector for qubits
        :rtype: np.ndarray
        """
        numBits = QuantumCircuitMatrix.qubits_to_bits(numQubits)
        qubit_matrix = np.zeros([1, numBits])
        for argv in args:
            qubit_matrix[0, argv] = 1
        if len(args) == 0:
            qubit_matrix[0, 0] = 1
        return qubit_matrix.T

    @staticmethod
    def get_zero_qubit_matrix(numQubits: int, *args: int):
        """
        creates a square matrix for qubits with each state set to 0 by default

        :param numQubits: The number of entangled qubits
        :type numQubits: int
        :param args: The qubits to switch from 0 to 1
        :type args: int
        :return: The square matrix for qubits
        :rtype: np.ndarray
        """
        qubit_matrix = np.zeros([numQubits * 2, numQubits * 2])
        for argv in args:
            qubit_matrix[argv, argv] = 1
        for i in range(numQubits):
            if qubit_matrix[2 * i+1, 2 * i + 1] == 0:
                qubit_matrix[2 * i, 2 * i] = 1
        if len(args) == 0:
            qubit_matrix[0, 0] = 1
        return qubit_matrix

    @staticmethod
    def get_zero_qubit_vector(numQubits: int, *args: int):
        """
        creates a column vector for qubits with each state set to 0 by default

        :param numQubits: The number of entangled qubits
        :type numQubits: int
        :param args: The qubits to switch from 0 to 1
        :type args: int
        :return: The column vector for qubits
        :rtype: np.ndarray
        """
        qubit_matrix = np.zeros([1, numQubits * 2])
        for argv in args:
            qubit_matrix[0, argv] = 1
        for i in range(numQubits):
            if qubit_matrix[0, 2 * i + 1] == 0:
                qubit_matrix[0, 2 * i] = 1
        if len(args) == 0:
            qubit_matrix[0, 0] = 1
        return qubit_matrix.T

    @staticmethod
    def get_zero_ket_qubit_vector(numQubits: int, *args: int):
        """
        creates a column vector ket representation for qubits with each state
        set to 0 by default

        :param numQubits: The number of entangled qubits
        :type numQubits: int
        :param args: The qubits to switch from 0 to 1
        :type args: int
        :return: The column vector for qubits
        :rtype: np.ndarray
        """
        qubit_matrix = np.zeros([1, numQubits * 2])
        for argv in args:
            qubit_matrix[0, argv] = 1
        if len(args) == 0:
            qubit_matrix[0, 0] = 1
        return qubit_matrix.T

    @staticmethod
    def get_Hadamard_matrix(numQubits: int, *args: int):
        """
        creates a square matrix for qubits in a |+⟩ state

        :param numQubits: The number of entangled qubits
        :type numQubits: int
        :param args: The qubits to switch from 0 to 1, must be in
            range(numQubits)
        :type args: int
        :return: The square matrix for qubits
        :rtype: np.ndarray
        """
        qubit_matrix = np.zeros([numQubits*2, numQubits*2])
        for i in range(numQubits*2):
            qubit_matrix[i][i] += 1
        for argv in args:
            qubit_matrix[argv * 2 + 1, argv * 2 + 1] *= -1
        return qubit_matrix / np.sqrt(2)

    @staticmethod
    def get_Hadamard_vector(numQubits: int, *args: int):
        """
        creates a column vector for qubits in a |+⟩ state

        :param numQubits: The number of entangled qubits
        :type numQubits: int
        :param args: The qubits to switch from 0 to 1, must be in
            range(numQubits)
        :type args: int
        :return: The column vector for qubits
        :rtype: np.ndarray
        """
        return QuantumCircuitMatrix.convert_matrix_to_vector(
            QuantumCircuitMatrix.get_Hadamard_matrix(numQubits, *args))

    @staticmethod
    def quantum_not_gate_matrix(numQubits: int):
        """
        creates a quantum equivalent of the classical not gate
        for any number of qubits

        :param numQubits: The number of entangled qubits
        :type numQubits: int
        :return: Pauli-X gate if numQubits=1,
            CNOT gate if numQubits=2,
            Toffoli gate if numQubits>2
        :rtype: np.ndarray
        """
        if numQubits == 0:
            return np.array([])
        if numQubits == 1:
            return QuantumCircuitMatrix.Pauli_X_gate
        if numQubits == 2:
            return QuantumCircuitMatrix.CNOT_gate
        q_not_gate_matrix = \
            np.kron(
                np.diag([1, 0]),
                QuantumCircuitMatrix.identityGate(numQubits-1)) + \
            np.kron(
                np.diag([0, 1]),
                QuantumCircuitMatrix.quantum_not_gate_matrix(numQubits-1))
        return q_not_gate_matrix

    @staticmethod
    def quantum_Fourier_transform(numQubits: int):
        """
        The quantum Fourier transform is the classical discrete Fourier
        transform applied to the vector of amplitudes of a quantum state,
        where we usually consider vectors of length N=2^n

        :param numQubits: The number of qubits
        :type numQubits: int
        :return: A quantum Fourier transform matrix for numQubits
        :rtype: np.ndarray
        """
        numBits = QuantumCircuitMatrix.qubits_to_bits(numQubits)
        quantum_Fourier_transform_matrix = Misc.real_to_complex_matrix(
            np.zeros([numBits, numBits]))
        # Using basic wave formula:
        quantum_phase = np.e ** (2j * np.pi / numBits)
        # # Using Euler's formula on basic wave formula:
        # quantum_phase = np.cos(2*np.pi/numBits) + np.sin(2*np.pi/numBits)*1j
        for i in range(numBits):
            for j in range(numBits):
                quantum_Fourier_transform_matrix[i][j] += quantum_phase ** (
                            i * j)
        quantum_Fourier_transform_matrix /= np.sqrt(numBits)
        return quantum_Fourier_transform_matrix

    @staticmethod
    def invert_matrix(matrix):
        """
        Calculates the inverse of a matrix

        :param matrix: A square matrix
        :type matrix: np.ndarray
        :return: The inverse of matrix
        :rtype np.ndarray:
        """
        from numpy.linalg import inv
        return inv(matrix)

    @staticmethod
    def applied_swap_gate(qubits: np.ndarray, *args: int):
        """
        Applies the swap gate to qubits

        :param qubits: A matrix of qubits
        :type qubits: np.ndarray
        :param args: Specified qubits to apply swap gate to, must be a multiple
            of 2 because swap gate will apply to every pair of two, must not
            have the same number more than once
        :type args: int
        :return: A swapped qubit matrix
        :rtype: np.ndarray
        """
        vector_start = False
        if qubits.shape[1] == 1:
            vector_start = True
            swapped_qubit_matrix = qubits
        else:
            swapped_qubit_matrix = np.zeros([qubits.shape[0]])
            for bits in range(qubits.shape[0]):
                swapped_qubit_matrix[bits] += qubits[bits][bits]
        if len(args) == 0:
            swapped_qubit_matrix = np.dot(
                swapped_qubit_matrix,
                np.kron(
                    QuantumCircuitMatrix.swap_gate, np.identity(
                        int(int(qubits.shape[0]) /
                            int(QuantumCircuitMatrix.swap_gate.shape[0])))
                ))
        else:
            swapping_gate_matrix = np.identity(qubits.shape[0])
            for argv in range(int(len(args)/2)):
                qubit_0 = args[argv]
                qubit_1 = args[argv+1]
                if swapping_gate_matrix[qubit_0*2+1][qubit_0*2+1] != 0 and \
                        swapping_gate_matrix[qubit_1*2][qubit_1*2] != 0:
                    swapping_gate_matrix[qubit_0*2+1][qubit_0*2+1] -= 1
                    swapping_gate_matrix[qubit_1*2][qubit_1*2] -= 1
                    swapping_gate_matrix[qubit_0*2+1][qubit_1*2] += 1
                    swapping_gate_matrix[qubit_1*2][qubit_0*2+1] += 1
                    swapped_qubit_matrix = np.dot(
                        swapped_qubit_matrix, swapping_gate_matrix)
        if vector_start:
            return swapped_qubit_matrix
        swapped_qubit_matrix = np.diag(swapped_qubit_matrix)
        return swapped_qubit_matrix

    @staticmethod
    def reverse_quantum_not_gate_matrix(numQubits: int):
        """
        creates a quantum equivalent of the classical not gate
        for any number of qubits

        :param numQubits: The number of entangled qubits
        :type numQubits: int
        :return: Pauli-X gate if numQubits=1,
            CNOT gate if numQubits=2,
            Toffoli gate if numQubits>2
        :rtype: np.ndarray
        """
        if numQubits == 0:
            return np.array([])
        if numQubits == 1:
            return QuantumCircuitMatrix.Pauli_X_gate
        if numQubits == 2:
            return np.kron(np.diag([0, 1]), np.identity(2)) + \
                   np.kron(np.diag([1, 0]), QuantumCircuitMatrix.Pauli_X_gate)
        q_not_gate_matrix = \
            np.kron(
                np.diag([0, 1]),
                QuantumCircuitMatrix.identityGate(numQubits - 1)) + \
            np.kron(
                np.diag([1, 0]),
                QuantumCircuitMatrix.quantum_not_gate_matrix(numQubits - 1))
        return q_not_gate_matrix

    @staticmethod
    def convert_matrix_to_vector(qubit_matrix: np.ndarray):
        """
        Converts a qubit matrix to a qubit vector

        :param qubit_matrix:
        :return:
        """
        if qubit_matrix.shape[1] == 1:
            return qubit_matrix
        qubit_vector = qubit_matrix.sum(axis=1)
        qubit_vector = np.array([qubit_vector])
        return qubit_vector.T

    @staticmethod
    def convert_vector_to_matrix(qubit_vector: np.ndarray):
        """
        Converts a qubit vector to a qubit matrix

        :param qubit_vector:
        :return:
        """
        if qubit_vector.shape[0] == qubit_vector.shape[1]:
            return qubit_vector
        qubit_matrix = np.zeros([qubit_vector.shape[0], qubit_vector.shape[0]])
        for q in range(qubit_vector.shape[0]):
            qubit_matrix[q][q] += qubit_vector[q][0]
        return qubit_matrix

    @staticmethod
    def print_qubits(*args: np.ndarray):
        """
        Prints the dimensions and matrices of qubits

        :param args: The qubits to print in order (starting at 0)
        :type args: np.ndarray
        """
        np.set_printoptions(linewidth=np.inf)
        i = 0
        for argv in args:
            print("qubit " + str(i) + " dimensions: " + str(argv.shape))
            print("qubit " + str(i) + ":")
            print(argv)
            print()
            i += 1

    @staticmethod
    def print_truncated_qubits(numDecimals: int, *args: np.ndarray):
        """
        Prints the dimensions and truncated matrices of qubits

        :param numDecimals: The number of decimals to truncate to
        :param args: The qubits to print in order (starting at 0)
        :type args: np.ndarray
        """
        np.set_printoptions(linewidth=np.inf)
        i = 0
        for argv in args:
            print("qubit " + str(i) + " dimensions: " + str(argv.shape))
            print("qubit " + str(i) + ":")
            print(np.round(argv, numDecimals))
            print()
            i += 1

    @staticmethod
    def QuantumPeriodFinding(func, *args, n_count: int = 8):
        """
        Uses Shor's period finding-algorithm to compute the period of func

        :param func: A quantum function
        :type func: function
        :param args: The arguments to pass to func
        :param n_count: The number of counting qubits
        :type n_count: int
        :return: The period
        :rtype: int
        """
        QFT = QuantumCircuitMatrix.quantum_Fourier_transform(n_count)
        QFT_dagger = QuantumCircuitMatrix.invert_matrix(QFT)
        qc = np.zeros([n_count, n_count])
        for q in range(n_count):
            qc[q][q] += \
                (func(args))[q][q]
        qubit_matrix = \
            np.dot(np.kron(qc, np.identity(
                int(QFT_dagger.shape[0] / qc.shape[0]))), QFT_dagger)
        return int(qubit_matrix.sum(0).sum(0).real / 4)
