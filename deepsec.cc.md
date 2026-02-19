
Parcel Security in Android: From Mismatch to Use-After-Free

Why parcel: 

Example 1 PDD

[Android反序列化漏洞-Bundle风水 | LLeaves Blog](https://blog.lleavesg.top/article/Bundle-Fengshui)

fragile as hand-written

Parcel/Bundle design is poor designed as it depends on the previous seri


LazyBundle: Vuln -> Program Error

Then: Parcel UAF

LazyValue is an intermediate ojbect
When is it replaced by actual value? bundle.getParceable()


What is LazyValue is forwarded? serieal again

LIFO Java's recycledParcel not classical GC

lifecycle of LazyValue & parcel out of sync

- get a lazyvalue
- make the parcel recycled but still hold the lazyvalue
- get the lazyvalue and then it copys the new parcel data

CVE-2022-20452: ... Put an undefiled class in the bundle

michalbednarski/LeakValue




CVE-2025-22429


map duplicate to trigger a error so lazyvalue=0,
 but there is a try...catch


CVE-2025-48583

nest binder transaction
reentrant lock => ...


Use UAF to steal IApplicationThread binder



Fix? don't manually manage the memory. destroy instead of recycle






# Attacking Apple Display Co-processor



About DCP

Attack serface
AFK Protocol(kernel communiccate with EP)


Kernel AFK issue
by 08tc3wbb(... about CVE 2022-32824 CVE-2023-27930)

Reverse

Lots of RPC calls AP to DCP

[Project Zero: The curious tale of a fake Carrier.app](https://googleprojectzero.blogspot.com/2022/06/curious-case-carrier-app.html)


SetBlock_Impl
block_type 97 has something interesting (function ptr)

User Calibration

--

CVE-2024-54506 Heap OOBR




?????





From Embodied AI jailbreak to 


Bluetooth Based RCE to Unitree robot

LLM inject( python function call `eval(args['angle'])`)
DNS Hijack



Send low level cmd msg to control motors

highly obf-ed

dump self-decrypting code

hook ptrace use LD_preload
dump .bss using gdb
import back to IDA


VM disassenmler
using Unicorn, found many mepeated pattern-> it's a VM

...

brick the robot; Then hardware




有人做MQTT，说，在国内厂商MQTT server的client_id可以用通配符，类似superclient\*这种


# WhatsApp 0-click Exp

ImageIO

opcodes in DNG file

The "Dog" PoC

numComponents

CVE-2025-55177

RequestUrlPreview



# cc


NSPredicate


p0's iMessage blog

PAC check intigrity

dlsym gadget


NSKeyedArchiver

dyld 
