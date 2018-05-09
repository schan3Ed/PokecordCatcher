# PokecordCatcher

### Updated! Works as of 10/04/2018, Name removal from URL workaround.
Selfbot to catch pokemon when they spawn for the Pokecord discord bot

## Getting Started

One of the easier ways to install is to use a direct release, you can download the latest release from [here](https://github.com/xKynn/PokecordCatcher/releases/latest) and you can move to the "Installing" part of the guide.  
For others, you can clone or download the project from the green button up top and extract the archive.

### Prerequisites

Python 3.6 or newer; you can easily install python by visiting: https://www.python.org/downloads/ . Make sure to tick add python to PATH.

### Installing

You will require the token of the account you want to run this bot on, it's better if it's an alt as selfbots violate ToS and you can get banned.  
To grab your token visit [Token Tutorial](https://github.com/TheRacingLion/Discord-SelfBot/wiki/Discord-Token-Tutorial).  
Skip the next part if you're using a packaged release.  
After you've setup python and grabbed your token, run setup.bat.

### Config

Open config.json up with any text editor, now put your token in the "".  
Other options in config are:
 - priority: In this list you can add pokemon that bypass the catch rate, pokemon that you absolutely want to catch.
 - catch_rate: This is a percent out of 100.
 - delay: A delay in seconds to try and catch a pokemon after PokeCord spawns one.
 - delay_on_priority: This can be set to `true` or `false`. True means delay will still apply on priority pokemon, false means an instant catch.
 - priority_only: Setting this to `true` means only priority pokemon will be caught.
 - avoid_list: A list just like priority, add names of pokemon you want the bot to ignore.
 - whitelist_channels: A list of channel IDs, so the bot will only catch pokemon on these channels.
 - blacklist_channels: A list of channel IDs, so the bot will catch in all channels except these.
 - verbose: Setting this to true will add a bit more info to the console when a pokemon spawns, i.e if pokemon was skipped and where the bot tried to catch a pokemon (server and channel name).
 - NOTE: Only one of whitelist or blacklist can have channel IDs at a time, the other needs to be empty
 - TIP: There are two ways to find a channel's ID, either go to the channel, tag the channel with a #, then add a \\ to it, ex: `\#general`, it will present a number in <>, that number is a channel ID you can use.
      - The second way is to go to discord settings > Appearance > Scroll down and enable Developer Mode, then you can right click on a channel in the left side channel bar and click Copy ID.

Example config:
```
{
  "token": "<your token>",
  "priority": ["Groudon", "Geodude"],
  "catch_rate": 90,
  "delay": 2,
  "delay_on_priority": true,
  "priority_only": false,
  "avoid_list": ["Rattata", "Poochyena"],
  "whitelist_channels": [369081842038603776, 369081842038603779],
  "blacklist_channels": [],
  "verbose": false
  "findPokemon": false,
  "findPokemon_channel": <your channel>,
  "findPokemon_delay": 2
}
```

You can use this as a reference to modify your config.json.

### Running the bot
Either run run.bat or `py -3 launcher.py` or use `launcher.exe` if you're using a release.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/xKynn/PokecordCatcher/blob/master/LICENSE) file for details

## Bug reports and problems

Please open an issue on this repo, you can do this from the issues tab on the top and I'll take a look at it when I can.