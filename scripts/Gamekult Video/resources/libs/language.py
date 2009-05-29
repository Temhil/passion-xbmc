"""
Language module

Nuka1195

Modified by temhil in order to add language selection
"""

import os
import xbmc
import xml.dom.minidom


class Language:
    """ Language Class: creates a dictionary of localized strings { int: string } """
    DEFAULT_LANGUAGE = "English"

    def __init__( self ):
        """ initializer """
        # language folder
        self.base_path = os.path.join( os.getcwd(), "resources", "language" )
        
        # get the current language
        self.language = self._get_language()
        
        #language = self._get_language( base_path )
        
        # create strings dictionary
        self._create_localized_dict(self.language )
        
    def _is_language_available( self, language ):
        """ returns the current language if a strings.xml file exists else returns default language """
        result = True
        # if no strings.xml file exists, use default language
        if ( not os.path.isfile( os.path.join( self.base_path, language, "strings.xml" ) ) ):
            result = False
        return result

    
    def _get_language( self):
        """ returns the language USED BY THE SKIN if a strings.xml file exists else returns default language """
        # get the current users language setting
        language = xbmc.getLanguage()
        # if no strings.xml file exists, use default language
        if ( not os.path.isfile( os.path.join( self.base_path, language, "strings.xml" ) ) ):
            language = self.DEFAULT_LANGUAGE
        return language

    def _create_localized_dict( self, language ):
        """ initializes self.strings and calls _parse_strings_file """
        # localized strings dictionary
        self.strings = {}
        
        # add localized strings
        self._parse_strings_file( os.path.join( self.base_path, language, "strings.xml" ) )
        # fill-in missing strings with default language strings
        if ( language != self.DEFAULT_LANGUAGE ):
            self._parse_strings_file( os.path.join( self.base_path, self.DEFAULT_LANGUAGE, "strings.xml" ) )
        print self.strings
        
    def _parse_strings_file( self, language_path ):
        """ adds localized strings to self.strings dictionary """
        try:
            # load and parse strings.xml file
            doc = xml.dom.minidom.parse( language_path )
            # make sure this is a valid <strings> xml file
            root = doc.documentElement
            if ( not root or root.tagName != "strings" ): raise
            # parse and resolve each <string id="#"> tag
            strings = root.getElementsByTagName( "string" )
            for string in strings:
                # convert id attribute to an integer
                string_id = int( string.getAttribute( "id" ) )
                # if a valid id add it to self.strings dictionary
                if ( string_id not in self.strings and string.hasChildNodes() ):
                    self.strings[ string_id ] = string.firstChild.nodeValue
        except:
            # print the error message to the log and debug window
            xbmc.output( "ERROR: Language file %s can't be parsed!" % ( language_path, ) )
        # clean-up document object
        try: doc.unlink()
        except: pass

    def getLanguageString( self, code ):
        """ returns the string corresponding to the current language if it exists """
        return self.strings.get( code, "Invalid Id %d" % ( code, ) )

    def setLanguage( self, language ):
        """ returns current language """
        if self._is_language_available(language):
            self.language = language
        
        # create strings dictionary
        self._create_localized_dict( self.language )
        
    def getCurrentLanguage( self ):
        """ returns current language """
        return self.language
