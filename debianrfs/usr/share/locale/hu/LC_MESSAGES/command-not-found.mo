��          �   %   �      p     q     �     �     �  .   �  1     :   B  ;   }  6   �  %   �           7     N  9   m     �  +   �  B   �  _   5  f   �     �  -     1   =     o  /   �  8   �  #   �       �    &   �      �  !   	     $	  6   B	  ?   y	  B   �	  A   �	  5   >
  /   t
     �
     �
     �
  5   �
     ,  0   K  K   |  Y   �  g   "      �  4   �  4   �       E   3  W   y  2   �                                                                                     
                                    	         command '%s' from deb %s%s   command '%s' from snap %s%s %prog [options] <command-name> %s: command not found Ask your administrator to install one of them. Command '%(command)s' is available in '%(place)s' Command '%(command)s' is available in the following places Command '%(command)s' not found, but can be installed with: Command '%s' not found, but there are %s similar ones. Command '%s' not found, did you mean: Do you want to install it? (N/y) Exception information: Please ask your administrator. Please include the following information with the report: Python version: %d.%d.%d %s %d See 'snap info %s' for additional versions. Sorry, command-not-found has crashed! Please file a bug report at: The command could not be located because '%s' is not included in the PATH environment variable. This is most likely caused by the lack of administrative privileges associated with your user account. Try: %s <deb name> You will have to enable component called '%s' You will have to enable the component called '%s' command-not-found version: %s don't print '<command-name>: command not found' ignore local binaries and display the available packages use this path to locate data fields y Project-Id-Version: command-not-found
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2018-04-12 19:10+0000
Last-Translator: Gabor Kelemen <kertitorp@gmail.com>
Language-Team: Hungarian <hu@li.org>
Language: hu
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2023-01-20 13:36+0000
X-Generator: Launchpad (build e04feada4865d7ca041d8edeee137fe87b5bcb3e)
   „%s” parancs %s%s deb csomagból   „%s” parancs %s%s snapből %prog [kapcsolók] <parancs neve> %s: a parancs nem található Kérje meg a rendszergazdát az egyik telepítésére. A parancs („%(command)s”) elérhető innen: „%(place)s” A parancs („%(command)s”) a következő helyekről érhető el „%(command)s” parancs nem található, de telepíthető így: „%s” parancs nem található, de van %s hasonló. „%s” parancs nem található, erre gondolt: Szeretné telepíteni? (N/i) Kivételinformációk: Kérje meg a rendszergazdát. A jelentésbe vegye be a következő információkat: Python verzió: %d.%d.%d %s %d További verziókért lásd: „snap info %s”. Elnézést, a command-not-found összeomlott. Küldjön hibajelentést ide: A parancs nem található, mert a PATH környezeti változóból hiányzik a(z) „%s”. Ezt valószínűleg a felhasználói fiókjához tartozó rendszergazdai jogosultságok hiánya okozza. Próbálja ki ezt: %s <deb_neve> Engedélyeznie kell a(z) „%s” nevű összetevőt Engedélyeznie kell a(z) „%s” nevű összetevőt command-not-found verzió: %s ne írja ki a „<parancs-neve>: parancs nem található” szöveget helyi binárisok figyelmen kívül hagyása, és az elérhető csomagok megjelenítése ezen útvonal használata adatmezők kereséséhez i 