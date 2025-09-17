# Sequential Logic Design

## Overview
- Introduction of sequential circuits
- Basic storage elements
- Synchronous sequential logic analysis
- Synchronous sequential logic design
- Classic sequential logic circuits

## Introduction to Sequential Circuit
- Consist of:
  - Storage elements: Latches or flip-flops
  - Combinational Logic:
    - Implement a function of inputs
    - Inputs are signals from the outside
    - Outputs are signals to the outside
    - Other Signals: Present State, signal from the storage elements
    - Other output, Next state: input of storage element
- Combinational Logic
  - Function of next state \( \text{Next State} = f(\text{Inputs}, \text{Present State}) \)
  - Output Function (Mealy) \( \text{Output} = g(\text{Inputs}, \text{State}) \)
  - Output Function (Moore) \( \text{Output} = h(\text{Present State}) \)
  - The type of output function depends on the functionality, and has a great impact on the design

## Types of Sequential Circuits
- Depends on the times at which:
  - storage elements observe their inputs, and
  - storage elements change their state
- Synchronous
  - Behavior defined by knowledge of its signals at discrete instances of time
  - Storage elements observe inputs and can change state only in relation to a timing signal (clock pulses from a clock)
- Asynchronous
  - Behavior defined by knowledge of inputs at any instant of time and the order in continuous time in which inputs change
  - If clock is regarded as another input, all circuits are asynchronous!
  - Nevertheless, the synchronous abstraction makes complex designs tractable!

## Gate Delay Models
- Consider a simple 2-input multiplexer with function:
  - \( Y = A \) for \( S = 0 \)
  - \( Y = B \) for \( S = 1 \)
- Gate Delay Models
  - If \( Y \) is connected to \( A \), the circuit becomes:
  - With function:
    - \( Y = B \) for \( S = 1 \), and \( Y(t) \) dependent on \( Y(t - 0.9) \) for \( S = 0 \)
  - The simple combinational circuit now becomes a sequential circuit because its output is a function of a time sequence of input signals!

## Storing State
- Simulation example as input signals change with time. Changes occur every 100 ns, so that the 1 ns delays are negligible.
- \( Y \) represents the state of the circuit, not only an output.
| B | S | Y | Comment |
|---|---|---|---------|
| 1 | 0 | 0 | Y “remembers” 0 |
| 1 | 1 | 1 | Y = B when S = 1 |
| 1 | 0 | 1 | Now Y “remembers” B = 1 for S = 0 |
| 0 | 0 | 1 | No change in Y when B changes |
| 0 | 1 | 0 | Y = B when S = 1 |
| 0 | 0 | 0 | Y “remembers” B = 0 for S = 0 |
| 1 | 0 | 0 | No change in Y when B changes |

## Basic (NAND) S – R Latch
- “Cross-Coupling” two NAND gates gives the S - R Latch:
- Which has the time sequence behavior:
- \( S = 0, R = 0 \) is forbidden as input pattern
| R | S | Q | Q' | Comment |
|---|---|---|-----|---------|
| 1 | 1 | ? | ?   | Stored state unknown |
| 1 | 0 | 1 | 0   | “Set” Q to 1 |
| 1 | 1 | 1 | 0   | Now Q “remembers” 1 |
| 0 | 1 | 0 | 1   | “Reset” Q to 0 |
| 1 | 1 | 0 | 1   | Now Q “remembers” 0 |
| 0 | 0 | 1 | 1   | Both go high |
| 1 | 1 | ? | ?   | Unstable! |

## Basic (NOR) S – R Latch
- Cross-coupling two NOR gates gives the S – R Latch:
- Which has the time sequence behavior:
| R | S | Q | Q' | Comment |
|---|---|---|-----|---------|
| 0 | 0 | ? | ?   | Stored state unknown |
| 0 | 1 | 1 | 0   | “Set” Q to 1 |
| 0 | 0 | 1 | 0   | Now Q “remembers” 1 |
| 1 | 0 | 0 | 1   | “Reset” Q to 0 |
| 0 | 0 | 0 | 1   | Now Q “remembers” 0 |
| 1 | 1 | 0 | 0   | Both go low |
| 0 | 0 | ? | ?   | Unstable! |

## Clocked S - R Latch
- Has a time sequence behavior similar to the basic S-R latch except that the S and R inputs are only observed when the line C is high.
- C means “control” or “clock”.
- Adding two NAND gates to the basic S - R NAND latch gives the clocked S – R latch:
- The Clocked S-R Latch can be described by a table:
| C | S | R | Q(t + 1) | Comment |
|---|---|---|----------|---------|
| 0 | X | X | No change |  |
| 1 | 0 | 0 | No change |  |
| 1 | 0 | 1 | Q=0：Clear Q |  |
| 1 | 1 | 0 | Q=1：Set Q |  |
| 1 | 1 | 1 | Undefined |  |

## D Latch
- Adding an inverter to the S-R Latch, gives the D Latch:
- Note that there are no “indeterminate” states!
- The graphic symbol for a D Latch is:
| C | D | Q(t + 1) | Comment |
|---|---|----------|---------|
| 0 | X | No change |  |
| 1 | 0 | Q=0: Clear Q |  |
| 1 | 1 | Q=1：Set Q |  |

## D Latch with Transmission Gates
- (Details not provided in the original text)

## Flip-Flops
- The latch timing problem
- Master-slave flip-flop
- Edge-triggered flip-flop
- Standard symbols for storage elements
- Direct inputs to flip-flops
- Flip-flop timing

## The Latch Timing Problem
- Consider the following circuit:
- Suppose that initially \( Y = 0 \).
- As long as \( C = 1 \), the value of \( Y \) continues to change!
- The changes are based on the delay present on the loop through the connection from \( Y \) back to \( Y \).
- This behavior is clearly unacceptable.
- Desired behavior: \( Y \) changes only once per clock pulse

## The Latch Timing Problem (continued)
- A solution to the latch timing problem is to break the inner path from input to output within the storage element
- The commonly-used, path-breaking solutions are:
  - a master-slave flip-flop
  - an edge-triggered flip-flop

## S-R Master-Slave Flip-Flop
- The input is observed by the first latch when \( C = 1 \)
- The output is changed by the second latch when \( C = 0 \)
- The path from input to output is broken by the difference of the clocking values (\( C = 1 \) and \( C = 0 \)).
- The behavior demonstrated in the previous example can be prevented since a change of \( Y \) based on \( D \) won’t occur until the clock changes from 1 to 0.
- Consists of two clocked S-R latches in series with the clock on the second latch inverted

## S-R Master-Slave Flip-Flop Timing Parameters
- (Details not provided in the original text)

## Flip-Flop Problem
- The change in the flip-flop output is delayed by the pulse width, which makes the circuit slower
- S and/or R are permitted to change while \( C = 1 \)
  - Suppose \( Q = 0 \) and \( S \) goes to 1 and then back to 0 with \( R \) remaining at 0
    - The master latch sets to 1
    - A 1 is transferred to the slave
  - Suppose \( Q = 0 \) and \( S \) goes to 1 and back to 0 and \( R \) goes to 1 and back to 0
    - The master latch sets and then resets
    - A 0 is transferred to the slave
  - This behavior is called 1s catching

## Flip-Flop Solution
- Use edge-triggering instead of master-slave
- An edge-triggered flip-flop ignores the pulse while it is at a constant level and triggers only during a transition of the clock signal
- Edge-triggered flip-flops can be built directly at the electronic circuit level, or
- A master-slave D flip-flop which also exhibits edge-triggered behavior can be used.

## Edge-Triggered D Flip-Flop
- It can be formed by:
  - Replacing the first clocked S-R latch with a clocked D latch or
  - Adding a D input and inverter to a master-slave S-R flip-flop
- The delay of the S-R master-slave flip-flop can be avoided since the 1s-catching behavior is not present with D replacing S and R inputs
- The change of the D flip-flop output is associated with the negative edge at the end of the pulse
- It is called a negative-edge triggered flip-flop

## Positive-Edge Triggered D Flip-Flop
- \( Q \) changes to the value on \( D \) applied at the positive clock edge within timing constraints to be specified
- Our choice as the standard flip-flop for most sequential circuits
- \( Q(t) \) is the current output of flip-flop while \( D(t) \) is the current input, and \( Q(t+1) \) represent the next output, then we have:
  - \( Q(t+1) = D(t) \)
- Formed by adding inverter to clock input

## Positive-Edge-Triggered D Flip-Flop (c ) Function Table
| Q' | Q | D | Cp | S | R |
|----|---|---|----|---|---|
| 1  | 1 | 1 | 1  | 1 | 0 |
| 0  | 1 | 0 | 1  | 0 | 1 |
| X  | X | 0 | 1  | 0 | 1 |
| X  | X | 1 | 0  | 1 | 0 |

## Standard Symbols for Storage Elements
- Latches
  - SR SR
  - S R
  - D with 0 Control
  - D C
  - D with 1 Control
  - D C
- Master-Slave Flip-Flops
  - D C
  - Triggered D
  - Triggered SR
  - S R
  - C
  - D
  - C
  - Triggered D
  - Triggered SR
  - S R
  - C
- Edge-Triggered Flip-Flops
  - Triggered D
  - D
  - C
  - Triggered D
  - D
  - C

## Direct Inputs
- Direct R and/or S inputs that control the state of the latches within the flip-flops are used for this initialization.
- For the example flip-flop shown
  - When R is 0, resets the flip-flop to the 0 state
  - When S is 0, sets the flip-flop to the 1 state
  - When R and S are both 1, flip-flop works normally
  - State undefined when R and S are both set to 0
- At power up or at reset, all or part of a sequential circuit usually is initialized to a known state before it begins operation
- This initialization is often done outside of the clocked behavior of the circuit, i.e., asynchronously.

## J-K Flip-flop
- Behavior
  - Same as S-R flip-flop with J analogous to S and K analogous to R
  - Except that J = K = 1 is allowed, and
  - For J = K = 1, the flip-flop changes to the opposite state
  - As a master-slave, has same “1s catching” behavior as S-R flip-flop
  - If the master changes to the wrong state, that state will be passed to the slave

## J-K Flip-flop (continued)
- Implementation
  - To avoid 1s catching behavior, one solution used is to use an edge-triggered D as the core of the flip-flop
  - Symbol
    - D
    - C
    - K
    - J
    - J
    - C
    - K

## T Flip-flop
- Behavior
  - Has a single input T
  - For T = 0, no change to state
  - For T = 1, changes to opposite state
  - Same as a J-K flip-flop with J = K = T
  - As a master-slave, has same “1s catching” behavior as J-K flip-flop
  - Cannot be initialized to a known state using the T input
  - Reset (asynchronous or synchronous) essential

## T Flip-flop (continued)
- Implementation
  - To avoid 1s catching behavior, one solution used is to use an edge-triggered D as the core of the flip-flop
  - Symbol
    - C
    - D
    - T
    - T
    - C

## Flip-flop Behavior Example
- Find the output waveforms for the flip-flops shown:
  - T
  - C
  - Clock
  - D,T
  - QD
  - QT
  - D
  - C

## Flip-Flop Behavior Example (continued)
- Find the output waveforms for the flip-flops shown:
  - J
  - C
  - K
  - S
  - C
  - R
  - Clock
  - S,J
  - QSR
  - QJK
  - R,K