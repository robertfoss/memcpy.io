Title: APA102 LED Current Usage
Date: 2018-02-20 22:26
Category: apa102
Tags: apa102, 2020, led, power, usage, current, quiescent
Description: During a recent project I've been surprised to learn about idle current usage of the APA102 LEDs.

[![Alt text](/images/2018-02-20_apa102_2020_quiescent_current.png "APA102 LED Quiescent Current Diagram")
](/images/2018-02-20_apa102_2020_quiescent_current.png)

What we're seeing here is a the LED being fully off (albeit with floating clock and data inputs), drawing somewhere between 0.7-1 mA.

I was quite surprised to see such a high quiescent current.

For the APA102 2020 which has a 20x20mm footprint this is somewhat disappointing, not because it is worse than the normal 50x50 APA102 variants, but rather because the small footprint begs for the IC to be used in wearables and other power consumption sensitive applications.


## Setup
So this is the very simple setup I was using. It's nothing fancy; a multimeter
set to the mA range, connected between the power supply and the APA102 breakout board I happened to have laying around.

[![Alt text](/images/2018-02-20_setup.jpg "APA102 LED Quiescent Current Diagram")
](/images/2018-02-20_setup.jpg)
