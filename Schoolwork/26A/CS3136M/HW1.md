

## 1. Network-Layer PDU

**Question:** What is the name of the protocol data unit (PDU) at the network layer of the OSI reference model?

**Answer: C. Packet.**

The network layer handles packets and routes them between networks. For comparison, the data link layer handles frames, and the physical layer transmits bits. A transport-layer TCP PDU is called a segment.

## 2. Connectionless Service

**Question:** What is another name for connectionless service?

**Answer: D. Datagram service.**

A datagram service sends each packet independently without first establishing a connection or virtual circuit. An acknowledged datagram service is a particular kind of connectionless service; the general term requested here is **datagram service**.

## 3. OSI Layer Responsibilities

### (a) Dividing the transmitted bit stream into frames

**Answer: Data link layer (Layer 2).**

Framing is a data link layer function. This layer organizes data into frames so that the receiver can identify frame boundaries.

### (b) Determining which route through the subnet to use

**Answer: Network layer (Layer 3).**

The network layer performs routing, determining the path packets take through the network toward their destination.

## 4. Fraction of Bandwidth Used by Headers

**Given:** A seven-layer protocol hierarchy, a 1,000-byte application message, and a 20-byte header added at each layer.

The total header size is

$$
H=7\times20=140\text{ bytes}.
$$

The total transmitted size is

$$
L=1000+140=1140\text{ bytes}.
$$

Therefore, the fraction occupied by headers is

$$
f=\frac{H}{L}=\frac{140}{1140}\approx0.122807.
$$

Expressed as a percentage,

$$
100f\approx\boxed{12.3\%}.
$$

The denominator is the total transmitted size, including headers. Dividing by only the 1,000-byte payload would give overhead relative to payload, rather than the fraction of total bandwidth occupied by headers. This calculation follows the question's explicit assumption that all seven layers add a header.

## 5. Physical Length of One Bit

**Given:** A transmission rate of $10\text{ Mbps}$ and a propagation speed in coaxial cable equal to $2/3$ of the speed of light.

The propagation speed is

$$
v=\frac{2}{3}c
=\frac{2}{3}(3.0\times10^8)
=2.0\times10^8\text{ m/s}.
$$

At a bit rate of $R=10\times10^6\text{ bits/s}$, one bit lasts

$$
T_b=\frac{1}{R}=10^{-7}\text{ s}.
$$

The spatial length of one bit is the distance the signal travels during one bit interval:

$$
\ell=vT_b=\frac{v}{R}
=\frac{2.0\times10^8}{10\times10^6}
=\boxed{20.0\text{ m}}.
$$

## 6. Best-Case Satellite Request-Response Delay

**Given:** A satellite at an altitude of $h=40{,}000\text{ km}$.

Assume the client and server are on the ground, both the request and response pass through the satellite, and processing, queuing, and transmission delays are negligible. For the best-case propagation lower bound, take each ground-to-satellite leg to have length $h$.

The request travels from the client up to the satellite and down to the server, covering $2h$. The response makes the reverse trip, covering another $2h$. Thus, the total request-response path length is

$$
d=4h=4(40{,}000)=160{,}000\text{ km}.
$$

Using $c\approx300{,}000\text{ km/s}$,

$$
t_{\min}=\frac{d}{c}
=\frac{160{,}000}{300{,}000}\text{ s}
\approx0.533333\text{ s}
=\boxed{533.3\text{ ms}}.
$$

The one-way propagation delay is approximately $266.7\text{ ms}$; a request followed by its response requires the round trip. Actual delays can be larger because of slant-path geometry and other delays.

## 7. Image Transmission Times

**Given:** An uncompressed image of $1024\times768$ pixels, with 3 bytes per pixel.

The image size in bytes is

$$
S_{\text{bytes}}=1024\times768\times3
=2{,}359{,}296\text{ bytes}.
$$

Converting to bits,

$$
S=2{,}359{,}296\times8
=18{,}874{,}368\text{ bits}.
$$

The transmission time at rate $R$ is

$$
t=\frac{S}{R}.
$$

Assume the full stated rate carries image data, with no additional protocol overhead, retransmissions, or propagation delay.

| Part | Channel | Calculation | Transmission time |
| --- | --- | --- | --- |
| (a) | 56-kbps modem | $18{,}874{,}368/56{,}000=337.0422857\ldots\text{ s}$ | **337.0 s** |
| (b) | 1-Mbps cable modem | $18{,}874{,}368/1{,}000{,}000=18.874368\text{ s}$ | **18.9 s** |
| (c) | 10-Mbps Ethernet | $18{,}874{,}368/10{,}000{,}000=1.8874368\text{ s}$ | **1.9 s** |
| (d) | 100-Mbps Ethernet | $18{,}874{,}368/100{,}000{,}000=0.18874368\text{ s}$ | **0.2 s** |

## 8. Time to Inspect Every Topology

**Given:** Five routers. Each pair can have a high-speed line, a medium-speed line, a low-speed line, or no line. Each topology takes 100 ms to generate and inspect.

Treat the routers as distinct and each line as an undirected connection between two different routers. The number of router pairs is

$$
P=\binom{5}{2}=\frac{5\times4}{2}=10.
$$

Each of the ten pairs has four independent choices, so the number of candidate topologies is

$$
N=4^{10}=1{,}048{,}576.
$$

Since $100\text{ ms}=0.1\text{ s}$, the total inspection time is

$$
T=N\times0.1
=1{,}048{,}576\times0.1
=\boxed{104{,}857.6\text{ s}}.
$$

In hours,

$$
T=\frac{104{,}857.6}{3600}
\approx\boxed{29.1\text{ hours}}.
$$

