import logging
import ot
import util

class Alice(ot.YaoGarbler):
    def __init__(self, circuits, oblivious_transfer=True, print_mode="none", filename="", bit_size=4):
        super().__init__(circuits)
        self.socket = util.GarblerConnection()
        self.ot = ot.ObliviousTransfer(self.socket, enabled=oblivious_transfer)
        self.pm = print_mode
        self.general_max = -1
        self.bitlen = bit_size
        if filename == "":
            _, self.private_value = util.process_private_data("Alice", bit_size=bit_size)
        else:
            _, self.private_value = util.process_private_data("Alice", bit_size=bit_size, file_read=True, filename=filename)

    def start(self):
        """Start Yao protocol."""
        for circuit in self.circuits:
            to_send = {
                "circuit": circuit["circuit"],
                "garbled_tables": circuit["garbled_tables"],
                "pbits_out": circuit["pbits_out"],
                "printout": self.pm,
                "bitlength": self.bitlen,
            }
            logging.debug(f"Sending circuit: {circuit['circuit']['id']}")
            self.socket.send_wait(to_send)
            if self.pm != "none":
                self.print(circuit)
            print("-------------")
            self.calculate_response(circuit)
            self.verify()

    def calculate_response(self, entry):
        circuit, pbits, keys = entry["circuit"], entry["pbits"], entry["keys"]
        a_wires = circuit.get("alice", [])
        a_inputs = {}
        b_wires = circuit.get("bob", [])
        b_keys = {
            w: self._get_encr_bits(pbits[w], key0, key1)
            for w, (key0, key1) in keys.items() if w in b_wires
        }

        bits_a = [int(b) for b in self.private_value]

        for i in range(len(a_wires)):
            a_inputs[a_wires[i]] = (keys[a_wires[i]][bits_a[i]], pbits[a_wires[i]] ^ bits_a[i])

        result = self.ot.get_result(a_inputs, b_keys)
        int_result = util.circuit_t_int(result)
        self.general_max = int_result
        print(f"Result of function is {int_result}")
        logging.debug(f"Calculated result: {int_result}")

    def _get_encr_bits(self, pbit, key0, key1):
        return ((key0, 0 ^ pbit), (key1, 1 ^ pbit))

    def verify(self):
        to_send = {
            "alice_max": int(self.private_value, 2),
            "general_max": self.general_max
        }
        logging.debug(f"Sending data for verification: {to_send}")
        self.socket.send_wait(to_send)
        self.socket.send("connection established")
        result = self.socket.receive()
        print(f"Result of verification: {result}")
        logging.debug(f"Verification result: {result}")
