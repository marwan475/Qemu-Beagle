��    4      �  G   \      x  L   y     �     �     �  0     *   7  
   b     m     {  $   �     �  %   �  B   �  #   6  !   Z      |     �     �  #   �  2   �  5   1  *   g  5   �  ?   �  5     C   >  N   �  A   �  0   	  $   D	  /   i	  9   �	  /   �	  @   
  I   D
  <   �
  G   �
  +     6   ?  '   v     �  $   �  +   �  '        4  *   N     y     �     �     �  J   �  �    e   �  "   /  $   R  -   w  R   �  <   �     5  '   D  !   l  B   �  -   �  -   �  \   -  ?   �  +   �  .   �  '   %  *   M  6   x  c   �  C     J   W  ^   �  e     e   g  \   �  q   *  d   �  `     ?   b  N   �  T   �  W   F  T   �  Q   �  H   E  o   �  H   �  H   G  ?   �  $   �  H   �  ;   >  E   z  *   �  E   �     1     D     T     l  b   |                          +      3              "   0   &                  $   *                                 
               2   '       (             !             )      	      /             1   .   4   %   ,       -                            #              The command reads the password to be scored from the standard input.
 BAD PASSWORD: %s Bad integer value Bad integer value of setting Cannot obtain random numbers from the RNG device Could not obtain the password to be scored Error: %s
 Fatal failure Memory allocation error Memory allocation error when setting No password supplied Opening the configuration file failed Password generation failed - required entropy too low for settings Password quality check failed:
 %s
 Setting %s is not of integer type Setting %s is not of string type Setting is not of integer type Setting is not of string type The configuration file is malformed The password contains forbidden words in some form The password contains less than %ld character classes The password contains less than %ld digits The password contains less than %ld lowercase letters The password contains less than %ld non-alphanumeric characters The password contains less than %ld uppercase letters The password contains monotonic sequence longer than %ld characters The password contains more than %ld characters of the same class consecutively The password contains more than %ld same characters consecutively The password contains the user name in some form The password contains too few digits The password contains too few lowercase letters The password contains too few non-alphanumeric characters The password contains too few uppercase letters The password contains too long of a monotonic character sequence The password contains too many characters of the same class consecutively The password contains too many same characters consecutively The password contains words from the real name of the user in some form The password differs with case changes only The password does not contain enough character classes The password fails the dictionary check The password is a palindrome The password is just rotated old one The password is shorter than %ld characters The password is the same as the old one The password is too short The password is too similar to the old one Unknown error Unknown setting Usage: %s <entropy-bits>
 Usage: %s [user]
 Warning: Value %ld is outside of the allowed entropy range, adjusting it.
 Project-Id-Version: PACKAGE VERSION
Report-Msgid-Bugs-To: http://fedorahosted.org/libpwquality
PO-Revision-Date: 2021-05-26 14:02+0000
Last-Translator: Ludek Janda <ljanda@redhat.com>
Language-Team: Japanese <https://translate.fedoraproject.org/projects/libpwquality/app/ja/>
Language: ja
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=1; plural=0;
X-Generator: Weblate 4.6.2
        このコマンドは、評価するパスワードを標準入力から読み込みます。
 正しくないパスワード: %s 正しくない整数型の値です 設定の正しくない整数型の値です RNG (乱数発生) デバイスから乱数を取得することができません 評価するパスワードを取得できませんでした エラー: %s
 致命的な障害が発生しました メモリー割り当てエラー 設定中にメモリー割り当てエラーが発生しました パスワードが与えられていません 設定ファイルを開けませんでした パスワードの生成に失敗: 設定に必要なエントロピーが小さすぎます パスワードの評価チェックに失敗しました:
 %s
 設定 %s は整数型ではありません 設定 %s は文字列型ではありません 設定は整数型ではありません 設定は文字列型ではありません 設定ファイルの形式が正しくありません このパスワードには、何らかの形で禁止されている単語が含まれています このパスワードの文字クラスは、%ld 種類未満です このパスワードには %ld 個未満の数字が含まれています このパスワードに含まれる小文字のアルファベットは、%ld 個未満です このパスワードのに含まれるアルファベット以外の文字数は %ld 個未満です このパスワードには %ld 個未満の大文字のアルファベットが含まれています このパスワードには %ld 文字より長い単調な文字列が含まれています このパスワードには %ld 個を越える連続する同じ文字クラスの文字が含まれています このパスワードはには、%ld 個を越える連続する同じ文字が含まれています このパスワードには、一部に何らかの形でユーザー名が含まれています このパスワードには、数字の個数が足りません このパスワードの小文字のアルファベット数が足りません このパスワードは、アルファベット以外の文字数が足りません このパスワードは、大文字のアルファベットの個数が足りません このパスワードには、長すぎる単調な文字列が含まれています このパスワードは、同じ文字クラス文字の連続が多すぎます このパスワードの連続した同じ文字の数が多すぎます このパスワードには、何らかの形でユーザーの本名に基づく単語が含まれています このパスワードは大文字と小文字を変更しただけです このパスワードに含まれる文字クラス数が足りません このパスワードは辞書チェックに失敗しました このパスワードは回文です このパスワードは、単に古いものを再利用しています このパスワードは %ld 文字未満の文字列です このパスワードは過去に設定されたものと同じです このパスワードは短かすぎます このパスワードは古いパスワードと類似しています 不明なエラー 未知の設定 例: %s <entropy-bits>
 例: %s [user]
 警告: 値 %ld は許可されるエントロピー範囲を超えていまで調整します。
 