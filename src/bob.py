import logging
import ot
import util

class Bob:
    def __init__(self, oblivious_transfer=True, filename=""):
        self.socket = util.EvaluatorSocket()
        self.ot = ot.ObliviousTransfer(self.socket, enabled=oblivious_transfer)
        self.private_value = "0"
        if filename == "":
            self.data, _ = util.process_private_data("Bob")
        else:
            self.data, _ = util.process_private_data("Bob", file_read=True, filename=filename)

    def listen(self):
        """Start listening for Alice messages."""
        logging.info("Start listening")
        try:
            for entry in self.socket.poll_socket():
                self.socket.send(True)
                if len(entry) == 5:
                    _, self.private_value = util.process_private_data(data=self.data, bit_size=entry["bitlength"])
                    if entry["printout"] != "none":
                        self.send_evaluation(entry)
                    self.send_response(entry)
                elif len(entry) == 2:
                    self.verify(entry)
                else:
                    logging.info("Stop listening")
                    exit(1)
        except KeyboardInterrupt:
            logging.info("Stop listening")

    def send_evaluation(self, entry):
        circuit, pbits_out = entry["circuit"], entry["pbits_out"]
        garbled_tables = entry["garbled_tables"]
        a_wires = circuit.get("alice", [])
        b_wires = circuit.get("bob", [])
        N = len(a_wires) + len(b_wires)

        print(f"Received {circuit['id']}")

        for bits in [format(n, 'b').zfill(N) for n in range(2 ** N)]:
            bits_b = [int(b) for b in bits[N - len(b_wires):]]

            b_inputs_clear = {
                b_wires[i]: bits_b[i]
                for i in range(len(b_wires))
            }

            self.ot.send_result(circuit, garbled_tables, pbits_out, b_inputs_clear)

    def send_response(self, entry):
        circuit, pbits_out = entry["circuit"], entry["pbits_out"]
        garbled_tables = entry["garbled_tables"]
        b_wires = circuit.get("bob", [])

        print(f"Received {circuit['id']}")

        bits_b = [int(b) for b in self.private_value]

        b_inputs_clear = {
            b_wires[i]: bits_b[i]
            for i in range(len(b_wires))
        }

        result = self.ot.send_result(circuit, garbled_tables, pbits_out, b_inputs_clear)
        int_result = util.circuit_t_int(result)
        print(f"Result of function is {int_result}")
        logging.debug(f"Calculated result: {int_result}")

    def verify(self, entry):
        logging.info("Verifying")
        self.socket.receive()
        alice_max = entry["alice_max"]
        general_max = entry["general_max"]
        verification_max = max(alice_max, int(self.private_value, 2))
        res = verification_max == general_max
        if res:
            print("Verified correctly")
        else:
            print(f"Error! Through transfer obtained: {general_max}, correct value: {verification_max}")
        self.socket.send(res)
