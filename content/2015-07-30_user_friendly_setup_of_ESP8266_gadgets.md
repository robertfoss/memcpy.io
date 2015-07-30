Title: User friendly setup of ESP8266 gadgets
Date: 2015-07-30 15:10
Category: ESP8266
Tags: NodeMCU, ESP8266, Setup

![Alt text](https://raw.githubusercontent.com/robertfoss/esp8266_nodemcu_wifi_setup/images/screenshot.png "Screenshot")

[esp8266_nodemcu_wifi_setup](https://github.com/robertfoss/esp8266_nodemcu_wifi_setup) is designed to provide a simple interface for users to configure their ESP8266/NodeMCU based devices through.

 * Start ESP.
 * Connect to the "SetupGadget" WiFi through your internet enabled thing of choice.
 * Submit credentials of your local WiFi.
 * The ESP reboots and connects to your local WiFi.

## What is this magic! How could a bare mortal like me summon features like this?!
Let me tell you..

By default DNS is not announced in the DHCP offer message, because a DNS server does not ship with NodeMCU.
In order to announce that the ESP8266 is running a DNS server, NodeMCU has to be recompiled to support that.
A guide to building NodeMCU can be found [here](http://memset.io/building-nodemcu-for-the-esp8266.html).

Thanks to the wonderful work of Andy Reischles on [Captive Portal](https://github.com/reischle/CaptiveIntraweb/tree/dev), a lua implementation of a domain hijacking DNS server exists. Which will allow an ESP8266 to redirect all traffic to itself.

#### Detailed guide

 * In dhcpserver.h, #define USE_DNS 1
 * Build NodeMCU.
 * Flash NodeMCU.
 * Upload all .lua files **and** index.html.
 * Reboot ESP.

#### What you need to do

After a user has connected throught the portal and sucessfully configured the the ESP8266 with the credentials of the local WiFi, something lua service should be started so that the ESP8266 actually does something.

I would suggest adding something like this to init.lua:

    dofile("init_connected.lua")

Where init_connected.lua is where your script resides.
