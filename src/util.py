import json
import operator
import random
import secrets
import sympy
import zmq

# SOCKET
LOCAL_PORT = 4080
SERVER_HOST = "localhost"
SERVER_PORT = 4080
def process_private_data(name: str = "", bit_size: int = 16, file_read: bool = False, filename=None, data: list = []) -> tuple:
    """
    Process private data for computing the maximum value.

    Returns:
        tuple: A tuple containing the cleaned input data and the local maximum.
    """
    if len(data) == 0:
        if not file_read:
            line = [*map(int, input().split())]
        else:
            try:
                with open(filename, "r") as f:
                    print("Reading data from txt file")
                    line = list(map(int, f.read().split()))
            except FileNotFoundError:
                print("File does not exist")
                exit(10)
    else:
        line = data

    # Clean up directly in the main function
    line = [num for num in line if 0 <= num < 2 ** bit_size]

    local_max = bin(max(line))[2:].zfill(bit_size)
    return line, local_max

def circuit_t_int(d: dict) -> int:
    """
    Convert a dictionary of bits to an integer.

    Args:
        d (dict): Dictionary representing bits.

    Returns:
        int: Integer value.
    """
    return int("".join(str(d[k]) for k in d.keys()), 2)



class Socket:
    def __init__(self, socket_type, endpoint=None):
        self.socket = zmq.Context().socket(socket_type)
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        
        if endpoint:
            if socket_type == zmq.REP:
                self.socket.bind(endpoint)
            elif socket_type == zmq.REQ:
                self.socket.connect(endpoint)
        
    def send(self, msg):
        self.socket.send_pyobj(msg)

    def receive(self):
        return self.socket.recv_pyobj()

    def send_wait(self, msg):
        self.send(msg)
        return self.receive()

    def poll_socket(self, timetick=100):
        try:
            while True:
                obj = dict(self.poller.poll(timetick))
                if self.socket in obj and obj[self.socket] == zmq.POLLIN:
                    yield self.receive()
        except KeyboardInterrupt:
            pass

class EvaluatorSocket(Socket):
    def __init__(self, endpoint=f"tcp://*:{LOCAL_PORT}"):
        super().__init__(zmq.REP, endpoint)

class GarblerConnection(Socket):
    def __init__(self, endpoint=f"tcp://{SERVER_HOST}:{SERVER_PORT}"):
        super().__init__(zmq.REQ, endpoint)

# Prime group constants
PRIME_BITS = 64


def next_prime(num):
    """Return next prime after 'num' (skip 2)."""
    return 3 if num < 3 else sympy.nextprime(num)


def gen_prime(num_bits):
    """Return random prime of bit size 'num_bits'"""
    r = secrets.randbits(num_bits)
    return next_prime(r)


def xor_bytes(seq1, seq2):
    """XOR two byte sequences."""
    return bytes(map(operator.xor, seq1, seq2))


def bits(num, width):
    """Convert number into a list of bits."""
    return [int(k) for k in f'{num:0{width}b}']


class PrimeGroup:
    """Cyclic abelian group of prime order 'prime'."""

    def __init__(self, prime=None):
        self.prime = prime or self._generate_prime()
        self.prime_minus_1 = self.prime - 1
        self.prime_minus_2 = self.prime - 2
        self.generator = self._find_generator()

    def _generate_prime(self):
        """Generate a random prime number."""
        random_bits = secrets.randbits(PRIME_BITS)
        return next_prime(random_bits)

    def _find_generator(self):
        """Find a random generator for the group."""
        factors = sympy.primefactors(self.prime_minus_1)

        while True:
            candidate = self._random_integer()
            if all(self.pow(candidate, (self.prime_minus_1) // factor) != 1 for factor in factors):
                return candidate

    def _random_integer(self):
        """Return a random integer in the range [1, prime - 1]."""
        return random.randint(1, self.prime_minus_1)

    def mul(self, num1, num2):
        """Multiply two elements in the group."""
        return (num1 * num2) % self.prime

    def pow(self, base, exponent):
        """Compute nth power of an element."""
        return pow(base, exponent, self.prime)

    def gen_pow(self, exponent):
        """Compute nth power of the generator."""
        return pow(self.generator, exponent, self.prime)

    def inv(self, num):
        """Compute the multiplicative inverse of an element."""
        return pow(num, self.prime_minus_2, self.prime)

# HELPER FUNCTIONS
def parse_json(json_path):
    with open(json_path) as json_file:
        return json.load(json_file)




