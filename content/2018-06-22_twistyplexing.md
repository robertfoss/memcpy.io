Title: Twistyplexing: A Charlieplexing variety
Date: 2018-06-22 12:26
Category: leds
Tags: twistyplexing, charlieplexing, multiplexing, led, leds
Description: Twistyplexing is a neat variety of Charlieplexing, with 2 small benefits.

[![Alt text](/images/2018-06-22_twistyplexing.png "A 42 LED, N == 7 Twistyplexing layout")
](/images/2018-06-22_twistyplexing.png)

The above layout has N = 7, yielding 42 LEDs.

Apart from the symmetry being visually pleasing compared to the normal
row & column Charlieplexing layouts, it's relatively easy to spot errors
in the schematic.

## Avoiding lookup tables

The major advantage of twistyplexing is the ability to avoid lookup tables
and replace them with some relatively straight forward arithmetic.

    row = led_number / (N - 1)
    column = led_number % (N - 1)
    anode = (row + column + 1) % N

Of course the cathode still has to be controlled, but its pin id already
defined by the **row** variable above.

## Thanks
The Twistyplexing concept was created by Tom Yu, and defined in [this](https://argonblue.wordpress.com/2012/06/30/twistyplexing-a-new-topology-for-led-multiplexing/) blog post.
