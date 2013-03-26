#!/usr/bin/python
# -*- coding: utf8 -*-
# Copyright (C) 2010-2011 Felix Herrmann <fx@herrmannfx.de>

import sys

DSC = """
transliterate russian cyrillics into latin letters
copyright (C) 2010-2011 Felix Herrmann <fx@herrmannfx.de>
"""

USAGE = """
call: "python translit.py '<cyrillics>'"
or:   "python translit.py --file <pathToFile>"

optionally specify the type of the transliteration:
    german scientific (default): "--type de"
    iso:                         "--type iso"
    american:                    "--type us"     

examples:
    "python translit.py --type iso 'русские слова'"
    "python translit.py --file /home/user/doc/file.txt --type us"
    "python translit.py --file /home/user/doc/file.txt"
    
call "python translit.py --help" to see this text
    
"""

ART = """
                            _ _                    
 _                         | (_)_                  
| |_   ____ ____ ____   ___| |_| |_    ____  _   _ 
|  _) / ___) _  |  _ \ /___) | |  _)  |  _ \| | | |
| |__| |  ( ( | | | | |___ | | | |__ _| | | | |_| |
 \___)_|   \_||_|_| |_(___/|_|_|\___|_) ||_/ \__  |
                                      |_|   (____/
                                       
"""


class Translit:
    def get_args(self):        
        args = {}
        args["inputStr"] = u""
        args["type"] = None
                
        if len(sys.argv) < 2:
            print ART
            print DSC
            print USAGE
            exit()
        
        for cnt, arg in enumerate( sys.argv ):
            
            if arg == "--help" or arg == "-h":
                print USAGE
                exit()              
            
            if arg == "--type" or arg == "-t":
                args["type"] = sys.argv[cnt+1]
                
            if arg == "--file" or arg == "-f":
                try:
                    inputFile = open( sys.argv[cnt+1] , "r")
                    for line in inputFile:
                        args["inputStr"] += line.decode("utf-8")
                    inputFile.close()
                    return args                    
                except:
                    print "Datei nicht lesbar oder nicht vorhanden. Beende Ausführung."
                    exit()
            else:
                if cnt == len(sys.argv)-1:                    
                    args["inputStr"] += arg.decode("utf-8")
                    #print args["inputStr"]
            #else:
            #    if arg != sys.argv[0]:
            #        
        
        return args
        
    
    def translit(self, transtype, string):        
    # returns the transliteration of the given utf-8-string
        
        #transtype = params["transtype"]        
        #string = params["inputStr"]
        output = u""
        prevLetter = u""
                
        if transtype == "de" or transtype == None:
            transDict = self.get_transDE()            
        if transtype == "iso":
            transDict = self.get_transISO()
        if transtype == "duden":
            transDict = self.get_transDUDEN()
        if transtype == "us": 
            transDict = self.get_transUS()
        if transtype == "kritika": 
            transDict = self.get_transKritika()
                
        for char in string:            
            try:
                if transDict[char] == "usEx":                                
                    ex, prevLetter = self.usEx(char, prevLetter, self.get_vocalList())
                    output += ex
                elif transDict[char] == "kritikaEx":
                    ex, prevLetter = self.kritikaEx(char, prevLetter, self.get_vocalList())
                    output += ex 
                else:
                    output += transDict[char]
                    prevLetter = char
            except:
                output += char
                prevLetter = char
    
        return output
    
    def usEx(self, char, lastLetter, vocalList):
        "tranliterate 'e' at the beginning of a word or after previous letter is in vocalList as 'ye'"        
        if char==u'Е' and lastLetter==' ' or char==u'Е' and lastLetter=='' or char==u'Е' and lastLetter in vocalList:            
            return 'Ye', char
        else:
            if char==u'е' and lastLetter==' ' or char==u'е' and lastLetter=='' or char==u'е' and lastLetter in vocalList:
                lastLetter = char                                       
                return 'ye', char
    
    def kritikaEx(self, char, lastLetter, vocalList):
        "tranliterate 'i' at the beginning of a word or after previous letter is in vocalList as 'ie'"        
        if char==u'Е' and lastLetter==' ' or char==u'Е' and lastLetter=='' or char==u'Е' and lastLetter in vocalList:            
            return 'Ie', char
        else:
            if char==u'е' and lastLetter==' ' or char==u'е' and lastLetter=='' or char==u'е' and lastLetter in vocalList:
                lastLetter = char                                       
                return 'ie', char
                      
    def get_vocalList(self):
        "list the vocals and the soft/hard sign to check for exceptions"
        return [u'a',u'А',                 
                 u'о', u'О', 
                 u'y', u'У', 
                 u'э', u'Э',
                 u'ы', u'Ы', 
                 u'я', u'Я', 
                 u'ё', u'Ё', 
                 u'ю', u'Ю',
                 u'е', u'Е',
                 u'и', u'И',
                 u'ь', u'Ь', 
                 u'ъ', u'Ъ',
                 ]
        
    
    def print_transDict(self, dict):
        for values in dict.iteritems():
            print values[0] + ":" + values[1]
    
    def get_transISO(self):
        "iso9 transliteration"
        iso = self.get_transDE()
        iso[u'Х'] = u'H'
        iso[u'х'] = u'h'
        iso[u'Щ'] = u'Ŝ'
        iso[u'щ'] = u'ŝ'
        iso[u'Э'] = u'È' 
        iso[u'э'] = u'è'
        iso[u'Ю'] = u'Û'
        iso[u'ю'] = u'û'
        iso[u'Я'] = u'Â'
        iso[u'я'] = u'â'
        return iso
    
    def get_transDE(self):
        "scientific transliteration: return the dictionary with mappings 'russian' : 'transliteration'"
        return {
            u'А':u'A', u'а':u'a',	
            u'Б':u'B', u'б':u'b', 	
            u'В':u'V', u'в':u'v',
            u'Г':u'G', u'г':u'g',
            u'Д':u'D', u'д':u'd', 	
            u'Е':u'E', u'е':u'e',	
            u'Ё':u'Ё', u'ё':u'ё',
            u'Ж':u'Ž', u'ж':u'ž',
            u'З':u'Z', u'з':u'z', 	
            u'И':u'I', u'и':u'i',	
            u'Й':u'J', u'й':u'j', 	
            u'К':u'K', u'к':u'k',	
            u'Л':u'L', u'л':u'l',	
            u'М':u'M', u'м':u'm',	
            u'Н':u'N', u'н':u'n',
            u'О':u'O', u'о':u'o', 	
            u'П':u'P', u'п':u'p', 	
            u'Р':u'R', u'р':u'r', 	
            u'С':u'S', u'с':u's', 	
            u'Т':u'T', u'т':u't', 	
            u'У':U'u', u'у':u'u', 	
            u'Ф':u'F', u'ф':u'f', 	
            u'Х':u'Ch',u'х':u'ch', 	
            u'Ц':u'C', u'ц':u'c',	
            u'Ч':u'Č', u'ч':u'č',
            u'Ш':u'Š', u'ш':u'š',
            u'Щ':u'Šč',u'щ':u'šč',
            u'Ъ':u"’’ ",u'ъ':u"’’",# to-do: Zollzeichen ersetzen durch Hochkomma 	
            u'Ы':u'Y', u'ы':u'y',	
            u'Ь':u"’", u'ь':u"’",	
            u'Э':u'Ė', u'э':u'ė',
            u'Ю':u'Ju',u'ю':u'ju',	
            u'Я':u'Ja',u'я':u'ja',
        }

    def get_transDUDEN(self):
        "TO-DO: German Duden transliteration: return the dictionary with mappings 'russian' : 'transliteration'"
        return {
            u'А':u'A', u'а':u'a',	
            u'Б':u'B', u'б':u'b', 	
            u'В':u'V', u'в':u'v',
            u'Г':u'G', u'г':u'g',
            u'Д':u'D', u'д':u'd', 	
            u'Е':u'E', u'е':u'e',	
            u'Ё':u'Ё', u'ё':u'ё',
            u'Ж':u'Ž', u'ж':u'ž',
            u'З':u'Z', u'з':u'z', 	
            u'И':u'I', u'и':u'i',	
            u'Й':u'J', u'й':u'j', 	
            u'К':u'K', u'к':u'k',	
            u'Л':u'L', u'л':u'l',	
            u'М':u'M', u'м':u'm',	
            u'Н':u'N', u'н':u'n',
            u'О':u'O', u'о':u'o', 	
            u'П':u'P', u'п':u'p', 	
            u'Р':u'R', u'р':u'r', 	
            u'С':u'S', u'с':u's', 	
            u'Т':u'T', u'т':u't', 	
            u'У':u'u', u'у':u'u', 	
            u'Ф':u'F', u'ф':u'f', 	
            u'Х':u'Ch',u'х':u'ch', 	
            u'Ц':u'C', u'ц':u'c',	
            u'Ч':u'Č', u'ч':u'č',
            u'Ш':u'Š', u'ш':u'š',
            u'Щ':u'Šč',u'щ':u'šč',
            u'Ъ':u"''",u'ъ':u"''", 	
            u'Ы':u'Y', u'ы':u'y',	
            u'Ь':u"'", u'ь':u"'",	
            u'Э':u'Ė', u'э':u'ė',
            u'Ю':u'Ju',u'ю':u'ju',	
            u'Я':u'Ja',u'я':u'ja',
        }	
    
    def get_transUS(self):
        "TO-DO: US transliteration: return the dictionary with mappings 'russian' : 'transliteration'"
        return {
            u'А':u'A', u'а':u'a',	
            u'Б':u'B', u'б':u'b', 	
            u'В':u'V', u'в':u'v',
            u'Г':u'G', u'г':u'g',
            u'Д':u'D', u'д':u'd', 	
            u'Е':u"usEx", u'е':u"usEx",	
            u'Ё':u'E', u'ё':u'e',
            u'Ж':u'Zh', u'ж':u'zh',
            u'З':u'Z', u'з':u'z', 	
            u'И':u'I', u'и':u'i',	
            u'Й':u'Y', u'й':u'y', 	
            u'К':u'K', u'к':u'k',	
            u'Л':u'L', u'л':u'l',	
            u'М':u'M', u'м':u'm',	
            u'Н':u'N', u'н':u'n',
            u'О':u'O', u'о':u'o', 	
            u'П':u'P', u'п':u'p', 	
            u'Р':u'R', u'р':u'r', 	
            u'С':u'S', u'с':u's', 	
            u'Т':u'T', u'т':u't', 	
            u'У':u'U', u'у':u'u', 	
            u'Ф':u'F', u'ф':u'f', 	
            u'Х':u'Kh',u'х':u'kh', 	
            u'Ц':u'Ts', u'ц':u'ts',	
            u'Ч':u'Ch', u'ч':u'ch',
            u'Ш':u'Sh', u'ш':u'sh',
            u'Щ':u'Shch',u'щ':u'shch',
            u'Ъ':u"",u'ъ':u"", 	
            u'Ы':u'Y', u'ы':u'y',	
            u'Ь':u"", u'ь':u"",	
            u'Э':u'E', u'э':u'e',
            u'Ю':u'Yu',u'ю':u'yu',	
            u'Я':u'Ya',u'я':u'ya',
        }
        
    def get_transKritika(self):
        "Kritika-Style transliteration: return the dictionary with mappings 'russian' : 'transliteration'"
        return {
            u'А':u'A', u'а':u'a',    
            u'Б':u'B', u'б':u'b',     
            u'В':u'V', u'в':u'v',
            u'Г':u'G', u'г':u'g',
            u'Д':u'D', u'д':u'd',     
            u'Е':u"E", u'е':u"e",    
            u'Ё':u'E', u'ё':u'e',
            u'Ж':u'Zh', u'ж':u'zh',
            u'З':u'Z', u'з':u'z',     
            u'И':u'I', u'и':u'i',    
            u'Й':u'I', u'й':u'i',     
            u'К':u'K', u'к':u'k',    
            u'Л':u'L', u'л':u'l',    
            u'М':u'M', u'м':u'm',    
            u'Н':u'N', u'н':u'n',
            u'О':u'O', u'о':u'o',     
            u'П':u'P', u'п':u'p',     
            u'Р':u'R', u'р':u'r',     
            u'С':u'S', u'с':u's',     
            u'Т':u'T', u'т':u't',     
            u'У':u'U', u'у':u'u',     
            u'Ф':u'F', u'ф':u'f',     
            u'Х':u'Kh',u'х':u'kh',     
            u'Ц':u'Ts', u'ц':u'ts',    
            u'Ч':u'Ch', u'ч':u'ch',
            u'Ш':u'Sh', u'ш':u'sh',
            u'Щ':u'Shch',u'щ':u'shch',
            u'Ъ':u"",u'ъ':u"",     
            u'Ы':u'Y', u'ы':u'y',    
            u'Ь':u"’", u'ь':u"’",    
            u'Э':u'E', u'э':u'e',
            u'Ю':u'Iu',u'ю':u'iu',    
            u'Я':u'Ia',u'я':u'ia',
        }
    
    
    
    def main(self):
        args = self.get_args()
        print self.translit(args["type"], args["inputStr"])
        #params["type"]        
        #string = params["inputStr"]        

if __name__ == "__main__":    
    translit = Translit()
    translit.main()

