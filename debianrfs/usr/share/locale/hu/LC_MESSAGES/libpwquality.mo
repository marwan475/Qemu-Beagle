��    4      �  G   \      x  L   y     �     �     �  0     *   7  
   b     m     {  $   �     �  %   �  B   �  #   6  !   Z      |     �     �  #   �  2   �  5   1  *   g  5   �  ?   �  5     C   >  N   �  A   �  0   	  $   D	  /   i	  9   �	  /   �	  @   
  I   D
  <   �
  G   �
  +     6   ?  '   v     �  $   �  +   �  '        4  *   N     y     �     �     �  J   �  �    Y   �     4     F  #   \  9   �  (   �  	   �     �     �  '        <  /   R  ]   �  2   �  -     (   A  "   j  %   �  *   �  9   �  5     1   N  /   �  A   �  0   �  ?   #  M   c  H   �  @   �  +   ;  )   g  ;   �  *   �  :   �  H   3  =   |  >   �  %   �  -     4   M     �  .   �  %   �  "   �       -   (     V     f  !   ~     �  ^   �                          +      3              "   0   &                  $   *                                 
               2   '       (             !             )      	      /             1   .   4   %   ,       -                            #              The command reads the password to be scored from the standard input.
 BAD PASSWORD: %s Bad integer value Bad integer value of setting Cannot obtain random numbers from the RNG device Could not obtain the password to be scored Error: %s
 Fatal failure Memory allocation error Memory allocation error when setting No password supplied Opening the configuration file failed Password generation failed - required entropy too low for settings Password quality check failed:
 %s
 Setting %s is not of integer type Setting %s is not of string type Setting is not of integer type Setting is not of string type The configuration file is malformed The password contains forbidden words in some form The password contains less than %ld character classes The password contains less than %ld digits The password contains less than %ld lowercase letters The password contains less than %ld non-alphanumeric characters The password contains less than %ld uppercase letters The password contains monotonic sequence longer than %ld characters The password contains more than %ld characters of the same class consecutively The password contains more than %ld same characters consecutively The password contains the user name in some form The password contains too few digits The password contains too few lowercase letters The password contains too few non-alphanumeric characters The password contains too few uppercase letters The password contains too long of a monotonic character sequence The password contains too many characters of the same class consecutively The password contains too many same characters consecutively The password contains words from the real name of the user in some form The password differs with case changes only The password does not contain enough character classes The password fails the dictionary check The password is a palindrome The password is just rotated old one The password is shorter than %ld characters The password is the same as the old one The password is too short The password is too similar to the old one Unknown error Unknown setting Usage: %s <entropy-bits>
 Usage: %s [user]
 Warning: Value %ld is outside of the allowed entropy range, adjusting it.
 Project-Id-Version: PWQuality library
Report-Msgid-Bugs-To: http://fedorahosted.org/libpwquality
PO-Revision-Date: 2021-02-10 17:40+0000
Last-Translator: Balázs Meskó <meskobalazs@mailbox.org>
Language-Team: Hungarian <https://translate.fedoraproject.org/projects/libpwquality/app/hu/>
Language: hu
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=n != 1;
X-Generator: Weblate 4.4.2
        A parancs beolvassa a jelszavát a szabványos bemenetről, hogy pontozhassa azt.
 ROSSZ JELSZÓ: %s Hibás egész érték Hibás egész beállítási érték Az RNG eszköztől nem kaphatóak meg a véletlen számok Nem érhető el a minősítendő jelszó Hiba: %s
 Végzetes hiba Memóriafoglalási hiba Memóriafoglalási hiba beállításkor Nincs jelszó megadva A konfigurációs fájl megnyitása meghiúsult Jelszó előállítás sikertelen – a szükséges entrópia túl kevés a beállításokhoz A jelszó minőség-ellenőrzése meghiúsult:
%s
 A beállított %s érték nem egész típusú A beállítás %s nem szöveges típusú A beállítás nem egész típusú A beállítás nem szöveges típusú A konfigurációs fájl rosszul formázott A jelszó tiltott szavakat tartalmaz valamilyen formában A jelszó kevesebb mint %ld karaktertípust tartalmaz A jelszó kevesebb mint %ld számjegyet tartalmaz A jelszó kevesebb mint %ld kisbetűt tartalmaz A jelszó kevesebb mint %ld nem alfanumerikus karaktert tartalmaz A jelszó kevesebb mint %ld nagybetűt tartalmaz A jelszó %ld karakternél hosszabb monoton sorozatot tartalmaz A jelszó több mint %ld ugyanolyan típusú ismétlődő karaktert tartalmaz A jelszó több mint %ld egyforma, egymást követő karaktert tartalmaz A jelszó tartalmazza a felhasználónevét valamilyen formában A jelszó túl kevés számjegyet tartalmaz A jelszó túl kevés kisbetűt tartalmaz A jelszó túl kevés nem alfanumerikus karaktert tartalmaz A jelszó túl kevés nagybetűt tartalmaz A jelszó túl hosszú monoton karaktersorozatot tartalmaz A jelszó túl sok ismétlődő, ugyanolyan típusú karaktert tartalmaz A jelszó ismétlődően tartalmazza ugyanazon a karaktereket A jelszó szavakat tartalmaz a felhasználó valódi nevéből A jelszó csak betűcserében tér el A jelszó nem tartalmaz elég karaktertípust A jelszó fennakadt a szótár alapú ellenőrzésen A jelszó egy palindrom A jelszó egy újrahasznosított régi jelszó A jelszó rövidebb mint %ld karakter A jelszó megegyezik a korábbival A jelszó túl rövid A jelszó túlságosan hasonlít a korábbira Ismeretlen hiba Ismeretlen beállítás Használat: %s <entrópia-bitek>
 Használat: %s [felhasználó]
 Figyelmeztetés: A(z) %ld kívül esik az engedélyezett entrópiatartományon, kiigazítás.
 