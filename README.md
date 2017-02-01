# PyRegRipper

Just a simple tool I wrote some time ago to better understand some forensic artifact. It appeared to become something in the spirit of RegRipper, but if you really want to do some forensic, you should check the real [RegRipper](https://github.com/keydet89/RegRipper2.8).

## Usage

```
Parse windows registry for interesting data

positional arguments:
  PATH                  PATH to the registry file or the system dir

optional arguments:
  -h, --help            show this help message and exit
  -p PLUGIN, --plugin PLUGIN
                        Plugin to be used
  -l                    List plugins
  -v [VERBOSE]
  -f {text,csv,json}, --format {text,csv,json}
```

## Example

```bash
>python2 pyrr.py -p shimcache SYSTEM
----------------------- ShimCache -------------------------
Last Modified Last Update Path File Size Exec Flag
10/14/11 06:01:48 N/A C:\Program Files (x86)\Secunia\PSI\sua.exe N/A True
07/25/15 19:26:14 N/A C:\Program Files (x86)\Avira\AntiVir Desktop\AVWSC.EXE N/A True
11/21/10 03:24:09 N/A C:\Windows\system32\LogonUI.exe N/A True
05/04/11 05:19:28 N/A C:\Windows\system32\SearchFilterHost.exe N/A True
05/04/11 05:19:28 N/A C:\Windows\system32\SearchProtocolHost.exe N/A True
```

## Plugins

```bash
>python2 pyrr.py -l
----------------------------- plugins ------------------------------
- volumeshadow
	['SYSTEM'] Display information on the Volume Shadow Copy

- winevt
	['SOFTWARE'] Display logging policy settings

- wordwheelquery
	['NTUSER'] Get Windows search list in wordwheelquery entry

- autoruns
	['NTUSER', 'SYSTEM'] List software launched at runtime (only registry entries of course)

- prefetch
	['SYSTEM'] Display information on the prefetch configuration

- recentdocs
	['NTUSER'] List windows recent docs

- typedurls
	['NTUSER'] List urls typed in Internet Explorer bar

- services
	['SYSTEM'] List windows services in SYSTEM hive

- shimcache
	['SYSTEM'] Extract shimcache entries

- runmru
	['NTUSER'] List Explorer Run MRU entries
```
