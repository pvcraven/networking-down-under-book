Introduction
************

There are a lot of "standards" when it comes to networking. We need
those standards to communicate. One organization that makes some of
those standards is the International Organization for Standardization
(ISO, and yes, the acronym doesn't line up with the name). ISO created a
standard called the Open Systems Interconnection model (OSI model).

ISO created OSI. The acronyms are just reversed.

OSI Model
=========

OSI divides up the concept of networking into seven layers:

* Physical
* Data-Link
* Networking
* Transport
* Session
* Presentation
* Application

This book is organized around these layers. We are going to start at the
Physical layer and work our way up to the Presentation Layer. As for the
Application layer? We could write another whole other book on that.

OSI is a conceptual model. There isn't a specific "implementation" of
any layer in this model. What the OSI model helps with is talking to
other people about networking. It also helps when you want to break
apart a complex networking problem into smaller logical parts. You know
when you talk about the "east-side" of your town? Exactly what fits into
that definition is a little fuzzy and can change a bit over time, but
the term gives most people an idea of what part of town you are talking
about. It works the same way with OSI layers.

It is worth remembering the name of each layer and their order. The
physical layer is considered "layer 1." If you talk to a networking
expert and mention that some process happens at the "networking layer",
or "layer 3" they will know what you are talking about. It is such a
popular way to talk about networking that there are even companies named
after "layer 3."

If you have trouble remembering the layer names, use the mnemonic
"Please Do Not Touch Steve's Pet Alligator." Take the first letter from
each word of that sentence, and you have the first letter of each layer.

What does each layer do?
------------------------
At the application layer, the user interacts with our application. For
example, we can give a thumbs-up to a video we like. Our application
needs to send that data to the website's server. Each OSI layer below
the application layer works to process that "thumbs-up", passing it down
until our request is finally turned into a signal on a wire, as shown in
:numref:`osi_1` and :numref:`osi_2`.

When the computer that receives the signal, when it is picked up at the
physical layer, we pass it up all the layers until we finally hit the
application layer where we store that information in a database.

.. _osi_1:
.. figure:: media/osi_1.svg
   :alt: The seven OSI Layers
   :width: 60%

   The seven OSI Layers

Incoming Data
-------------

In detail, what might it look like when we *receive* a web page?

Physical: Translates pulses of electricity, radio waves, or light into
binary 1's and 0's. The physical layer then takes that binary data and
passes it up to the data-link layer.

Data-Link: Decodes the binary data from the physical layer into chunks
of data called "frames." A frame has a data "payload" and if the frame
is addressed for this computer and uncorrupted, it is passed up to the
networking layer. Otherwise it is ignored.

Networking: Each chunk of data at this level is called a "packet." At
the networking level, we look to see if this the final destination for
the packet. If it is, pass it up a level. If not, figure out the next
"hop" to pass the packet to. Pass the packet back down to the data-link
level to go to that hop. The networking layer routes packets.

Transport: Takes the data contained in the packets, and reassembles them
into the original file, image, or larger data stream. If we are missing
data, we'll ask for it again. We will also pass it to the correct
program on the computer that is expecting the data.

Session: At this level we track a whole "conversation." So if multiple
files are being sent, we'll know to send them to the right program.
We'll also decrypt and uncompress any zipped up data at this level.

Presentation: This is where we display information. In our example we
combine images, web HTML files, and CSS style documents together to
render a web page.

Application: At this level, we interact with the user and wait for a
"thumbs up" or "thumbs down" on our post.

Outgoing Data
-------------

What if the user clicks a "thumbs-up" on the video? The layers might
work like this:

Application: Realize the user pressed a mouse button on the document.
Pass that down to the presentation layer.

Presentation: Receive that the user pressed the "thumbs up" icon. Turn
that into a small file that holds info on which thumbs-up was clicked.

Session: Add information about who the user was. Encrypt the message.
Compress it.

Transport: Take the file and break it into smaller packet-sized parts.

Networking: Add an address with our final destination. We probably
aren't going to get there in one hop, this layer routes to the
destination computer.

Data-link: Add an address for our next hop. This layer only worries
about point-to-point communication.

Physical: Turn the data into electrical pulses on a wire.

.. _osi_2:
.. figure:: media/osi_2.svg
   :alt: The seven OSI Layers

   The seven OSI Layers

OSI Model vs. Reality
---------------------

That's the *theory* behind the OSI model. But reality? The technologies
we use don't always fit neatly into those layers. Here are some of the
more common technologies and approximately where they fit into the
model.

You may have heard of *Ethernet*. Ethernet is a set of protocols for
networking we use when we network with cables or wirelessly. It covers
both the physical layer (layer 1) and the data-link layer (layer 2).

You may have heard of *TCP/IP*. It is the one of the main protocols that
gets Internet traffic to its destination. TCP/IP stands for Transmission
Control Protocol/Internet Protocol. IP covers the networking layer
(layer 3), TCP covers the transport layer (layer 4). TCP/IP (layers 3
and 4) can run on top of Ethernet (layers 1 and 2), but it doesn't have
to.

Have you seen those letters, "http" as part of an address for a web
page? They stand for *HyperText Transport Protocol*. That protocol
covers parts of transport and session layers (layers 4 and 5). HTTP can
run on top of TCP/IP that runs on top of Ethernet.

The display of web pages, PDFs, images, even 3D graphics fall under
presentation (layer 6), while the management of menus, buttons and other
are covered by the application (layer 7).

Just remember, many of the boundaries between these layers are fuzzy and
not clearly defined. Often technologies do tasks outside of what their
"layer", and software may lump multiple layers together.

