import logging
from abc import abstractmethod, ABC
import hashlib
import logging
import pickle
import util
import yao

# File kept mostly intact
# Only change is applied to func send result,
# which now also return the same value as is sent through channel

class YaoGarbler:
    """Class for Yao garblers (e.g., Alice) supporting local testing."""

    def __init__(self, circuits, print_mode="circuit"):
        self._load_circuits(circuits)
        self._print_mode = print_mode
        self._modes = {
            "circuit": self._print_evaluation,
            "table": self._print_tables,
            "none": self._print_evaluation
        }
        logging.info(f"Print mode: {print_mode}")

    def _load_circuits(self, circuits):
        parsed_circuits = util.parse_json(circuits)
        self.name = parsed_circuits["name"]
        self.circuits = []

        for circuit_data in parsed_circuits["circuits"]:
            garbled_circuit = yao.GarbledCircuit(circuit_data)
            entry = {
                "circuit": circuit_data,
                "garbled_circuit": garbled_circuit,
                "garbled_tables": garbled_circuit.get_garbled_tables(),
                "keys": garbled_circuit.get_keys(),
                "pbits": garbled_circuit.get_pbits(),
                "pbits_out": {w: garbled_circuit.get_pbits()[w] for w in circuit_data["out"]},
            }
            self.circuits.append(entry)

    def start(self):
        """Start local Yao protocol."""
        for circuit_entry in self.circuits:
            self._modes[self.print_mode](circuit_entry)

    def _print_tables(self, circuit_entry):
        """Print garbled tables."""
        circuit_entry["garbled_circuit"].print_garbled_tables()

    def _print_evaluation(self, circuit_entry):
        """Print circuit evaluation."""
        circuit_data = circuit_entry["circuit"]
        pbits = circuit_entry["garbled_circuit"].get_pbits()
        keys = circuit_entry["keys"]
        garbled_tables = circuit_entry["garbled_tables"]
        outputs = circuit_data["out"]
        a_wires = circuit_data.get("alice", [])  # Alice's wires
        b_wires = circuit_data.get("bob", [])  # Bob's wires
        pbits_out = circuit_entry["pbits_out"]
        N = len(a_wires) + len(b_wires)
        
        print(f"======== {circuit_data['id']} ========")

        for bits in [format(n, 'b').zfill(N) for n in range(2**N)]:
            a_inputs = {a_wires[i]: (keys[a_wires[i]][int(b)], pbits[a_wires[i]] ^ int(b))
                        for i, b in enumerate(bits[:len(a_wires)])}
            b_inputs = {b_wires[i]: (keys[b_wires[i]][int(b)], pbits[b_wires[i]] ^ int(b))
                        for i, b in enumerate(bits[-len(b_wires):])}
            
            result = yao.evaluate(circuit_data, garbled_tables, pbits_out, a_inputs, b_inputs)
            
            str_bits_a = ' '.join(bits[:len(a_wires)])
            str_bits_b = ' '.join(bits[-len(b_wires):])
            str_result = ' '.join([str(result[w]) for w in outputs])
            
            print(f"  Alice{a_wires} = {str_bits_a} "
                  f"Bob{b_wires} = {str_bits_b}  "
                  f"Outputs{outputs} = {str_result}")
        
        print()

    @property
    def print_mode(self):
        return self._print_mode

    @print_mode.setter
    def print_mode(self, print_mode):
        if print_mode not in self._modes:
            logging.error(f"Unknown print mode '{print_mode}', "
                          f"must be in {list(self._modes.keys())}")
            return
        self._print_mode = print_mode
     
class ObliviousTransfer:
    def __init__(self, socket, enabled=True):
        self.socket = socket
        self.enabled = enabled

    def get_result(self, a_inputs, b_keys):
        """Send Alice's inputs and retrieve Bob's result of evaluation.

        Args:
            a_inputs: A dict mapping Alice's wires to (key, encr_bit) inputs.
            b_keys: A dict mapping each Bob's wire to a pair (key, encr_bit).

        Returns:
            The result of the yao circuit evaluation.
        """
        logging.debug("Sending inputs to Bob")
        self.socket.send(a_inputs)

        for _ in range(len(b_keys)):
            w = self.socket.receive()  # receive gate ID where to perform OT
            logging.debug(f"Received gate ID {w}")

            if self.enabled:  # perform oblivious transfer
                pair = (pickle.dumps(b_keys[w][0]), pickle.dumps(b_keys[w][1]))
                self.ot_garbler(pair)
            else:
                to_send = (b_keys[w][0], b_keys[w][1])
                self.socket.send(to_send)

        return self.socket.receive()

    def send_result(self, circuit, g_tables, pbits_out, b_inputs):
        """Evaluate circuit and send the result to Alice.

        Args:
            circuit: A dict containing circuit spec.
            g_tables: Garbled tables of yao circuit.
            pbits_out: p-bits of outputs.
            b_inputs: A dict mapping Bob's wires to (clear) input bits.

        Returns:
            result: Output of the evaluation, formatted as dictionary {no_of_wire: bit}
                    It is the same value as is sent to the counterpart.
        """
        # map from Alice's wires to (key, encr_bit) inputs
        a_inputs = self.socket.receive()
        # map from Bob's wires to (key, encr_bit) inputs
        b_inputs_encr = {}

        logging.debug("Received Alice's inputs")

        for w, b_input in b_inputs.items():
            logging.debug(f"Sending gate ID {w}")
            self.socket.send(w)

            if self.enabled:
                b_inputs_encr[w] = pickle.loads(self.ot_evaluator(b_input))
            else:
                pair = self.socket.receive()
                logging.debug(f"Received key pair, key {b_input} selected")
                b_inputs_encr[w] = pair[b_input]

        result = yao.evaluate(circuit, g_tables, pbits_out, a_inputs,
                              b_inputs_encr)

        logging.debug("Sending circuit evaluation")
        self.socket.send(result)
        return result

    def ot_garbler(self, msgs):
        """Oblivious transfer, Alice's side.

        Args:
            msgs: A pair (msg1, msg2) to suggest to Bob.
        """
        logging.debug("OT protocol started")
        G = util.PrimeGroup()
        self.socket.send_wait(G)

        # OT protocol based on Nigel Smart’s "Cryptography Made Simple"
        c = G.gen_pow(G._random_integer())
        h0 = self.socket.send_wait(c)
        h1 = G.mul(c, G.inv(h0))
        k = G._random_integer()
        c1 = G.gen_pow(k)
        e0 = util.xor_bytes(msgs[0], self.ot_hash(G.pow(h0, k), len(msgs[0])))
        e1 = util.xor_bytes(msgs[1], self.ot_hash(G.pow(h1, k), len(msgs[1])))

        self.socket.send((c1, e0, e1))
        logging.debug("OT protocol ended")

    def ot_evaluator(self, b):
        """Oblivious transfer, Bob's side.

        Args:
            b: Bob's input bit used to select one of Alice's messages.

        Returns:
            The message selected by Bob.
        """
        logging.debug("OT protocol started")
        G = self.socket.receive()
        self.socket.send(True)

        # OT protocol based on Nigel Smart’s "Cryptography Made Simple"
        c = self.socket.receive()
        x = G._random_integer()
        x_pow = G.gen_pow(x)
        h = (x_pow, G.mul(c, G.inv(x_pow)))
        c1, e0, e1 = self.socket.send_wait(h[b])
        e = (e0, e1)
        ot_hash = self.ot_hash(G.pow(c1, x), len(e[b]))
        mb = util.xor_bytes(e[b], ot_hash)

        logging.debug("OT protocol ended")
        return mb

    @staticmethod
    def ot_hash(pub_key, msg_length):
        """Hash function for OT keys."""
        key_length = (pub_key.bit_length() + 7) // 8  # key length in bytes
        bytes = pub_key.to_bytes(key_length, byteorder="big")
        return hashlib.shake_256(bytes).digest(msg_length)
