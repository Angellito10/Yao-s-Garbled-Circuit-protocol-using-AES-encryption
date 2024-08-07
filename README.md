**Project Overview** 

This project implements Yao's Garbled Circuit protocol using AES encryption to securely compute  the  maximum  value  between  two  sets  of  4-bit  integers.  It  extends  the  initial implementation by Olivier Roques and Emmanuelle Risson, ensuring secure communication and computation between two parties, Alice and Bob. 

**Objective** 

The primary objective is to enable secure computation where Alice initiates the protocol by providing the circuit design. The protocol ensures confidentiality and authenticity, even in untrusted environments. ![](Aspose.Words.78a54c2c-d82c-44f0-b684-526d78b7db84.001.png)

1. **Circuit Design and Overview** 
1. **Circuit Design** 

**Inputs and Outputs:** 

- **Alice's Inputs:** alice = [101, 102, 103, 104] (4-bit integers) 
- **Bob's Inputs:** bob = [105, 106, 107, 108] (4-bit integers) 
- **Outputs:** out = [150, 151, 152, 153] (4-bit integer representing the maximum value) 
2. **Gates and Connections** 

The circuit utilizes NOT, AND, OR, and XNOR gates interconnected to perform bitwise operations necessary for comparison and selection. 

**Detailed Logic Flow** 

1. **Comparator Section** 

The comparator evaluates bits from Most Significant Bit (MSB) to Least Significant Bit (LSB) to determine which input is larger. 

**Bitwise Comparison:** 

- **Least Significant Bit (LSB):** 
- NOT gate on 104 results in 110. 
- AND gate on 110 and 108 results in 111. 
- XNOR gate on 103 and 108 results in 112. 
- AND gate on 111 and 112 results in 113. 
- **Second Bit:** 
- NOT gate on 103 results in 114. 
- AND gate on 114 and 107 results in 115. 
- OR gate on 113 and 115 results in 116. 
- **Third Bit:** 
- XNOR gate on 102 and 108 results in 117. 
- OR gate on 116 and 117 results in 118. 
- NOT gate on 102 results in 119. 
- AND gate on 119 and 106 results in 120. 
- OR gate on 120 and 118 results in 121. 
- **Most Significant Bit (MSB):** 
- XNOR gate on 101 and 108 results in 122. 
- OR gate on 121 and 122 results in 123. 
- NOT gate on 101 results in 124. 
- AND gate on 124 and 105 results in 125. 
- OR gate on 125 and 123 results in 130. 
2. **Determining Larger Number** 
- NOT gate on 130 results in 131. 
- AND gate on 131 and 101 results in 132. 
- AND gate on 130 and 105 results in 133. 
- OR gate on 132 and 133 results in the first output bit 150. 

**Similar operations produce bits 151, 152, and 153:** 

- AND gate on 131 and 102 results in 134. 
- AND gate on 130 and 106 results in 135. 
- OR gate on 134 and 135 results in the second output bit 151. 
- AND gate on 131 and 103 results in 136. 
- AND gate on 130 and 107 results in 137. 
- OR gate on 136 and 137 results in the third output bit 152. 
- AND gate on 131 and 104 results in 138. 
- AND gate on 130 and 108 results in 139. 
- OR gate on 138 and 139 results in the fourth output bit 153. 

After  comparison,  multiplexers  select  bits  from  Alice's  and  Bob's  inputs  based  on  the comparator's result to form the final 4-bit maximum value.  ![](Aspose.Words.78a54c2c-d82c-44f0-b684-526d78b7db84.002.png)

2. **Running the Project** 
1. **Pre-requisites** 
1. **Python Version:** 
- Ensure Python 3 is installed. Verify with: 

  python3 --version 

- If not installed, download and install Python 3 from[ python.org.](https://www.python.org/downloads/) 
2. **Package Installation:** 
- Install dependencies using pip: 

  pip install -r requirements.txt 

2. **Execution** 
1. **Open Terminals:** 
- Open two terminal windows. 
2. **Run Bob's Instance:** 
- In one terminal, navigate to the project directory and run: 

  python3 main.py bob -i inputs/bob.txt 

3. **Run Alice's Instance:** 
- In the other terminal, navigate to the project directory and run: 

  python3 main.py alice -i inputs/alice.txt 

3. **Expected Output** 
- Both terminals should display the computation result and verification status: 

  Reading data from txt file Received compute 4-bit Result of function is 15 Verified correctly ![](Aspose.Words.78a54c2c-d82c-44f0-b684-526d78b7db84.003.png)

**3. Documentation for Provided Code** 

**Directory Structure** 

├── alice.py 

├── bob.py 

├── circuits 

│   └── computerMaximum.json ├── inputs 

│   ├── alice.txt 

│   └── bob.txt 

├── main.py 

├── ot.py 

├── util.py 

└── yao.py 

**Code Explanation** 

- **alice.py:**  Implements  Alice's  role  in  Yao's  protocol,  managing  garbled  circuit evaluation and communication with Bob. 
- **bob.py:** Defines Bob's role in Yao's protocol, processing private data, evaluating the garbled circuit, and verifying results. 
- **ot.py:** Implements the Oblivious Transfer (OT) protocol, essential for secure multi- party computation. 
- **util.py:** Provides utilities for secure computation using Yao's protocol, including socket communication and cryptographic operations. 

***1.1. Code Explanation*** 

Using the original code from the repo blow are the  details of code added and the updated to it. 

1\. util.py 

**Purpose:** util.py serves as a fundamental module providing utilities essential for secure computation using Yao's protocol. It includes functionalities for socket communication, prime number  generation,  byte/bit  manipulation,  and  cryptographic  operations.  Recent  updates enhance its capabilities by adding features like processing private data and specialized socket classes tailored for secure computation. 

**Functions:** 

1. **process\_private\_data** 
- **Purpose:** Processes private data for computing the maximum value, filtering data to fit within the specified bit size, and providing its binary representation. 
- **Parameters:** 
- name (optional, str): Identifier for the data source (default: ""). 
- bit\_size (optional, int): Maximum bit size for each number (default: 16). 
- file\_read (optional, bool): Indicates if data should be read from a file (default: False). 
- filename (optional, str): Name of the file from which to read data (if file\_read is True). 
- data (optional, list): Direct input of data as a list of integers. 
- **Returns:** A tuple containing: 
- A list of processed data points. 
- The binary representation of the local maximum value. 
2. **circuit\_t\_int** 
- **Purpose:**  Converts  a  dictionary  containing  binary  values  into  an  integer, representing the combined string values of the dictionary keys. 
- **Parameters:** 
- d (dict): Dictionary where keys represent binary positions, and values are binary digits. 
- **Returns:** An integer representing the combined string values of the dictionary keys. 

**Classes:** 

1. **Socket** 
- **Purpose:** Base class for handling socket communication using ZeroMQ. 
- **Methods:** 
- send(msg): Sends a message. 
- receive(): Receives a message. 
- send\_wait(msg): Sends a message and waits for a response. 
- poll\_socket(timetick=100):  Polls  the  socket  at  the  specified 

  interval. 

2. **EvaluatorSocket** 
- **Purpose:**  Specialized  socket  class  for  the  evaluator  role  using  ZeroMQ, representing a REP type socket bound to a local port. 
- **Parameters:** 
- endpoint  (str,  optional):  The  endpoint  to  bind  to  (default: f"tcp://\*:{LOCAL\_PORT}"). 
3. **GarblerConnection** 
- **Purpose:**  Specialized  socket  class  for  the  garbler  role  using  ZeroMQ, representing a REQ type socket connecting to a specified server. 
- **Parameters:** 
- endpoint  (str,  optional):  The  endpoint  to  connect  to  (default: f"tcp://{SERVER\_HOST}:{SERVER\_PORT}"). ![](Aspose.Words.78a54c2c-d82c-44f0-b684-526d78b7db84.004.png)

2\. main.py 

**Purpose:** main.py serves as the main entry point for executing Yao's protocol, initializing either Alice or Bob based on command-line arguments. It manages the execution of Yao's protocol  by  setting  up  logging  and  directing  control  flow  to  the  respective  party's implementation. 

**Functions:** 

1. **main** 
- **Purpose:**  Initializes  the  specified  party  (Alice,  Bob,  or  local  test)  for  Yao's protocol execution. 
- **Parameters:** 
- party (str): Role to initialize ("alice", "bob", "local"). 
- circuit\_path (str): Path to the circuit configuration JSON file (default: "src/circuits/computerMaximum.json"). 
- oblivious\_transfer  (bool):  Flag  for  enabling  oblivious  transfer (default: True). 
- print\_mode (str): Print mode for debugging (default: "none"). 
- loglevel (int): Logging level (default: logging.WARNING). 
- filename (str): Name of the file containing private data (default: ""). 
- bitsize (int): Maximum bit size for private data (default: 4). 
2. **init** 
- **Purpose:** Initializes argument parsing and starts the main function with parsed arguments. ![](Aspose.Words.78a54c2c-d82c-44f0-b684-526d78b7db84.005.png)
3. alice.py 

**Purpose:** alice.py defines the role of Alice in Yao's protocol, managing garbled circuit evaluation and communication with Bob. It integrates with ot.py and util.py to ensure secure computation and communication. 

**Class: Alice** 

1. **Initialization (\_\_init\_\_)** 
- **Purpose:** Sets up Alice's environment for protocol execution. 
- **Parameters:** 
- circuits (str): Path to circuit configuration JSON file. 
- oblivious\_transfer  (bool):  Flag  for  enabling  oblivious  transfer (default: True). 
- print\_mode (str): Print mode for debugging (default: "none"). 
- filename (str): Name of the file containing private data (default: ""). 
- bit\_size (int): Maximum bit size for private data (default: 4). 
2. **Method: start** 
- **Purpose:** Initiates the Yao protocol for Alice, sending circuits and managing protocol execution. 
- **Steps:** 
- Sends circuit details to Bob. 
- Optionally prints circuit details based on print\_mode. 
- Calculates response based on private data and received keys. 
- Verifies computed result. 
3. **Method: calculate\_response** 
- **Purpose:** Computes Alice's response to Bob's input using oblivious transfer and evaluates the garbled circuit. 
- **Parameters:** 
- entry (dict): Dictionary containing circuit details, pbits, and keys. 
4. **Method: \_get\_encr\_bits** 
- **Purpose:** Returns encrypted bits based on Alice's private value and provided pbits and keys. 
- **Parameters:** 
- pbit (bool): Boolean indicating the encryption bit (0 or 1). 
- key0, key1 (str): Encryption keys. 
5. **Method: verify** 
- **Purpose:** Verifies the correctness of the computed result against the expected maximum value. 
- **Steps:** 
- Sends  Alice's  private  maximum  value  and  the  computed  general maximum value to Bob for verification. 
- Receives and prints verification result. ![](Aspose.Words.78a54c2c-d82c-44f0-b684-526d78b7db84.006.png)

4\. bob.py 

**Purpose:** The bob.py module defines Bob's role in the Yao protocol. Bob listens for messages from Alice, processes private data, evaluates the garbled circuit, and ensures the integrity of the computed results. 

**Class: Bob** 

1. **Initialization (\_\_init\_\_)** 
- **Purpose:** Initializes Bob's socket and other necessary components for secure computation. 
- **Parameters:** 
- oblivious\_transfer  (bool):  Flag  for  enabling  oblivious  transfer (default: True). 
- filename (str): Name of the file containing private data (default: ""). 
2. **Method: listen** 
- **Purpose:** Starts listening for messages from Alice. 
- **Steps:** 
- Processes received messages and either sends evaluation results or verifies the computation. 
3. **Method: send\_evaluation** 
- **Purpose:** Sends the evaluation result of the garbled circuit based on Bob's inputs to Alice. 
- **Parameters:** 
- entry (dict): Dictionary containing circuit details, pbits, and keys. 
4. **Method: send\_response** 
- **Purpose:** Sends the response after computing the function's result based on Alice's instructions. 
- **Parameters:** 
- entry (dict): Dictionary containing circuit details, pbits, and keys. 
5. **Method: verify** 
- **Purpose:** Verifies the correctness of the computed maximum value against expected outcomes to ensure data integrity. 
- **Parameters:** 
- entry  (dict):  Dictionary  containing  Alice's  maximum  value  and  the computed general maximum value. ![](Aspose.Words.78a54c2c-d82c-44f0-b684-526d78b7db84.007.png)

**5. ot.py**

code primarily implements the Oblivious Transfer (OT) protocol, an essential component in secure multi-party computation, which enables one party (Alice) to send one of two pieces of information to another party (Bob), without knowing which piece was sent. 

The  only  updates  is  the  addition  of  the  YaoGarbler  class  and  adjustments  to  the ObliviousTransfer class, focusing on enhancing local testing capabilities and improving 

result handling. 

**Updated Functions** 

1. **YaoGarbler Class**: 
- \_\_init\_\_: Initializes with circuit data, parsing it and setting up garbled circuits. 
- start:  Initiates  the  local  Yao  protocol,  allowing  selection  of  print  modes (circuit, table, none). 
- \_print\_tables: Displays garbled tables for a specified circuit entry. 
- \_print\_evaluation:  Outputs  circuit  evaluations  for  different  input combinations. 
2. **ObliviousTransfer Class**: 
- get\_result: 
  - Sends Alice's inputs to Bob. 
  - Manages OT based on the enabled flag. 
  - Returns Bob's evaluated result using Yao's circuit evaluation. 
- send\_result: 
- Receives Alice's inputs and evaluates the circuit using Yao's library. 
- Sends the evaluation result back to Alice and returns it explicitly as a dictionary. 
