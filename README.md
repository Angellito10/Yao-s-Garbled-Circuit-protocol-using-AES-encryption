# **Project Overview**

This project implements Yao's Garbled Circuit protocol using AES encryption to securely compute the maximum value between two sets of 4-bit integers. It extends the initial implementation by Olivier Roques and Emmanuelle Risson [GitHub Repository: Yao's Garbled Circuit Protocol](https://github.com/ojroques/garbled-circuit) , ensuring secure communication and computation between two parties, Alice and Bob.

## **Objective**

The primary objective is to enable secure computation where Alice initiates the protocol by providing the circuit design. The protocol ensures confidentiality and authenticity, even in untrusted environments.

## **Circuit Design and Overview**

### **Inputs and Outputs**

- **Alice's Inputs:** `alice = [101, 102, 103, 104]` (4-bit integers)
- **Bob's Inputs:** `bob = [105, 106, 107, 108]` (4-bit integers)
- **Outputs:** `out = [150, 151, 152, 153]` (4-bit integer representing the maximum value)

### **Gates and Connections**

The circuit utilizes NOT, AND, OR, and XNOR gates interconnected to perform bitwise operations necessary for comparison and selection.

### **Detailed Logic Flow**

#### **Comparator Section**

The comparator evaluates bits from Most Significant Bit (MSB) to Least Significant Bit (LSB) to determine which input is larger.

**Bitwise Comparison:**

1. **Least Significant Bit (LSB):**
    - NOT gate on `104` results in `110`.
    - AND gate on `110` and `108` results in `111`.
    - XNOR gate on `103` and `108` results in `112`.
    - AND gate on `111` and `112` results in `113`.

2. **Second Bit:**
    - NOT gate on `103` results in `114`.
    - AND gate on `114` and `107` results in `115`.
    - OR gate on `113` and `115` results in `116`.

3. **Third Bit:**
    - XNOR gate on `102` and `108` results in `117`.
    - OR gate on `116` and `117` results in `118`.
    - NOT gate on `102` results in `119`.
    - AND gate on `119` and `106` results in `120`.
    - OR gate on `120` and `118` results in `121`.

4. **Most Significant Bit (MSB):**
    - XNOR gate on `101` and `108` results in `122`.
    - OR gate on `121` and `122` results in `123`.
    - NOT gate on `101` results in `124`.
    - AND gate on `124` and `105` results in `125`.
    - OR gate on `125` and `123` results in `130`.

#### **Determining Larger Number**

- NOT gate on `130` results in `131`.
- AND gate on `131` and `101` results in `132`.
- AND gate on `130` and `105` results in `133`.
- OR gate on `132` and `133` results in the first output bit `150`.

**Similar operations produce bits `151`, `152`, and `153`:**

- AND gate on `131` and `102` results in `134`.
- AND gate on `130` and `106` results in `135`.
- OR gate on `134` and `135` results in the second output bit `151`.
- AND gate on `131` and `103` results in `136`.
- AND gate on `130` and `107` results in `137`.
- OR gate on `136` and `137` results in the third output bit `152`.
- AND gate on `131` and `104` results in `138`.
- AND gate on `130` and `108` results in `139`.
- OR gate on `138` and `139` results in the fourth output bit `153`.

---

## **Running the Project**

### **Pre-requisites**

#### **Python Version**

- Ensure Python 3 is installed. Verify with:
  ```sh
  python3 --version
  ```
- If not installed, download and install Python 3 from [python.org](https://www.python.org/downloads/).

#### **Package Installation**

- Install dependencies using virtual environment:
    
  ```sh
    python3 -m venv path/to/venv
    source path/to/venv/bin/activate
    python3 -m pip install -r requirements.txt
  ```
  
## OR

- Install dependencies using pip:
  ```sh
  pip install -r requirements.txt
  ```

### **Execution**

1. **Open Terminals:**
    - Open two terminal windows.

2. **Run Bob's Instance:**
    - In one terminal, navigate to the project directory and run:
      ```sh
      cd src/
      python3 amain.py bob -i inputs/bob.txt
      ```

3. **Run Alice's Instance:**
    - In the other terminal, navigate to the project directory and run:
      ```sh
      cd src/
      python3 main.py alice -i inputs/alice.txt
      ```

### **Expected Output**

Both terminals should display the computation result and verification status:
```sh
Reading data from txt file
Received compute 4-bit
Result of function is 15
Verified correctly
```

---

## **Documentation for Provided Code**

### **Directory Structure**

```plaintext
├── alice.py
├── bob.py
├── circuits
│   └── computerMaximum.json
├── inputs
│   ├── alice.txt
│   └── bob.txt
├── main.py
├── ot.py
├── util.py
└── yao.py
```

### **Code Explanation**

#### **alice.py**

Implements Alice's role in Yao's protocol, managing garbled circuit evaluation and communication with Bob.

#### **bob.py**

Defines Bob's role in Yao's protocol, processing private data, evaluating the garbled circuit, and verifying results.

#### **ot.py**

Implements the Oblivious Transfer (OT) protocol, essential for secure multi-party computation.

#### **util.py**

Provides utilities for secure computation using Yao's protocol, including socket communication and cryptographic operations.

---

### **1. util.py**

**Purpose:** `util.py` serves as a fundamental module providing utilities essential for secure computation using Yao's protocol. It includes functionalities for socket communication, prime number generation, byte/bit manipulation, and cryptographic operations.

**Functions:**

1. **process\_private\_data**
    - **Purpose:** Processes private data for computing the maximum value, filtering data to fit within the specified bit size, and providing its binary representation.
    - **Parameters:**
        - `name` (optional, str): Identifier for the data source (default: "").
        - `bit_size` (optional, int): Maximum bit size for each number (default: 16).
        - `file_read` (optional, bool): Indicates if data should be read from a file (default: False).
        - `filename` (optional, str): Name of the file from which to read data (if `file_read` is True).
        - `data` (optional, list): Direct input of data as a list of integers.
    - **Returns:** A tuple containing:
        - A list of processed data points.
        - The binary representation of the local maximum value.

2. **circuit\_t\_int**
    - **Purpose:** Converts a dictionary containing binary values into an integer, representing the combined string values of the dictionary keys.
    - **Parameters:**
        - `d` (dict): Dictionary where keys represent binary positions, and values are binary digits.
    - **Returns:** An integer representing the combined string values of the dictionary keys.

**Classes:**

1. **Socket**
    - **Purpose:** Base class for handling socket communication using ZeroMQ.
    - **Methods:**
        - `send(msg)`: Sends a message.
        - `receive()`: Receives a message.
        - `send_wait(msg)`: Sends a message and waits for a response.
        - `poll_socket(timetick=100)`: Polls the socket at the specified interval.

2. **EvaluatorSocket**
    - **Purpose:** Specialized socket class for the evaluator role using ZeroMQ, representing a REP type socket bound to a local port.
    - **Parameters:**
        - `endpoint` (str, optional): The endpoint to bind to (default: `f"tcp://*:{LOCAL_PORT}"`).

3. **GarblerConnection**
    - **Purpose:** Specialized socket class for the garbler role using ZeroMQ, representing a REQ type socket connecting to a specified server.
    - **Parameters:**
        - `endpoint` (str, optional): The endpoint to connect to (default: `f"tcp://{SERVER_HOST}:{SERVER_PORT}"`).

---

### **2. main.py**

**Purpose:** `main.py` serves as the main entry point for executing Yao's protocol, initializing either Alice or Bob based on command-line arguments. It manages the execution of Yao's protocol by setting up logging and directing control flow to the respective party's implementation.

**Functions:**

1. **main**
    - **Purpose:** Initializes the specified party (Alice, Bob, or local test) for Yao's protocol execution.
    - **Parameters:**
        - `party` (str): Role to initialize ("alice", "bob", "local").
        - `circuit_path` (str): Path to the circuit configuration JSON file (default: `"src/circuits/computerMaximum.json"`).
        - `oblivious_transfer` (bool): Flag for enabling oblivious transfer (default: True).
        - `print_mode` (str): Print mode for debugging (default: "none").
        - `loglevel` (int): Logging level (

default: `logging.DEBUG`).
    - **Usage:** Called with command-line arguments to initiate the protocol execution.

---

## **Contributors**

- **Project Contributors:** Olivier Roques, Emmanuelle Risson
