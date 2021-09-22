
## GeoShot - Geotag Your Screenshots!


MSFS GeoShot is the first and only all-in-one **screenshot tool** that's specifically crafted for Microsoft Flight Simulator. It allows you to take intelligent screenshots that store helpful information about your flight in their **metadata**, which then allows you to import them into other tools to achieve all kinds of fun integrations, e.g.:

- Viewing a **map of your screenshots** using [Google My Maps](https://www.google.com/intl/en_us/maps/about/mymaps/) or [GeoSetter](https://geosetter.de/en/main-en/)
- **Searching** for screenshots in Explorer by their location or even the **type of aircraft** used!

Additionally, MSFS GeoShot will **name your screenshots** by date, time, and human-readable location (e.g. country, area, city), making it super simple for you to browse through your screenshots and keep them organized.

### Getting Started

1. Download and **unzip** the attached zip file
2. Run the simple **installer .exe** contained within
3. Launch MSFS GeoShot by clicking on its **desktop shortcut** or **start menu** entry

With the flight simulator running, simply press **Ctrl+Shift+S** to take a screenshot, or use the corresponding button in MSFS GeoShot. 

The hotkey, just like almost everything about the tool, can be **customized** using a number of easy-to-use options.

### Making More of Your Screenshots

To get the most out of MSFS GeoShot, make sure to couple it with other apps and services that support the metadata within!

#### Windows Explorer

To view your screenshot metadata, simply [enable the details pane](https://www.youtube.com/watch?v=66m32OE2Smw), or change to a column view and customize the columns shown to include image metadata. The metadata also automatically enriches Explorer's search feature, allowing you to e.g. find screenshots taken in a particular aircraft type.

#### Google My Maps

One of the most fun ways to utilize the screenshots taken by MSFS GeoShot is to display them on a map. The easiest way to do so is using the [My Maps](https://www.google.com/intl/en_us/maps/about/mymaps/) Service by Google Maps. To get you started on that please see [this offical tutorial by Google](https://www.youtube.com/watch?v=DrTLEI5hjME).

If you're so inclined, you can even go one step further, record your flight path with [Little Navmap](https://albar965.github.io/), and then export it to GPX in order to [import it](https://support.google.com/mymaps/answer/3024836?hl=en&co=GENIE.Platform%3DDesktop) as a layer into your custom map.

#### GeoSetter

As an alternative to Google My Maps, you might also want to check out [GeoSetter](https://geosetter.de/en/main-en/). This will allow you to view your screenshots on a map without having to upload them to Google first.

Important tip: By default GeoSetter will try to show Google Maps as the map layer, but due to limitations on Google's side, that does not seem to work particularly well at the moment. So my recommendation would be to immediately swap out the layer for OpenStreetMap at the top of the map widget. That way you will also see the same map as in LittleNavmap.

#### Other Tools

The apps and services listed above are just a few of the many ways to integrate MSFS GeoShot with other tools. If you find other fun integrations, please do let me know in the comments!

### Credits and License

MSFS GeoShot is Copyright (C) 2021 [pyviator](https://github.com/pyviator).

The source code for MSFS GeoShot is available on
<a href="https://github.com/pyviator/msfs-geoshot">GitHub</a>.
Contributions are welcome!</p>

*Regarding MSFS GeoShot's code:*

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

*Regarding non-code-files*:

MSFS GeoShot also includes a number of media assets which are licensed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode). For more information on the exact licensing terms and credits of original works, please see the [media resources README](msfs_geoshot/_resources/README.md).

Additionally, compiled builds of MSFS GeoShot include [Python-SimConnect](https://github.com/odwdinc/Python-SimConnect/) which ships with a bundled version of the SimConnect.dll from Microsoft Flight Simulator's SDK. Microsoft Flight Simulator is © Microsoft Corporation. Any assets from Microsoft Flight Simulator used by MSFS GeoShot (SimConnect.dll) are used under Microsoft's "Game Content Usage Rules". This project is not in any way endorsed by or affiliated with Microsoft.

*Special shout-outs*

MSFS GeoShot is built on the shoulders of giants, with a special shout-out due for the following members of the MSFS community:

*   [odwdinc](https://github.com/odwdinc) for their work on [Python-SimConnect](https://github.com/odwdinc/Python-SimConnect)
*   [Luuk3333](https://github.com/Luuk3333/msfs-screenshot-gps-data) for inspiring this project with [msfs-screenshot-gps-data](https://github.com/Luuk3333/msfs-screenshot-gps-data)

MSFS GeoShot would also not exist without a number of other third-party software in the greater open-source ecosystem. A full overview of all the  dependencies bundled with the program and overview of their copyright statements and licenses may be found in MSFS GeoShot's in-program credits.
