# System I - Combinational Logic Design

## Overview
- Introduction to Verilog HDL
- About combinational logic circuits
- Some classic/basic designs
- Timing analysis

## Introduction to Verilog HDL
### Background
- **Heterogeneous computing**
  - CPU vs. GPU vs. FPGA vs. ASIC
- **Digital circuit design**
  - FPGA vs. ASIC

### What is HDL?
- Hardware description language is a language that uses formal methods to describe digital circuits and design digital logic systems.

### HDL-based Design Flow
- Logic design with HDL
- Simulation
- Synthesis
- Physical Design
- Final step

### Logic design with HDL
```verilog
module top(
    input a,
    input b,
    output c
);
    assign c = a & b;
endmodule
```

### Simulation
```verilog
module sim_top();
    reg a_in, b_in;
    wire c_out;
    top dut(
        .a(a_in),
        .b(b_in),
        .c(c_out)
    );
    initial begin
        a_in = 1'b0;
        b_in = 1'b0;
        #2 b_in = 1'b1;
        #2 a_in = 1'b1;
        #2 $finish;
    end
    always @(*) begin
        $display("a=%d, b=%d, c=%d", a_in, b_in, c_out);
    end
endmodule
```

### Synthesis
- Parsing
- Multi-level synthesis
  - Non-synthesizable HDL code
- Technology mapping

### Physical Design
- Placement
- Routing
- Static timing analysis
- LVS and DRC
- Generating result
  - ASIC: layout file
  - FPGA: bitstream file

### Final Step
- **ASIC**
  - Tape-out
- **FPGA**
  - Download bitstream file

### Design Flow: ASIC vs. FPGA
[ASIC vs. FPGA Design Flow](https://www.xilinx.com/video/fpga/fpga-vs-asic-design-flow.html)

## Verilog HDL
### Lexical conventions
- Very similar to C
  - Verilog is case-sensitive
  - All keywords are in lowercase
- A Verilog program is a string of tokens
  - Whitespace
  - Comments
  - Delimiters
  - Numbers
  - Strings
  - Identifiers
  - Keywords


# Lexical Conventions and Basic Syntax in Verilog

## Lexical Conventions

### Whitespace
- Blank space (`\b`)
- Tab (`\t`)
- Newline (`\n`)
- Whitespace is ignored in Verilog except:
  - In strings
  - When separating tokens

### Comments
- Used for readability and documentation
- Just like C:
  - `//` single line comment
  - `/*` multi-line comment `*/`
  - Nested comments (e.g., `/* Nested comments /* like this */`) may not be acceptable (depends on Verilog compiler)

### Number Specification

#### Sized Numbers
- General syntax: `<size>'<base><number>`
  - `<size>`: number of bits (in decimal)
  - `<number>`: the number in radix `<base>`
  - `<base>`:
    - `d` or `D` for decimal (radix 10)
    - `b` or `B` for binary (radix 2)
    - `o` or `O` for octal (radix 8)
    - `h` or `H` for hexadecimal (radix 16)
- Examples:
  - `4'b1111`
  - `12'habc`
  - `16'd255`

#### Unsized Numbers
- Default base is decimal
- Default size is at least 32 (depends on Verilog compiler)
- Examples:
  - `23232`
  - `'habc`
  - `'o234`

#### X or Z Values
- Unknown value: lowercase `x`
  - 4 bits in hex, 3 bits in octal, 1 bit in binary
- High-impedance value: lowercase `z`
  - 4 bits in hex, 3 bits in octal, 1 bit in binary
- Examples:
  - `12'h13x`
  - `6'hx`
  - `32'bz`
- Extending the most-significant part:
  - Applied when `<size>` is bigger than the specified value
  - Filled with `x` if the specified MSB is `x`
  - Filled with `z` if the specified MSB is `z`
  - Zero-extended otherwise
- Examples:
  - `6'hx`

#### Negative Numbers
- Put the sign before the `<size>`
- Examples:
  - `-6'd3`
  - `4'd-2` // illegal
- Two’s complement is used to store the value

#### Underscore Character and Question Marks
- Use `_` to improve readability
  - Example: `12'b1111_0000_1010`
  - Not allowed as the first character
- `?` is the same as `z` (only regarding numbers)
  - Example: `4'b10??` // the same as `4'b10zz`

### Strings
- As in C, use double-quotes
- Examples:
  - `"Hello world!"`
  - `"a / b"`
  - `"text\tcolumn1\bcolumn2\n"`

### Identifiers and Keywords
- Identifiers: alphanumeric characters, `_`, and `$`
  - Should start with an alphabetic character or `_`
  - Only system tasks can start with `$`
- Keywords: identifiers reserved by Verilog
- Examples:
  - `reg value;`
  - `input clk;`

### Escaped Identifiers
- Start with `\`
- End with whitespace (space, tab, newline)
- Can have any printable character between start and end
- The `\` and whitespace are not part of the identifier
- Examples:
  - `\a+b-c` // `a+b-c` is the identifier
  - `\**my_name**` // `**my_name**` is the identifier
- Used as name of modules

## Basic Syntax: Module, Port, and Instantiate

### Module and Port
```verilog
module model-name (port list);
    <Port definition> // optional
    Data type definition
    Logic function description
endmodule
```

### Instantiate
```verilog
model-name instance-identifier (port related list);
```
- Example:
```verilog
module top( input a, input b, output c );
    assign c = a & b;
endmodule

module sim_top();
    reg a_in, b_in;
    wire c_out;
    top dut( .a(a_in), .b(b_in), .c(c_out) );
    initial begin
        a_in = 1'b0;
        b_in = 1'b0;
        #2 b_in = 1'b1;
        #2 a_in = 1'b1;
        #2 $finish;
    end
    always @(*) begin
        $display("a=%d,b=%d,c=%d, a_in,b_in,c_out);
    end
endmodule
```

## Basic Syntax: Data Type

### Net
- Physical connection (wire type)

### Register
- Storage element (reg type)

### Vectors and Arrays
- Vector: multi-bit signal
  - Example: `wire[7:0] a; reg[31:0] rdata, wdata;`
- Array:
  - Example: `wire b[2:0]` or `reg[15:0] mem [1023:0]`

### Parameter
- Local scope (the current module)
- Usually defined as constant

## Basic Syntax: Data Type (cont’d)

### Module’s Port Type
- Input
  - Definition: `wire`
  - Instantiate: `wire` or `reg`
- Output
  - Definition: `wire` or `reg`
  - Instantiate: `wire`

### Examples
```verilog
module Right ( input in1, input wire in2, input [3:0] in3, output out1, output [3:0] out2, output reg [1:0] out3 );
    ...
endmodule

module Wrong ( input reg in1, output out1 [2:0] );
    ...
endmodule
```

## Basic Syntax: Operator and Precedence

### Operators
- Unary operators:
  - `+`
- Bitwise operators:
  - `~ & | ^ ^~`
- Arithmetic operators:
  - `+ - * / %`
- Reduction operators:
  - `& ~& | |~ ^ ^~`
- Logic operators:
  - `&& || !`
- Logic equality operators:
  - `== !=`
- Relational operators:
  - `< <= > >=`
- Bit Concatenation operators:
  - `{ }`
- Shift operators:
  - `>> <<`
- Conditional operator:
  - `?:`

## Modeling Methods

### Structured Modeling
- Module-level
- Gate-level
- Switch-level

### Dataflow Modeling
- Suitable for modeling combinational logic circuits
- Use continuous assignment statements: `assign`

### Behavioral Modeling
- Key elements:
  - `always`
  - `always @(event signal list)`
  - Procedure statement

# Combinational vs. Sequential Circuits

## Combinational Circuits
- **Memory-less:**
  - The output value depends ONLY on the current input values.

## Sequential Circuits
- **Composition:**
  - Consist of combinational logic as well as memory elements (used to store certain circuit states).
- **Output Dependency:**
  - Outputs depend on BOTH current input values and previous input values (kept in the storage elements).

## Combinational Circuit (n-inputs, m-outputs)
- **Output Dependency:**
  - Depends only on inputs.

## Sequential Circuit (n-inputs, m-outputs)
- **Components:**
  - Combinational Circuit
  - Storage Elements
  - Next state

## Characteristics of Combinational Logic Circuits
- **Elements:**
  - Each element is a combinational logic circuit.
- **Node Output:**
  - A node can only be the output of one element.
- **Loop:**
  - Loop is not allowed.

## Design Choice Of Combinational Circuits
- **2-level vs. Multi-level:**
  - Gate delay
  - Fan-in/fan-out
  - Trade-off between cost and speed
- **Functional Blocks**

## Design Procedure
1. **Specification**
   - Write a specification for the circuit if one is not already available (text, HDL).
2. **Formulation**
   - Derive a truth table or initial Boolean equations that define the required relationships between the inputs and outputs, if not in the specification.
3. **Optimization**
   - Apply 2-level and multiple-level optimization.
   - Draw a logic diagram or provide a netlist for the resulting circuit using ANDs, ORs, and inverters.
4. **Technology Mapping**
   - Map the logic diagram or netlist to the implementation technology selected.
5. **Verification**
   - Verify the correctness of the final design.

## Transformation
- **Steps:**
  - Optimization
  - Problem Truth Table
  - Optimum function
  - Transferred function
  - Logic Circuit
  - Logic abstraction
  - Assignment

## Design Example 1
### Specification
- **Analysis Result:**
  - Input Signal: Switches $S1, S2, S3$
  - Output Signal: Light $F$
  - "1" for switch closed and "0" for opened
  - "1" for light on and "0" for light off

### Truth Table
| $S3$ | $S2$ | $S1$ | $F$ |
|----------|----------|----------|---------|
| 0        | 0        | 0        | 0       |
| 0        | 0        | 1        | 1       |
| 0        | 1        | 0        | 1       |
| 0        | 1        | 1        | 0       |
| 1        | 0        | 0        | 1       |
| 1        | 0        | 1        | 0       |
| 1        | 1        | 0        | 0       |
| 1        | 1        | 1        | 1       |

### Formulation
\[ F = S1 S2 S3 + S1 S2 S3 + S1 S2 S3 + S1 S2 S3 \]

### Optimization
- **Truth Table:**
  | $S3$ | $S2$ | $S1$ | $F$ |
  |----------|----------|----------|---------|
  | 0        | 0        | 0        | 0       |
  | 0        | 0        | 1        | 1       |
  | 0        | 1        | 0        | 1       |
  | 0        | 1        | 1        | 0       |
  | 1        | 0        | 0        | 1       |
  | 1        | 0        | 1        | 0       |
  | 1        | 1        | 0        | 0       |
  | 1        | 1        | 1        | 1       |

### Technology Mapping
- **Least use of gates?**

### Verilog Programming
```verilog
module lamp_control(s1,s2,s3,F);
  input s1,s2,s3;
  output F;
  wire s1,s2,s3,f;
  assign F = (~s3&~s2&s1) | (~s3&s2&~s1) | (s3&~s2&~s1) | (s3&s2&s1);
endmodule
```

## Design Example 2
### Specification
- **BCD to Excess-3 code converter**
  - Transforms BCD code for the decimal digits to Excess-3 code for the decimal digits.
  - BCD code words for digits 0 through 9: 4-bit patterns 0000 to 1001, respectively.
  - Excess-3 code words for digits 0 through 9: 4-bit patterns consisting of 3 (binary 0011) added to each BCD code word.
  - Implementation:
    - multiple-level circuit
    - NAND gates (including inverters)

### Formulation
- **Conversion of 4-bit codes:**
  - Variables - BCD: $A, B, C, D$
  - Variables - Excess-3: $W, X, Y, Z$
  - Don’t Cares - BCD 1010 to 1111

### Truth Table
| Input BCD $A$ $B$ $C$ $D$ | Output Excess-3 $WXYZ$ |
|------------------------------------------|---------------------------|
| 0 0 0 0                                  | 0 1 1                     |
| 0 0 0 1                                  | 0 1 0 0                   |
| 0 0 1 0                                  | 0 1 0 1                   |
| 0 0 1 1                                  | 0 1 1 0                   |
| 0 1 0 0                                  | 0 1 1 1                   |
| 0 1 0 1                                  | 1 0 0 0                   |
| 0 1 1 0                                  | 1 0 0 1                   |
| 0 1 1 1                                  | 1 0 1 0                   |
| 1 0 0 0                                  | 1 0 1 1                   |
| 1 0 0 1                                  | 1 1 0 0                   |

### Optimization
#### 2-level using K-maps
- **Karnaugh Maps:**
  - $W = A + BC + BD$
  - $X = \overline{B} \cdot T1 + B \cdot \overline{T1}$
  - $Y = CD + \overline{T1}$
  - $Z = \overline{D}$

- **Karnaugh Map for W:**
  | $CD$ | $AB$ | 00 | 01 | 11 | 10 |
  |----------|----------|----|----|----|----|
  | 00       | 00       | 1  | 1  | 1  |    |
  | 01       | 01       | 1  | 1  |    |    |
  | 11       | 11       |    |    |    |    |
  | 10       | 10       | 1  | 1  |    |    |

- **Karnaugh Map for X:**
  | $CD$ | $AB$ | 00 | 01 | 11 | 10 |
  |----------|----------|----|----|----|----|
  | 00       | 00       |    | 1  | 1  |    |
  | 01       | 01       | 1  |    |    |    |
  | 11       | 11       |    |    |    |    |
  | 10       | 10       | 1  |    |    |    |

- **Karnaugh Map for Y:**
  | $CD$ | $AB$ | 00 | 01 | 11 | 10 |
  |----------|----------|----|----|----|----|
  | 00       | 00       | 1  |    |    |    |
  | 01       | 01       |    |    |    |    |
  | 11       | 11       | 1  | 1  |    |    |
  | 10       | 10       |    |    |    |    |

- **Karnaugh Map for Z:**
  | $CD$ | $AB$ | 00 | 01 | 11 | 10 |
  |----------|----------|----|----|----|----|
  | 00       | 00       | 1  |    |    |    |
  | 01       | 01       |    |    |    |    |
  | 11       | 11       |    |    |    |    |
  | 10       | 10       | 1  |    |    |    |

#### Multiple-level using transformations
- **Extraction:**
  - $T1 = C + D$
  - $W = A + B \cdot T1$
  - $X = \overline{B} \cdot T1 + B \cdot \overline{T1}$
  - $Y = CD + \overline{T1}$
  - $Z = \overline{D}$

### Technology Mapping
- **Mapping with a library containing:**
  - Inverters
  - 2-input NAND
  - 3-input NAND
  - 2-input NOR
  - 2-2 AOI gates

### Verilog Programming
```verilog
module BCD_Excess_3(A,B,C,D,W,X,Y,Z);
  input A,B,C,D;
  output W,X,Y,Z;
  wire A,B,C,D, W,X,Y,Z,T1;
  assign T1 = C | D;
  assign W = A | B & C | B & D;
  assign X = ~B & T1 | B & ~T1;
  assign Y = C & D | ~T1;
  assign Z = ~D;
endmodule
```

# Combinational Logic

## Overview

- Introduction to Verilog HDL
- About combinational logic circuits
- Some classic/basic designs
- Timing analysis

## Some Classic/Basic Designs

- Functions and functional blocks
- Rudimentary logic functions
- Encoder and decoder
- Multiplexer and demultiplexer
- Half adder and full adder

## Functions and Functional Blocks

The functions considered are those found to be very useful in design. Corresponding to each function is a combinational circuit implementation called a functional block. In the past, many functional blocks were implemented as SSI, MSI, and LSI circuits. Today, they are often used as simply parts within a VLSI circuit.

## Rudimentary Logic Functions

Four elementary combinational logic functions:

- Value-Fixing: $F = 0$ or $F = 1$, no Boolean operator
- Transferring: $F = X$, no Boolean operator
- Inverting: $F = \overline{X}$, involves one logic gate
- Enabling: $F = X \cdot EN$ or $F = X + EN$, involves one or two logic gates

The first three are functions of a single variable $X$.

| $X$ | $F = 0$ | $F = X$ | $F = \overline{X}$ | $F = 1$ |
|---------|-------------|-------------|------------------------|-------------|
| 0       | 0           | 0           | 1                      | 1           |
| 1       | 0           | 1           | 0                      | 1           |

## Multiple-bit Rudimentary Functions

Multi-bit Examples:

- A wide line is used to represent a bus which is a vector signal.
- In the example, $F = (F3, F2, F1, F0)$ is a bus.
- The bus can be split into individual bits.
- Sets of bits can be split from the bus.
- The sets of bits need not be continuous.

## Enabling Function

Enabling permits an input signal to pass through to an output. Disabling blocks an input signal from passing through to an output, replacing it with a fixed value. The value on the output when it is disabled can be Hi-Z (as for three-state buffers and transmission gates), 0, or 1.

## Decoding

Decoding - the conversion of an $n$-bit input code to an $m$-bit output code with $n \leq m \leq 2^n$ such that each valid code word produces a unique output code. Circuits that perform decoding are called decoders.

## Classic Designs: Decoder

Multiple inputs: address, binary code, ...

Multiple outputs: one-hot, ...

Example:

- 3-bit binary input, 8-bit output.
- When the input 3 bits are 000, then the first bit in output is 1, and others are 0.
- When the input 3 bits are 001, then only the second bit in output is 1.

## Decoder Examples

- 1-to-2-Line Decoder
- 2-to-4-Line Decoder

The 2-4-line is made up of 2 1-to-2-line decoders and 4 (2-inputs) AND gates.

| $A2$ | $A1$ | $A0$ | $D0$ | $D1$ | $D2$ | $D3$ | $D4$ | $D5$ | $D6$ | $D7$ |
|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| 0        | 0        | 0        | 1        | 0        | 0        | 0        | 0        | 0        | 0        | 0        |
| 0        | 0        | 1        | 0        | 1        | 0        | 0        | 0        | 0        | 0        | 0        |
| 0        | 1        | 0        | 0        | 0        | 1        | 0        | 0        | 0        | 0        | 0        |
| 0        | 1        | 1        | 0        | 0        | 0        | 1        | 0        | 0        | 0        | 0        |
| 1        | 0        | 0        | 0        | 0        | 0        | 0        | 1        | 0        | 0        | 0        |
| 1        | 0        | 1        | 0        | 0        | 0        | 0        | 0        | 1        | 0        | 0        |
| 1        | 1        | 0        | 0        | 0        | 0        | 0        | 0        | 0        | 1        | 0        |
| 1        | 1        | 1        | 0        | 0        | 0        | 0        | 0        | 0        | 0        | 1        |

## Decoder Expansion

General procedure for any decoder with $n$ inputs and $2^n$ outputs:

1. Let $k = n$
2. There are $2^k$ AND gates which will be driven by 2 decoders.
   - If $k$ is even, both decoders have $2^{k/2}$ outputs.
   - If $k$ is odd, one decoder has $2^{(k+1)/2}$ outputs, while another one has $2^{(k-1)/2}$ outputs.
3. For each decoder obtained from step 2, let the number of outputs becomes $k$, and repeat step 2 until $k=1$ (i.e., 1-to-2-line decoder).

## Decoder Expansion: 3-8 Decoder

- Number of output ANDs = 8
- Number of inputs to decoders driving output ANDs = 3
- Closest possible split to equal:
  - 2-to-4-line decoder
  - 1-to-2-line decoder

## Decoder Expansion: 3-8 Decoder (cont’d)

- Number of output ANDs = 4
- Number of inputs to decoders driving output ANDs = 2
- Closest possible split to equal:
  - Two 1-to-2-line decoders

## Decoder with Enable

In general, attach $m$-enabling circuits to the outputs. See truth table below for function. Note use of X’s to denote both 0 and 1. Combination containing two X’s represent four binary combinations. Alternatively, can be viewed as distributing value of signal EN to 1 of 4 outputs. In this case, called a demultiplexer.

| $EN$ | $A1$ | $A0$ | $D0$ | $D1$ | $D2$ | $D3$ |
|----------|----------|----------|----------|----------|----------|----------|
| 0        | X        | X        | 1        | 1        | 1        | 1        |
| 1        | 0        | 0        | 0        | 0        | 0        | 1        |
| 1        | 0        | 1        | 0        | 0        | 1        | 0        |
| 1        | 1        | 0        | 0        | 1        | 0        | 0        |
| 1        | 1        | 1        | 1        | 0        | 0        | 0        |

## Combinational Logic Implementation - Decoder and OR Gates

Implement $m$ functions of $n$ variables with:

- Sum-of-minterms expressions
- One $n$-to-$2^n$-line decoder
- $m$ OR gates, one for each output

Approach 1:

- Find the truth table for the functions.
- Make a connection to the corresponding OR from the corresponding decoder output wherever a 1 appears in the truth table.

Approach 2:

- Find the minterms for each output function.
- OR the minterms together.

## Decoder and OR Gates Example

Implement a binary Adder. Finding sum of minterms expressions:

\[ S(X, Y, Z) = \sum m(1, 2, 4, 7) \]
\[ C(X, Y, Z) = \sum m(3, 5, 6, 7) \]

Find circuit. Truth Table:

| $X$ | $Y$ | $Z$ | $S$ | $C$ |
|---------|---------|---------|---------|---------|
| 0       | 0       | 0       | 0       | 0       |
| 0       | 0       | 1       | 1       | 0       |
| 0       | 1       | 0       | 1       | 0       |
| 0       | 1       | 1       | 0       | 1       |
| 1       | 0       | 0       | 1       | 0       |
| 1       | 0       | 1       | 0       | 1       |
| 1       | 1       | 0       | 0       | 1       |
| 1       | 1       | 1       | 1       | 1       |

## Seven-Segment Display Decoder

| $I0$ | $I1$ | $I2$ | $I3$ | $Oa$ | $Ob$ | $Oc$ | $Od$ | $Oe$ | $Of$ | $Og$ |
|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| 0        | 0        | 0        | 0        | 1        | 1        | 1        | 1        | 1        | 1        | 0        |
| 0        | 0        | 0        | 1        | 0        | 1        | 1        | 0        | 0        | 0        | 0        |
| 0        | 0        | 1        | 0        | 1        | 1        | 0        | 1        | 1        | 0        | 1        |
| 0        | 0        | 1        | 1        | 1        | 1        | 1        | 1        | 0        | 0        | 1        |
| 0        | 1        | 0        | 0        | 0        | 1        | 1        | 0        | 0        | 1        | 1        |
| 0        | 1        | 0        | 1        | 1        | 0        | 1        | 1        | 0        | 1        | 1        |
| 0        | 1        | 1        | 0        | 1        | 0        | 1        | 1        | 1        | 1        | 1        |
| 0        | 1        | 1        | 1        | 1        | 1        | 1        | 0        | 0        | 0        | 0        |
| 1        | 0        | 0        | 0        | 1        | 1        | 1        | 1        | 1        | 1        | 1        |
| 1        | 0        | 0        | 1        | 1        | 1        | 1        | 1        | 0        | 1        | 1        |

## Common electrode

Common Anode Display (CAD):

- All the anode connections of the LED's are joined together to logic "1" and the individual segments are illuminated by connecting the individual Cathode terminals to a "LOW", logic "0" signal.
- $a \sim g = 0$ on, $a \sim g = 1$ off (Active Low)

Common Cathode Display (CCD):

- All the cathode connections of the LED's are joined together to logic "0" or ground.
- The individual segments are illuminated by application of a "HIGH", logic "1" signal to the individual Anode terminals.
- $a \sim g = 1$ on, $a \sim g = 0$ off (Active High)

## BCD-to-Seven Segment Decoder

Truth Table for BCD-to-Seven-Segment Decoder:

| $I0$ | $I1$ | $I2$ | $I3$ | $Oa$ | $Ob$ | $Oc$ | $Od$ | $Oe$ | $Of$ | $Og$ |
|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| 0        | 0        | 0        | 0        | 1        | 1        | 1        | 1        | 1        | 1        | 0        |
| 0        | 0        | 0        | 1        | 0        | 1        | 1        | 0        | 0        | 0        | 0        |
| 0        | 0        | 1        | 0        | 1        | 1        | 0        | 1        | 1        | 0        | 1        |
| 0        | 0        | 1        | 1        | 1        | 1        | 1        | 1        | 0        | 0        | 1        |
| 0        | 1        | 0        | 0        | 0        | 1        | 1        | 0        | 0        | 1        | 1        |
| 0        | 1        | 0        | 1        | 1        | 0        | 1        | 1        | 0        | 1        | 1        |
| 0        | 1        | 1        | 0        | 1        | 0        | 1        | 1        | 1        | 1        | 1        |
| 0        | 1        | 1        | 1        | 1        | 1        | 1        | 0        | 0        | 0        | 0        |
| 1        | 0        | 0        | 0        | 1        | 1        | 1        | 1        | 1        | 1        | 1        |
| 1        | 0        | 0        | 1        | 1        | 1        | 1        | 1        | 0        | 1        | 1        |

## Encoder

8-to-3-line encoder:

| $I0$ | $I1$ | $I2$ | $I3$ | $I4$ | $I5$ | $I6$ | $I7$ | $O0$ | $O1$ | $O2$ |
|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| 1        | 0        | 0        | 0        | 0        | 0        | 0        | 0        | 0        | 0        | 0        |
| 0        | 1        | 0        | 0        | 0        | 0        | 0        | 0        | 0        | 0        | 1        |
| 0        | 0        | 1        | 0        | 0        | 0        | 0        | 0        | 0        | 1        | 0        |
| 0        | 0        | 0        | 1        | 0        | 0        | 0        | 0        | 0        | 1        | 1        |
| 0        | 0        | 0        | 0        | 1        | 0        | 0        | 0        | 1        | 0        | 0        |
| 0        | 0        | 0        | 0        | 0        | 1        | 0        | 0        | 1        | 0        | 1        |
| 0        | 0        | 0        | 0        | 0        | 0        | 1        | 0        | 1        | 1        | 0        |
| 0        | 0        | 0        | 0        | 0        | 0        | 0        | 1        | 1        | 1        | 1        |

## Priority Encoder Example

Priority encoder with 4 inputs $(D3, D2, D1, D0)$ - highest priority to most significant 1 present - Code outputs $A1, A0$ and $V$ where $V$ indicates at least one 1 present.

| No. of Minterms/Row | Inputs | Outputs |
|---------------------|--------|---------|
| 1                   | 0 0 0 0 | X X 0   |
| 1                   | 0 0 0 1 | 0 0 1   |
| 2                   | 0 0 1 X | 0 1 1   |
| 4                   | 0 1 X X | 1 0 1   |
| 8                   | 1 X X X | 1 1 1   |

## Multiplexer

Selecting of data or information is a critical function in digital systems and computers. Circuits that perform selecting have:

- A set of information inputs from which the selection is made
- A single output
- A set of control lines for making the selection

Logic circuits that perform selecting are called multiplexers. Selecting can also be done by three-state logic or transmission gates.

## Multiplexers

A multiplexer selects information from an input line and directs the information to an output line. A typical multiplexer has $n$ control inputs $(S_{n-1}, \ldots, S0)$ called selection inputs, $2^n$ information inputs $(I_{2n-1}, \ldots, I0)$, and one output $Y$. A multiplexer can be designed to have $m$ information inputs with $m < 2^n$ as well as $n$ selection inputs.

## 2-to-1-Line Multiplexer

Since $2 = 2^1$, $n = 1$. The single selection variable $S$ has two values:

- $S = 0$ selects input $I0$
- $S = 1$ selects input $I1$

The equation: $Y = I0 + SI1$

## 4-to-1-line Multiplexer

Input Output

| $S0$ | $S1$ | $F$  |
|----------|----------|----------|
| 0        | 0        | $A$  |
| 0        | 1        | $B$  |
| 1        | 0        | $C$  |
| 1        | 1        | $D$  |

## Multiplexer Width Expansion

Select “vectors of bits” instead of “bit”. Use multiple copies of $2n \times 2$ AND-OR in parallel. Example: 4-to-1-line quad multiplexer

## Other Selection Implementations

- Three-state logic in place of AND-OR
- Gate input cost = 18

## Other Selection Implementations

- Distributing the decoding across the three-state drivers
- Gate input cost = 14
- GN of AND-OR gate implementation: 22
- GN of implementation with AND-OR gate replaced by three-state drivers: 18

## Other Selection Implementations

- Transmission Gate Multiplexer
- Gate input cost = 8 compared to 14 for 3-state logic and 18 or 22 for gate logic

## Combinational Logic Implementation - Multiplexer Approach 1

Implement $m$ functions of $n$ variables with:

- Sum-of-minterms expressions
- An $m$-wide $2^n$-to-1-line multiplexer

Design:

- Find the truth table for the functions.
- In the order they appear in the truth table:
  - Apply the function input variables to the multiplexer inputs $S_{n-1}, \ldots, S0$
  - Label the outputs of the multiplexer with the output variables
  - Value-fix the information inputs to the multiplexer using the values from the truth table (for don’t cares, apply either 0 or 1)

## One Bit Binary Adder By Multiplexer

Implementing a 1-bit Binary Adder with a Dual 8-to-1-Line Multiplexer

- Truth table
- Circuit


# Overview
- Introduction to Verilog HDL
- About combinational logic circuits
- Some classic/basic designs
- Timing analysis

# Timing Analysis
## Circuit delay
### Ideal case
### In practice
- Rise-time delay of the transmission gate
- Delay of the invertor

## Propagation delay
- $T_{pd} = \text{max delay from input to output}$

## Contamination delay
- $T_{cd} = \text{min delay from input to output}$

## Reasons why $T_{pd}$ and $T_{cd}$ may be different:
- Different rising and falling delays
- Multiple inputs and outputs, some of which are faster than others
- Circuits slow down when hot and speed up when cold

# Timing Analysis (cont’d)
## The critical (longest) path
- $T_{pd}$ of the circuit = $\sum$ all $T_{pd}$ of circuit elements along the critical path

## The shortest path
- $T_{cd}$ of the circuit = $\sum$ all $T_{cd}$ of circuit elements along the shortest path

# Timing Analysis (cont’d)
- A B
- C
- D Y
- Critical Path
- Short Path
- $n1$
- $n2$
- $T_{pd} = 2T_{pd\_\text{AND}} + T_{pd\_\text{OR}}$
- $T_{cd} = T_{cd\_\text{AND}}$

## Race hazard
- Glitch: when a single input change causes multiple output changes

# Timing Analysis (cont’d)
- N1
- Race hazard in a circuit
- No glitch
- Glitch

# Analysis of Logic Circuits
1. Write the Boolean function for the circuit
   - begin with the input signal
   - Define the relationship of each gate
   - optimization
2. Derive a truth table
   - Define the relationships between the inputs and outputs,
3. Functional Analysis
   - Define the function of each signal and the whole circuit
   - Draw the timing diagram of the circuit
4. Verification
   - Verify the correctness of the final design

# Analyze the Function of the Logic Circuit
- List the Boolean functions for all signals
- $P1 = A \oplus B$
- $P2 = B \oplus C$
- $P3 = C \oplus A$
- $P4 = P1 + P2$
- $P5 = P3 + P4$
- $P6 = P5 \cdot (A \cdot B)$
- $F = P6 + P4 \cdot (C \cdot A)$

# Logic Circuits
- $P1 = A \oplus B$
- $P2 = B \oplus C$
- $P3 = C \oplus A$
- $P4 = P1 + P2$
- $P5 = P3 + P4$
- $P6 = P5 \cdot (A \cdot B)$
- $F = P6 + P4 \cdot (C \cdot A)$

# Boolean Function Simplification
- Derive the truth table
- $F = (A \oplus B) + (B \oplus C) \cdot (A \cdot B)$
- $F = (A \oplus B) + (B \oplus C) \cdot (A \cdot B) + (C \oplus A) \cdot (A \cdot B)$
- $F = (A \oplus B) + (B \oplus C) \cdot (A \cdot B) + (C \oplus A) \cdot (A \cdot B) + (A \cdot B \cdot C)$
- $F = (A \oplus B) + (B \oplus C) \cdot (A \cdot B) + (C \oplus A) \cdot (A \cdot B) + (A \cdot B \cdot C) + (A \cdot B \cdot C)$
- $F = (A \oplus B) + (B \oplus C) \cdot (A \cdot B) + (C \oplus A) \cdot (A \cdot B) + (A \cdot B \cdot C) + (A \cdot B \cdot C) + (A \cdot B \cdot C)$
- $F = (A \oplus B) + (B \oplus C) \cdot (A \cdot B) + (C \oplus A) \cdot (A \cdot B) + (A \cdot B \cdot C) + (A \cdot B \cdot C) + (A \cdot B \cdot C) + (A \cdot B \cdot C)$

# Boolean Function Simplification
- From the truth table, we can see that $F=1$ if $A \neq B$ or $B < C$.
- The original design is not the best. Use the following circuits instead.
- Derive the truth table

# Summary
- Introduction to Verilog HDL
- About combinational logic circuits
- Some classic/basic designs
- Timing analysis