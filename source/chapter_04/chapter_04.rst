Theory: Data-Link Layer
***********************

Layer 2 of the networking stack is the *data-link* layer, responsible
for transmitting bursts of data between two networked devices, known as
*nodes*. Just about anything can be a node: computers, smart phones,
tablets, and even light switches. We call each burst of data a *frame*,
which contains groupings of data called *packets*. I'll discuss packets
in detail in the *networking layer* chapter (Chapter 6); for now, just
know that frames are at Layer 2, and packets are at Layer 3.

Protocols like Bluetooth, USB, CAN-Bus, I\ :sup:`2`\ C, and Ethernet
live at Layer 2, and they allow you to link over wireless, wired, or
fiber optic links. Each of these protocols are best at certain tasks:

* Ethernet: Great for networking computers. Supports wired, wireless, and
  fiber-optics.
* USB: Ideal for connecting keyboards, mice, phones, and other devices to your
  computer.
* Bluetooth: Wirelessly connect a device to a computer or phone.
* CAN-Bus: Used to connect parts in a car or pieces of industrial equipment.
* I\ :sup:`2`\ C: Perfect for connecting smaller, cheaper electronics like switches,
  sensors, and robotics.

This chapter focuses on the theory behind the data-link layer, which is
generally made up of two sublayers: the *Media Access Control (MAC)*
protocol that controls which node has access to the transmitting medium,
and the optional and often no longer used *Logical Link Control (LLC)*.
Before TCP/IP—the protocol the internet runs on—became commonplace, LLC
helped multiple types of protocols share the same network (we'll cover
TCP/IP in depth in Chapter 6). We don't use LLC very often anymore, so
we can concentrate on the MAC sublayer instead and familiarize ourselves
with the most common Layer 2 standards and popular frame formats.

Network Topology
================

A *network topology* describes how nodes are connected to form a network
and which nodes have direct connections. Each topology has advantages
and disadvantages.

Direct Point-to-Point Topology

The simplest topology is *direct point-to-point topology*, where we
directly connect one node to another (:numref:`p2p`).

.. _p2p:
.. figure:: media/p2p.svg
   :alt: Point to Point Topology
   :width: 30%

   Point to Point Topology

Point-to-point topology
-----------------------

With Ethernet, we do this by plugging one computer directly into another
computer. A direct connection is a bit more complex than you might
expect because Cat 5 cable expects you to connect to a central hub
rather than to another node. As discussed in Chapter 2, an Ethernet
cable has lines to transmit to the hub and lines to receive data from
the hub. If you are connecting two computers together, rather than a
computer to a hub, both computers will transmit on the same lines and no
computer will be listening. You need either a *cross-over* cable that
crosses those wires, or to have electronics built into your computer
that detect this issue and reconfigure which wires are used for transmit
and receive automatically. Thankfully, those electronics are reasonably
common.

This point-to-point protocol isn't very common with Ethernet, but it's
common with other types of networks when working with hardware, such as
connecting a sensor or display to a computer using I\ :sup:`2`\ C.

Line Topology
-------------

If we're connecting more than two nodes, we can hook them up in a chain
with *line topology* (:numref:`line`).

.. _line:
.. figure:: media/line.svg
   :alt: Line topology
   :width: 60%

   Line topology

Having the nodes in a row requires less wire than the ring or star
topologies we'll introduce soon. However, the middle nodes require two
connectors—one for the left and one for the right—and if anything
happens to one node's connection, the whole chain goes down. We don't
use this topology very often for this reason.

Bus Topology
------------

In *bus topology*, we have a row of nodes, and each node taps into a
common line (:numref:`bus`). Bus topology requires only one connector for
each node, so it's cheaper and more common than line topology. We can
also plug and unplug nodes from the bus without reconfiguring the
network.

.. _bus:
.. figure:: media/bus.svg
   :alt: Bus topology
   :width: 60%

   Bus topology

This is a simple topology that doesn't require much cable. Bus topology
used to be common with Ethernet setups in the 1990s, but it fell out of
favor partly because an issue with the wiring of any one node's
connection to the bus can take down everything. We still use the bus
topology in non-Ethernet networking, like in cars or when we embed it as
part of a circuit board. If you've ever plugged a video card into your
computer, you've plugged it into a bus.

Ring Topology
-------------

In *ring topology*, we connect the ends of nodes in a line topology
together to form a ring (:numref:`ring`).

.. _ring:
.. figure:: media/ring.svg
   :alt: Ring topology
   :width: 60%

   Ring topology

This topology is useful because if there's a break in any connection,
all computers still are connected together in a line. This type of
networking often appears in backbone networks that go across long
distances.

Star Topology
-------------

*Star topology* has a central hub, switch, or router with an individual
cable to each connected computer (:numref:`star`).

.. _star:
.. figure:: media/star.svg
   :alt: Star topology
   :width: 60%

   Star topology

But rarely are things set up so that we can place the hub in the middle
of our nodes; rather, we typically have a bundle of TP cables going down
the row, as shown in :numref:`star2`. For example, we might have a row of
office cubicles and a hub in a wiring closet at the end of the row.

.. _star2:
.. figure:: media/star2.svg
   :alt: Star topology, more realistic
   :width: 60%

   Star topology where nodes are in a row

Star topology is the most common way to cable a bunch of computers
together using Ethernet. It requires you to run more cable than bus and
line topologies, but it comes with two serious advantages that are
usually worth the extra cost: reliability and speed. When one node's
connection goes down in a star topology, the rest of the nodes don't go
down with it. You can also push higher speeds because each node has its
own dedicated cable rather than sharing with other nodes.

Fully Connected Topology
------------------------

*Fully connected topology* is where each node connects to every other
node (:numref:`full`).

.. _full:
.. figure:: media/full.svg
   :alt: Fully connected topology
   :width: 60%

   Fully connected topology

For wired networks, this is rarely practical, as just 10 nodes would
require 90 cables and 9 ports on each node to connect into. But for wireless
networks, this topology makes sense: radio waves travel out, and each
node in range can listen in and communicate.

Mesh Topology
-------------

*Mesh topology* refers to a set of distributed nodes with connections
that give the network a net-like appearance (:numref:`mesh`). If each node
repeats every message to every other node, it's considered a Layer 2
topology, because we aren't trying to route a path through the nodes
(routing occurs in Layer 3, so the mesh topology is often seen in that
layer as well, as we'll learn in Chapter 6).

.. _mesh:
.. figure:: media/mesh.svg
   :alt: Mesh topology
   :width: 60%

   Mesh topology

Mesh topology

Now let's look at how to manage multiple nodes communicating
simultaneously within the same network.

Media Access Control Methods
============================

When you're with a group of people, it's natural to take turns speaking
so you don't talk over each other. The same concept applies to networks.
When nodes share the same medium, they need to decide when each node can
transmit and when each node should listen. This process is managed by
the MAC protocol. Three main methods exist for carrying out MAC: we can
wait for a gap in the communication traffic before transmitting, use an
indicator on whose turn it is, or avoid the problem altogether.

Waiting for a Gap in the Communication with CSMA/CD

If our nodes share a transmit medium, the MAC protocol tells the
Ethernet to wait for a gap in the conversation before transmitting. The
technical term for this is *Carrier Sense Multiple Access with Collision
Detection (CSMA/CD)*. Carrier sense means that if a node wants to send
data, it first listens to make sure no other node is talking. Multiple
access means multiple nodes can transmit on the medium. Collision
detection means that if two nodes realize they're talking at the same
time, they'll stop, wait a random period of time, and then try talking
again. This is how people manage conversations, just implemented for
computers with a fancy acronym.

Using a Talking Stick with Token Ring

Some network engineers thought the CSMA/CD method of communication
(expecting connections to wait politely, not interrupt, and not talk too
much) was a recipe for pandemonium, so they created a protocol called
*Token Ring*. The Token Ring protocol is similar to passing around a
talking stick in a group discussion, where only the person holding the
stick can talk. With Token Ring, a *token* passes from node to node, and
only the node with the token can talk. In the 1980s, both Ethernet and
Token Ring competed in the market to become the standard. Ethernet ended
up being cheaper and evolved to support faster speeds than Token Ring,
so Ethernet and CSMA/CD became the de facto standard. Nowadays, we
typically carry out MAC by using CSMA/CD or avoid the problem by using
star topologies.

Avoiding the Problem with Star Topology

In a star topology, the central hub plays traffic cop. Every node talks
directly to the hub, each with one pair of balanced lines on the cable
to transmit from the node to the hub, and another pair to transmit from
the hub to the node. No one gets interrupted, and all communication
passes through the hub. While we have to run a separate wire to each
node, the benefits outweigh the cost.

Common Standards
================

Once we've figured out how to hook up the nodes in our network, we need
to come to an agreement on how to pass data back and forth. When we pass
bytes across the wire, the nodes need rules that tell them the order of
the data fields, how many bytes make up each field, and when it's okay
to transmit them.

We call those rules a *protocol*. If a lot of people use the same
protocol, we describe it as a *standard protocol*, oftentimes shortened
to *standard*. We typically use the words protocol and standard
interchangeably.

Industry-related groups, such as IEEE and ISO, have set up many
standards for transmitting data at Layer 2. The most common standards
are as follows:

Wired networks

Multiple Ethernet standards, grouped under IEEE 802.3.

Wi-Fi

Multiple Ethernet standards, grouped under IEEE 802.11.

Ethernet

Can be used for both wired and wireless networks, and is the one of the
most commonly used protocols. It arranges the bytes into the same data
frame format, regardless of the medium being used.

Vehicles

CAN-Bus, grouped under several ISO standards.

USB connections

Created by a consortium of multiple companies.

Bluetooth

Started as an IEEE standard, now maintained by a group of thousands of
companies in the Bluetooth Special Interest Group organization.

Let's survey each of these standards in terms of where they're used, how
they've evolved, and how they format their data.

Wired Network Standards
-----------------------

The most popular standards used over TP wire at the time of this writing
are Ethernet standards. As mentioned in Chapter 2, there are several
wired Ethernet standards as well as standards for wireless and
fiber-optic mediums. The wired standards are all part of the 802.3 IEEE
standards.

Most new equipment uses *802.3ab Gigabit Ethernet*, which transmits data
at a rate of 1 billion bits per second. Since there are eight bits in a
byte, this is equal to 125 megabytes per second. However, each message
contains a preamble, frame overhead, and a required gap between each
message; so in practice, it's actually around 118 megabytes per second.
Older equipment often uses *802.3u Fast Ethernet*, which is 10 times
slower at 100Mbps. Some equipment also uses *802.3ae 10 Gigabit
Ethernet*, which is very new and not as common because of its high price
point.

**NOTE** For the full list of Ethernet standards and their evolution
over time, see the Wikipedia article on IEEE 802.3:
*https://en.wikipedia.org/wiki/IEEE_802.3*.

Ethernet is very popular for both wired and fiber connections; however,
not all communications use Ethernet as a protocol. For example,
telecommunication companies have non-Ethernet standards that let them
transmit terabytes of data each second over fiber-optic cables. Although
this is beyond the scope of this book, you should know that they exist.

Wi-Fi Standards
---------------

The original Wi-Fi standard was numbered 802.11, and subsequent
standards added letters after the number, like 802.11a and 802.11b.
However, this numbering scheme proved confusing for the average user. In
2018, the Wi-Fi Alliance associated these standards with progressive
version numbers to help people more easily recognize what their router
supports and which standard is faster or better. Table 4-1 lists the
various Wi-Fi version numbers in use today.

Wi-Fi Version Numbers

+-----------------+-----------------+----------------+-----------------+
| Wi-Fi version   | IEEE version    | Date           | Max speed       |
+=================+=================+================+=================+
| Wi-Fi 1         | 802.11b         | 1999           | 11Mbps          |
+-----------------+-----------------+----------------+-----------------+
| Wi-Fi 2         | 802.11a         | 1999           | 54Mbps          |
+-----------------+-----------------+----------------+-----------------+
| Wi-Fi 3         | 802.11g         | 2003           | 54Mbps          |
+-----------------+-----------------+----------------+-----------------+
| Wi-Fi 4         | 802.11n         | 2009           | 300Mbps         |
+-----------------+-----------------+----------------+-----------------+
| Wi-Fi 5         | 802.11ac        | 2014           | 866.5 Mbps      |
+-----------------+-----------------+----------------+-----------------+
| Wi-Fi 6         | 802.11ax        | 2019           | 10 Gbps         |
+-----------------+-----------------+----------------+-----------------+

To find the standard your connection uses on Windows, navigate to the
Performance tab of the Task Manager (Figure 4-9).

|Graphical user interface Description automatically generated|

Finding the connection type on Windows

If you're on a Mac, hold down the option key and click the Wi-Fi icon in
the menu bar. From there, find the currently connected wireless router
and look for the PHY Mode item to see the connection type.

Wireless access points simplify connections by broadcasting a *service
set identifier (SSID)*, which is a normal name like *Uptown Coffee Shop*
that appears in lists of possible connections when you scan for Wi-Fi
hotspots. The owner of the access point can turn this feature off to not
broadcast, but the client computer will then need to type in the SSID
manually to get it to work.

Wi-Fi Security
^^^^^^^^^^^^^^

Originally, Wi-Fi shipped with no security by default, which made it
easy to set up, but also easy for evil-doers to eavesdrop or tap into
the network for illegal activities.

Wi-Fi needed *security protocols* to define how we'd encrypt data so
people couldn't see what was being sent or received and to keep unwanted
people off a network. One of the first security protocols was *Wired
Equivalent Privacy (WEP)*, which used a 40- or 104-bit key for
encryption and two methods for authenticating (logging in to the
network). WEP was advertised to be as secure as running through a wire.

**Warning** Spoiler: it wasn't. If WEP appears as an option in your
settings, *don't use it.*

The following is a list of current protocols:

Wi-Fi Protected Access (WPA)

Has been superseded by WPA2, so don't use this if setting up a new
network.

Wi-Fi Protected Access version 2 (WPA2)

The most common protocol and a safe choice.

Wi-Fi Protected Access version 3 (WPA3)

Introduced January 2018 and is new enough that not all older devices
support it. For now, WPA2 might be the better choice until more devices
support WPA3.

In addition to selecting which version of WPA to use, you also need to
choose how you want the devices on the network to authenticate. There
are two ways you can set up a network to require devices have permission
to connect:

1. Pre-shared key (PSK): a required *pre-shared key*, a passphrase
   needed to get into a Wi-Fi network. A PSK works best for home
   networks and small businesses.

2. Enterprise: pre-shared keys don't work well for larger organizations.
   For example, if a company has 200 people, and one person quits,
   should all 199 remaining people get a new key in order to make sure
   the departing disgruntled employee doesn't still have keys to the
   network? A good solution is the Enterprise version of a PSK, which
   requires a username and password that's managed by a central database
   for users to access the wireless. This is type of server is called a
   *RADIUS server*. If an organization has more than 10 or so people, it
   likely needs the Enterprise version.

The WPA protocols allow users to choose an encryption algorithm to use,
such as the following:

-  Temporal Key Integrity Protocol (TKIP): an older encryption protocol
   that's no longer as secure as other options.

-  Advanced Encryption Standard (AES): the encryption standard currently
   recommended to use when setting up a connection.

In summary, if you're setting up a small network, choose WPA2-PSK (AES).
It's the most commonly used protocol, has the best encryption available,
and uses a simple key you can give others to log in to the network. If
you need individual logins for a larger company, use WPA2-Enterprise
(AES) and set up a RADIUS server.

The Ethernet Frame
------------------

If you've ever wanted to know why your internet is slow, why some web
pages aren't working, or what's happening when the computer sits and
pauses to wait for the network, you need to see how the network passes
data between nodes.

Data at Layer 2 is passed in a chunk called a frame. If you pass this
data frame between two computers, those computers need a standard on how
to format that data. They need to figure out where the data is going,
where it's from, and whether it's corrupted.

Ethernet is by far the most common standard at Layer 2. Table 4-2 shows
the parts that make up an Ethernet frame.

The Parts of an Ethernet Frame

+-----+------+-----+-------+----+------+-----+-----+----+---------+
|     | Prea | Fr  | MAC   | M  | 80   | Et  | P   | F  | I       |
|     | mble | ame | d     | AC | 2.1Q | her | ayl | ra | nterpac |
|     |      | del | estin | so |  tag | net | oad | me | ket gap |
|     |      | imi | ation | ur | (o   | t   |     | c  |         |
|     |      | ter |       | ce | ptio | ype |     | he |         |
|     |      |     |       |    | nal) |     |     | ck |         |
+=====+======+=====+=======+====+======+=====+=====+====+=========+
|     | 7 b  | 1   | 6     | 6  | (4   | 2   | 4   | 4  | 12      |
|     | ytes | by  | bytes |  b | by   | by  | 6–1 | b  | bytes   |
|     |      | tes |       | yt | tes) | tes | 500 | yt |         |
|     |      |     |       | es |      |     | by  | es |         |
|     |      |     |       |    |      |     | tes |    |         |
+-----+------+-----+-------+----+------+-----+-----+----+---------+
| La  |      |     | ←     |    |      |     |     |    |         |
| yer |      |     | 64    |    |      |     |     |    |         |
| 2   |      |     | –1522 |    |      |     |     |    |         |
| Et  |      |     | bytes |    |      |     |     |    |         |
| her |      |     | →     |    |      |     |     |    |         |
| net |      |     |       |    |      |     |     |    |         |
| fr  |      |     |       |    |      |     |     |    |         |
| ame |      |     |       |    |      |     |     |    |         |
+-----+------+-----+-------+----+------+-----+-----+----+---------+
| La  | ←    |     |       |    |      |     |     |    | ← 12    |
| yer | 72–  |     |       |    |      |     |     |    | bytes → |
| 1   | 1530 |     |       |    |      |     |     |    |         |
| Et  | b    |     |       |    |      |     |     |    |         |
| her | ytes |     |       |    |      |     |     |    |         |
| net | →    |     |       |    |      |     |     |    |         |
+-----+------+-----+-------+----+------+-----+-----+----+---------+

Let's look at each part in more detail:

Preamble

An Ethernet frame first transmits a *preamble* to give the receiver a
chance to synchronize with the transmitter. The preamble is seven bytes
worth of alternating ones and zeros, or 56 (:math:``) bits. In Chapter
3's Manchester Encoding project, you needed to know how long the gap was
between each up/down transition; the preambles give the receiver time to
figure that out.

Frame Delimiter

The *frame delimiter* has two ones at the end that tell the receiver
you're about to transmit data. The seven-byte preamble along with the
one-byte delimiter look like this:

10101010 10101010 10101010 10101010 10101010 10101010 10101010 10101011

MAC Destination and Source Addresses

Because devices can share the same medium, they need a way to know
whether a frame of data is intended for them or for a different device.
Each device gets its own unique number, which acts as the device's name.

This unique number is a Layer 2 address, which the manufacturer of the
networking hardware sets by default. The Layer 2 address is a six-byte
number called a MAC address. Keep in mind, this is an entirely different
address from the IP address. Both addresses are necessary; the MAC
address gets the data to the next node, and the IP address builds on top
of that to route across multiple hops. You'll learn about IP addresses
in Chapter 6.

The six-byte *MAC destination address* of the frame's recipient—that is,
where the data is going—follows the frame delimiter. In hexadecimal, it
looks something like this:

BE 15 38 D3 0B 70

Then comes the six-byte *MAC source* *address* of the frame's sender.
Think of it as the return address.

**NOTE** The 802.1Q tag is optional and used only with virtual networks,
so we won't discuss it here.

Ethernet Type

Next are two bytes that denote the *Ethernet type*, which defines how
the rest of the packet is formatted. Most modern Ethernet packets are
Ethernet II type packets, so the next field usually has the following
bytes to identify it as such: 08 00. The next most common type is the
Address Resolution Protocol (ARP) packet used to connect Layer 2
addresses to Layer 3 addresses.

Payload

Following the Ethernet type comes the actual data we're trying to
transmit, known as the *payload*, which can range from 46 to 1,500
bytes. This payload data is often a Layer 3 packet, so we pass this
payload up to the Networking Layer.

Frame Check Sequence

After the payload, we transmit 4 bytes (32 bits) that make up our *frame
check sequence*. The frame check sequence ensures the frame doesn't have
any errors, such as missing bits, extra bits, or flipped bits. The
sender calculates the frame check sequence based on the contents of the
payload and sends it to the receiver. The receiver also calculates the
sequence and ensures that it matches the sender's sequence. The frame
check sequence is calculated using an algorithm called a cyclic
redundancy check (CRC).

Interpacket Gap

After that, no one should talk for 12 bytes worth of time to give the
receiver time to prepare to receive another packet. This gap is called
the *interpacket gap*.

Controller Area Network

Most modern cars, trucks, and even some airplanes and medical equipment
have a standard networking technology called *controller area network
bus (CAN-Bus)*. Cars use a CAN-Bus to read sensors and control
equipment, such as the engine, transmission, steering, and audio; it's
essentially the car's nervous system. To save cost and weight, the
CAN-Bus is typically implemented as a bus topology, hence the name.

CAN-Bus is popular for several reasons. It's low cost: when you're
making cars, tractors, or other equipment, every dollar counts. It's
centralized: a technician can plug into one spot and read what's
happening with every electronic control on the vehicle. It's robust: if
a part fails or the equipment you're running emits a lot of electronic
interference, CAN-Bus keeps working. It's efficient: there's not much
overhead, and you can prioritize messages. It's flexible: you can easily
add additional controls to the CAN-Bus network.

The CAN-Bus uses a high and a low wire to communicate. The signals on
the wires are exactly opposite of each other and about two volts apart,
so they can use differential signaling (see Chapter 2). Optionally, you
can add other wires to increase shielding from other signals or keep
communications going if either the high or low wire breaks.

Each node on the network (such as a sensor or a control) has its own ID
number and a small computer that interfaces with the CAN-Bus.

Some advanced cars allow you to access the CAN-Bus remotely for starting
and door unlocking from a distance. This remote access, however, may
leave users vulnerable to security issues, as Chrysler realized when it
had to recall 1.4 million Jeeps when a pair of hackers remotely hijacked
the cars' systems.

On a car, anyone can connect to this network via the standard on-board
diagnostics port called *ODB-II*, usually found on the lower dash of the
driver's side. A technician might use this to read error codes that
cause the check engine light to turn on. People trained in tuning cars
can even use this port and other tools to reprogram the engine to
increase its power.

USB
---

The *Universal Serial Bus (USB)* standard was first released in 1996
after seven companies cooperated to create a standard for connecting
devices to a computer. This was a huge event in computer technology;
before USB, users would have to manage different types of connectors and
install custom software drivers for everything that hooked up to their
computers, which was a major hassle.

USB has had three major revisions and about 10 different common plug
types (Figure 4-10). Typically, connections travel only about 10 feet
(two meters).

|image4|

“Comparison of USB connector plugs” by Milos and “USB Type-C” by Pietz
retrieved from Wikipedia and licensed under CC BY 3.0

USB can deliver power at 5 volts. A high-current power supply can
deliver up to 2.4 amps of power at 5V for most USB plug types. The most
recent USB-C plugs can deliver 5 amps of power at 5V, or 3 amps at 20V
(60 watts) if backed by an appropriate power supply.

The top connection speed for USB 3.2 is 20Gbps. USB 3 with a USB Type-C
connector can transmit video, making it a great all-in-one connection.

Table 4-3 shows how the USB standard has evolved over time to support
faster connection speeds.

Evolution of the USB Standard

+----------------+----------------+-----------------+-----------------+
| Year Invented  | USB Standard   | Connection      | Common          |
|                |                | Speed           | Connectors      |
+================+================+=================+=================+
| 1996           | USB 1.0        | 1.5Mbit/s and   | USB A and B     |
|                |                | 12Mbit/s        | connectors      |
+----------------+----------------+-----------------+-----------------+
| 1998           | USB 1.1        | 1.5Mbit/s and   |                 |
|                |                | 12Mbit/s        |                 |
+----------------+----------------+-----------------+-----------------+
| 2000           | USB 2.0        | 480Mbit/s       | USB Mini-A and  |
|                |                |                 | Mini-B          |
|                |                |                 | connectors      |
+----------------+----------------+-----------------+-----------------+
| 2008           | USB 3.0        | 5Gbit/s         | USB Type-C      |
|                |                |                 | connector       |
+----------------+----------------+-----------------+-----------------+
| 2013           | USB 3.1        | 10Gbit/s        |                 |
+----------------+----------------+-----------------+-----------------+
| 2017           | USB 3.2        | 20Gbit/s        |                 |
+----------------+----------------+-----------------+-----------------+
| 2019           | USB 4.0        | 40Gbit/s        | USB Type-C      |
|                |                |                 | connector       |
+----------------+----------------+-----------------+-----------------+

You can easily create your own USB device with small Arduino-compatible
boards that emulate a keyboard, mouse, or joystick.

Bluetooth
---------

Bluetooth is a popular wireless standard intended for *Personal Area
Networks (PAN)*—that is, networks intended to span only a few feet, such
as your desktop or personal space. Each Bluetooth device has a class
that describes the transmission power and range of the device, as shown
in Table 4-4.

Bluetooth Classes

+-------------+------------------------+------------------------------+
| Class       | Power (mW)             | Typ. Range (m)               |
+=============+========================+==============================+
| 1           | 100                    | ~100                         |
+-------------+------------------------+------------------------------+
| 2           | 2.5                    | ~10                          |
+-------------+------------------------+------------------------------+
| 3           | 1                      | ~1                           |
+-------------+------------------------+------------------------------+
| 4           | 0.5                    | ~0.5                         |
+-------------+------------------------+------------------------------+

The Bluetooth version is different from the Bluetooth class. Instead of
specifying the power output, the *Bluetooth version* defines the current
version of the standards that all equipment must follow. Bluetooth 4.0,
introduced in 2010, added the *Bluetooth Low Energy (BLE)* substandard
that allowed very low power connections that could be powered by
button-cell batteries used in watches and other small devices. This has
been continued in subsequent versions, with Bluetooth 5 introduced in
2016.

Like Ethernet, Bluetooth has a frame format. Bluetooth packets have
three main sections, as listed in Table 4-5.

Bluetooth Frame Format

+-----------------------------------+----------------------------------+
| Section                           | Bit Size                         |
+===================================+==================================+
| Access Code                       | 72 bits                          |
+-----------------------------------+----------------------------------+
| Header                            | 54 bits                          |
+-----------------------------------+----------------------------------+
| Payload                           | 0–2,745 bits                     |
+-----------------------------------+----------------------------------+

The first section is an *access code*, which has a preamble similar to
Ethernet's and a method of identifying the Bluetooth connection. The
next section is the *header*, which has a node address, the type of
packet (audio, data, and so on), sequence number, and error check. The
last section is the payload.

I\ :sup:`2`\ C
--------------

Bluetooth, Ethernet, and CAN-Bus are great protocols for linking
electronics together, but those protocols require separate chips and
electronics. What if you need something even simpler and cheaper, maybe
to connect a temperature and humidity sensor to a computer and run logic
to control its fans? When you don't need all the features offered by the
other protocols, the *Inter-Integrated Circuit (I\ 2\ C)* protocol is a
great option.

I\ :sup:`2`\ C is a two-wire interface designed to hook together sensors
and displays to microcontrollers. It's popular in creating integrated
circuits, and it's easy enough for amateur makers to use.

You can send I\ :sup:`2`\ C signals with Raspberry Pi computers and even
smaller computers like the Arduino (about the size of a wallet), the
Adafruit Feather (the size of a stick of gum), or the Adafruit Trinket
(postage-stamp sized).

You can read or control many items with I\ :sup:`2`\ C, including
sensors for temperature, pressure, altitude; accelerometers; GPS;
LCD/OLED/LED displays; accurate time/clock modules; digital-to-analog
and analog-to-digital converters; servo and motor drivers; audio
amplifiers; and keypads and switches.

I\ :sup:`2`\ C uses both a *serial clock line (SCL)* and a *serial data
line (SDA)*, similar to the method described in Chapter 2. The SCL
regularly goes between low and high. When the SCL is low, the SDA
transitions to high or low depending on what data bit we have. When the
SCL goes high, the SDA is ready for us to read. Although I\ :sup:`2`\ C
takes two wires, one for SCL and one for SDA, typically the components
require two more wires for power.

I\ :sup:`2`\ C devices are hooked together in a bus topology. Each
device has a seven-bit address, numbered 0-127. The devices typically
default to a particular address that can be changed.

Communication typically happens at 100,000 bits per second.

It's important to make sure that the voltage of all the I\ :sup:`2`\ C
items hooked together match. Both 5V and 3.3V levels are common. If you
need to use both, I\ :sup:`2`\ C level converters can convert between
the voltages.

What You Learned
================

The data-link layer allows us to connect two or more nodes together. We
can wire them in configurations like the bus or star topologies, or
fully connect them if they're using wireless. Once connected, we can use
data-link protocols like Ethernet, Bluetooth, USB, CAN-Bus, and
I\ :sup:`2`\ C to define who can talk, how fast to send data, and the
order and format of sent data.

In the next chapter, you'll work on several projects to try out some of
these protocols. You'll send and receive Ethernet frames, “sniff” data
sent from other applications, and see how fast you can send data. You'll
also read from a car's CAN-Bus, work with Bluetooth, and try
I\ :sup:`2`\ C.

