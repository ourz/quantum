# Estimates \pi on a quantum circuit with n cubits. The algorithm iteratively searches for a solution
# to the equation f(x) - x = 0, where f is a quantum circuit parameterized by one parameter. This 
# parameter represents an estimate of pi and is used instead of the actual value of pi in the inverse 
# quantum fourier transform . With x = \pi, the equation f(x) = x is satisfied with equality. The error
# of the estimate decreases with the number of cubits. The actual secant search is done classically.

def initialize_qubits(given_circuit, measurement_qubits, target_qubit):
    given_circuit.h(measurement_qubits)
    given_circuit.x(target_qubit)

def apply_iqft(given_circuit, measurement_qubits, n):#improper qft inverse using an estimate of pi
    def f(pi_est):
        for x in measurement_qubits:
            if x < (n-1)/2: given_circuit.swap(x,n-1-x)

        for target_qubit in reversed(measurement_qubits):
            for control_qubit in reversed(range(target_qubit+1,n)):
                k = target_qubit - control_qubit - 1
                exponent = -2**(k)
                given_circuit.cu1(2*pi_est*exponent, control_qubit, target_qubit)
            given_circuit.h(target_qubit)
            given_circuit.barrier()
    return f

def qpe_program(n, pi_init):
    from qiskit import QuantumCircuit
    # Create a quantum circuit on n+1 qubits (n measurement, 1 target)
    qc = QuantumCircuit(n+1, n)

    # Initialize the qubits
    initialize_qubits(qc, range(n), n)

    # Apply the controlled unitary operators in sequence
    for x in range(n):
        exponent = 2**(n-x-1)
        qc.cu1(1*exponent, x, n)

    qc.barrier()
    # Apply the "inverse quantum Fourier transform"
    apply_iqft(qc, range(n), n)(pi_init)

    # Measure all qubits
    qc.measure(range(n), range(n))
  
    return qc

def measure_pi(n, mycircuit, simulator):
    counts = execute(mycircuit, backend=simulator, shots=5000).result().get_counts(mycircuit)
    highest_probability_outcome = max(counts.items(), key=operator.itemgetter(1))[0][::-1]
    return 2**(n-1) / int(highest_probability_outcome, 2)

def estimate_pi(n):
    import operator
    from qiskit import Aer, execute
    simulator = Aer.get_backend('qasm_simulator')
    pi_est = 1
    pi_est_last = 1.2
    qc = qpe_program(n, pi_est)
    measured = measure_pi(n, qc, simulator)
    qc = qpe_program(n, pi_est_last)
    measured_last = measure_pi(n, qc, simulator)
    for k in range(200):
        tmp = pi_est
        converged = measured == measured_last and pi_est == pi_est_last
        if converged:
            print("using ", n, " qubits, after ", k, " iterations, the estimate of pi is", pi_est)
            return (measured, k)
        else:
            pi_est = pi_est - (pi_est - pi_est_last) / (measured - pi_est - measured_last + pi_est_last ) * (measured - pi_est)
            measured_last = measured
            pi_est_last = tmp
            qc = qpe_program(n, pi_est)
            measured = measure_pi(n, qc, simulator)
    print("failed to converge")
 
 for n in range(5, 20):
    estimate_pi(n)
