<div align="center">

![Icon](assets/icon.jpg)

# sphaira - enhanced hbmenu

</div>

**sphaira** is hbmenu alternative. It currently has feature parity with hbmenu `that is, launches homebrew + nxlink` whilst adding quite a few features.


### HomeBrew​
The main menu tab, it lists all the.nro found in `/switch/`. From there, you can `launch, sort, delete, create` a forwarder etc.
You can navigate to the other menu tabs using **`L`** and **`R`**, explained below.

### FileBrowser​
By pressing **`L`** from the main menu, you can access the file browser. You can `Cut, Copy, Delete, Rename` etc.
You can select multiple files / folders by using the **`ZR`** button and then se the above functions of that group of files.

Forwaders can be created if the selected file has a file assoc, see below for more details.

### hbstore​
sphaira features an appstore, using the api from [hb-app.store/switch](https://hb-app.store/switch). It can be navigated to by pressing **`R`** from the main menu.
The appstore is feature parity with hb-appstore app, as well as installing the manifests in the same folder as hb-appstore, in order to not break compatibility between the two.

### Themes​
sphaira comes with 3 themes, abyss (default), black and white (unfinished).
custom themes can be added to `/config/sphaira/themes/`, here is the `Abyss_theme` for example:

```ini
[meta]
name=Abyss
author=TotalJustice
version=1.0.0
; unused currently
preview=romfs:/theme/preview.jpg

[theme]
background=0x0f111aff
grid=0x0f115c30
selected=0x0f115cff
selected_overlay=0x529cffff
text=0xffbc41ff
text_selected=0x529cffff

icon_audio=romfs:/theme/icon_audio.png
icon_video=romfs:/theme/icon_video.png
icon_image=romfs:/theme/icon_image.png
icon_file=romfs:/theme/icon_file.png
icon_folder=romfs:/theme/icon_folder.png
icon_zip=romfs:/theme/icon_zip.png
icon_nro=romfs:/theme/icon_nro.png
```

Music can be added to a theme, as long as the music is converted to bfstm format. simply add an entry like so: `music=/config/sphaira/themes/music/bgmusic_pcm.bfstm`

### Forwaders​
sphaira can create and install forwarders for any.nro. It will use the icon of the .nro and the name + author.

It can also install forwarders for files that have a file assoc. For example, if mgba is installed and a game is located in `/roms/gba/game.gba`, then the ***Install Forwarder*** option will appear. In this case, it will try to scrape the icon of the game, otherwise it will use the icon of the .nro and the name will be a combination of the.nro name and game name.

### File Assoc​
file assoc is a way to associate file extensions (.gba,.nro etc) with a homebrew app. For example, clicking on rom.gbc that has an file assoc will bring up a list of all the applications that can handle it.
This can be used for emulators, media players, text editors etc...

Custom file assoc should go in the folder `/config/sphaira/assoc/`.

The format is very simple, here is an example of `vgedit.ini`

```ini
[config]
supported_extensions=txt|json|cfg|ini|md|log
```

And again for `mgba.ini`

```ini
[config]
supported_extensions=gba|gbc|sgb|gb
database=Nintendo - Game Boy|Nintendo - Game Boy Color|Nintendo - Game Boy Advance
```

`path`: (optional) fullpath to the.nro. if not specified, it uses the name of the ini, ie, mgba.ini will use mgb.nro.

`supported_extensions`: list of extensions the application supports, separated by |. plea

`database`: (optional) name of the rom database to use defined by the left-side of this table:

<https://gist.github.com/ITotalJustice/d5e82ba601ca13b638af9b00e33a4a86>

```cpp
using PathPair = std::pair<std::string_view, std::string_view>;
constexpr PathPair PATHS[]{
    PathPair{"3do", "The 3DO Company - 3DO"},
    PathPair{"atari800", "Atari - 8-bit"},
    PathPair{"atari2600", "Atari - 2600"},
    PathPair{"atari5200", "Atari - 5200"},
    PathPair{"atari7800", "Atari - 7800"},
    PathPair{"atarilynx", "Atari - Lynx"},
    PathPair{"atarijaguar", "Atari - Jaguar"},
    PathPair{"atarijaguarcd", ""},
    PathPair{"n3ds", "Nintendo - Nintendo 3DS"},
    PathPair{"n64", "Nintendo - Nintendo 64"},
    PathPair{"nds", "Nintendo - Nintendo DS"},
    PathPair{"fds", "Nintendo - Famicom Disk System"},
    PathPair{"nes", "Nintendo - Nintendo Entertainment System"},
    PathPair{"pokemini", "Nintendo - Pokemon Mini"},
    PathPair{"gb", "Nintendo - Game Boy"},
    PathPair{"gba", "Nintendo - Game Boy Advance"},
    PathPair{"gbc", "Nintendo - Game Boy Color"},
    PathPair{"virtualboy", "Nintendo - Virtual Boy"},
    PathPair{"gameandwatch", ""},
    PathPair{"sega32x", "Sega - 32X"},
    PathPair{"segacd", "Sega - Mega CD - Sega CD"},
    PathPair{"dreamcast", "Sega - Dreamcast"},
    PathPair{"gamegear", "Sega - Game Gear"},
    PathPair{"genesis", "Sega - Mega Drive - Genesis"},
    PathPair{"mastersystem", "Sega - Master System - Mark III"},
    PathPair{"megadrive", "Sega - Mega Drive - Genesis"},
    PathPair{"saturn", "Sega - Saturn"},
    PathPair{"sg-1000", "Sega - SG-1000"},
    PathPair{"psx", "Sony - PlayStation"},
    PathPair{"psp", "Sony - PlayStation Portable"},
    PathPair{"snes", "Nintendo - Super Nintendo Entertainment System"},
    PathPair{"pico8", "Sega - PICO"},
    PathPair{"wonderswan", "Bandai - WonderSwan"},
    PathPair{"wonderswancolor", "Bandai - WonderSwan Color"},
};
```

All of the retroarch cores has file assoc built into sphaira, so if you download retroarch using the appstore, and then navigate to `/roms/gbc/game.gbc`, gambatte and mgba will be available to be selected.

Games can be kept in .zip format, sphaira will peek into the .zip and find the real extension and use that for displaying icons / file assoc.

### Roms​
Roms should be placed in `/roms/system_name/` where system name is defined by this table right-side entries <https://gist.github.com/ITotalJustice/d5e82ba601ca13b638af9b00e33a4a86>.

this is the same layout emulation station uses. the reason for forcing roms to be in specific folders is due to many roms for different systems using the same file extension, ie, .bin / .cue or .chd.

roms placed in subfolders are allowed, for example "/roms/psx/scooby-doo/scooby-doo.bin" is valid.

### Themezer​
Themes can be browsed and download by going **`Menu Options -> Misc -> Themezer`**. 
Themes will be downloaded to **`/themes/sphaira/Theme Name - By Author/`**

To install themes, launch **NXThemes Installer** and browse to the selected folder listed above.

### Irs​
InfaRed Sensor. its a toy app i made 4(?) years ago where it shows the output of the joycon irs, use it to take a selfie :)

### Web​
Launches the builtin web browser, it's not very good.

### Nxlink​
For homebrew developers, nxlink is built into sphaira. You do not have to press any special buttons, just do `nxlink .nro` and send your nro like normal, console logging works to be using `nxlink -s .nro`
By default, this is enabled in the background, to disable it: `Menu Options -> Network -> Nxlink`.

That's most of the features spahira has. If you enjoy it so much that you'd rather it be launched over regular hbmenu, you can enable the option in `Menu Options -> Replace hbmenu on exit` where it will do just that. It will create a backup of hbmenu in `/switch/hbmen.nro` should you wish to swap back.

### **[sphaira Releases](https://github.com/ITotalJustice/sphaira/releases)**

### **[Bleeding-edge Releases](https://github.com/ITotalJustice/sphaira/actions)**

### **[Source Code](https://github.com/ITotalJustice/sphaira)**

## showcase

|                          |                          |
:-------------------------:|:-------------------------:
![Img](assets/screenshots/2024121522512100-879193CD6A8B96CD00931A628B1187CB.jpg) | ![Img](assets/screenshots/2024121522514300-879193CD6A8B96CD00931A628B1187CB.jpg)
![Img](assets/screenshots/2024121522513300-879193CD6A8B96CD00931A628B1187CB.jpg) | ![Img](assets/screenshots/2024121523084100-879193CD6A8B96CD00931A628B1187CB.jpg)
![Img](assets/screenshots/2024121522505300-879193CD6A8B96CD00931A628B1187CB.jpg) | ![Img](assets/screenshots/2024121522502300-879193CD6A8B96CD00931A628B1187CB.jpg)
![Img](assets/screenshots/2024121523033200-879193CD6A8B96CD00931A628B1187CB.jpg) | ![Img](assets/screenshots/2024121523070300-879193CD6A8B96CD00931A628B1187CB.jpg)

## bug reports

for any bug reports, please use the issues tab and explain in as much detail as possible!

**Please include:**

- CFW type (i assume Atmosphere, but someone out there is still using Rajnx)
- CFW version
- FW version
- The bug itself and how to reproduce it

### FTP server

FTP Server can be enabled via the network menu. It uses the same config as ftpsrv `/config/ftpsrv/config.ini`. 

`config.ini.template`

```ini
##########
# ftpsrv #
##########

#######################################################################
# Rename config.ini.template to config.ini for changes to take effect.#
#######################################################################

[Login]
# disabled by default, do not enable if using ldn_mitm as
# it's a security risk - you have been warned!
anon = 0

# if anon is disabled, then user and pass must be set.
user = ""
pass = ""

[Network]
# port 21 is the default port for an ftp server, some platforms may not
# support using privileged ports, change if needed.
port = 21

# timeout in seconds until a session is closed.
# if 0, then no timeout is set.
# it is recommended to set this to an actual value, eg 20.
timeout = 0

[Misc]
# use local time zone over gm (UTC) time zone.
use_localtime = 0

[Log]
# enables log output to /config/ftpsrv/log.txt
log = 0

# options specific to Nintendo Switch
[Nx]
# enables showing all available mount points at root "/"
# for example, SdCard is as at "/sdmc:"
mount_devices = 0

# allows save data to be writable, needs mount_devices = 1
save_writable = 0

# allows for bis partitions to be mounted, needs mount_devices = 1
# WARNING: modifying bis files can soft brick your switch!
mount_bis = 0

# enables led on the controller to light flash
led = 0

# options specific to Nintendo Switch App
[Nx-App]
; anon = 0
; user = ""
; pass = ""
; port = 21
; timeout = 0
; use_localtime = 0
; log = 0
; mount_devices = 0
; save_writable = 0
; mount_bis = 0
; led = 0

# options specific to Nintendo Switch Sysmodule
[Nx-Sys]
; anon = 0
; user = ""
; pass = ""
; port = 21
; timeout = 0
; use_localtime = 0
; log = 0
; mount_devices = 0
; save_writable = 0
; mount_bis = 0
; led = 0
```## mtp

mtp can be enabled via the network menu.

## file assoc

sphaira has file assoc support. lets say your app supports loading .png files, then you could write an assoc file, then when using the file browser, clicking on a .png file will launch your app along with the .png file as argv[1]. This was primarly added for rom loading support for emulators / frontends such as retroarch, melonds, mgba etc.

```ini
[config]
path=/switch/your_ap.nro
supported_extensions=jpg|png|mp4|mp3
```

the `path` field is optional. if left out, it will use the name of the ini to find the nro. For example, if the ini is called mgba.ini, it will try to find the nro in /switch/mgb.nro and /switch/mgba/mgb.nro.

see `assets/romfs/assoc/` for more examples of file assoc entries

---

I've added a github api downloader as a way to fetch apps that aren't on the appstore. the api is very simple, you just need to provide a name and a github url:

```json
{
    "name": "SwitchWave",
    "url": "https://github.com/averne/SwitchWave"
}
```

This will fetch all the downloads for the latest release.

You can also specify the name of the assets to display for download, this is useful if the app has multiple builds available for different platforms.

```json
{
    "name": "ftpsrv",
    "url": "https://github.com/ITotalJustice/ftpsrv",
    "assets": [
        {
            "name": "switch_application.zip"
        },
        {
            "name": "switch_sysmod.zip"
        }
    ]
}
```

You can also specify the output path. some apps don't push releases as a .zip, so it's its required to specify the output path:

```JSON
{
    "name": "dbi",
    "url": "https://github.com/rashevskyv/dbi",
    "assets": [
        {
            "name": "DB.nro",
            "path": "/switch/DBI/DB.nro"
        },
        {
            "name": "dbi.config",
            "path": "/switch/DBI/dbi.config"
        }
    ]
}
```

Finally, you can specify an output path for a zip. this will prepend the path of all files within the zip.

JSON entries are to be placed in **`/config/sphaira/github/`**. It will come bundled with a few entries for apps i have made, but won't include entries for apps that are piracy related.

No release for this yet, as there's a few more features i want to work on first, but you can try build in the github actions.

---

![Img](https://gbatemp.net/attachments/2024122618230800-ca43ec7375ab1e2bc8afc050c0941918-jpg.477698)

---

![Img](https://gbatemp.net/attachments/2024122618231200-ca43ec7375ab1e2bc8afc050c0941918-jpg.477699)

---

![Img](https://gbatemp.net/attachments/2024122618231700-ca43ec7375ab1e2bc8afc050c0941918-jpg.477700)

---
---
---

## Credits

- borealis
- stb
- yyjson
- nx-hbmenu
- nx-hbloader
- deko3d-nanovg
- libpulsar
- minIni
- gbatemp
- hb-appstore
- haze
- everyone who has contributed to this project!
