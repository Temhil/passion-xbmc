
import os
import re
import sys
from traceback import print_exc

try: import xbmc
except: xbmc = None


__script__ = "IPX"

PRINT_DEBUG = False
PRINT_ERROR = True

LOGS_REGEXP  = "bypass: |bypass_debug: |bypass_comment: "
bypass_debug = re.compile( LOGS_REGEXP ).search


def notif( msg="" ):
    try:
        msg = msg or str( sys.exc_info()[ 1 ] )
        if xbmc is not None:
            if ( xbmc.Settings( os.getcwd() ).getSetting( "notif_error" ) == "true" ) and not xbmc.getCondVisibility( "Window.IsVisible(infodialog)" ):
                notif = "%s!,%s,4000,DefaultIconError.png" % ( xbmc.getLocalizedString( 257 ), msg )
                xbmc.executebuiltin( "XBMC.Notification(%s)" % notif )
    except:
        pass


class Logger( object ):
    def __init__( self ):
        self.terminal = sys.stdout

    def write( self, message ):
        BYPASS = bypass_debug( message )
        comment = not message.startswith( "bypass_comment" )
        if PRINT_DEBUG or BYPASS or not message.strip( "\r\n " ):
            message = re.split( LOGS_REGEXP, message, 1 )[ -1 ]
            if not message.strip( "\r\n " ) or not comment: self.terminal.write( message )
            else: self.terminal.write( "[SCRIPT %s]: %s" % ( __script__, message ) )


class Logerr( object ):
    def __init__( self ):
        self.terminal = sys.stderr

    def write( self, message ):
        if PRINT_ERROR:
            if not message.strip( "\r\n " ): self.terminal.write( message )
            else: self.terminal.write( "[SCRIPT %s] ERROR: %s" % ( __script__, message ) )
        notif()


try:
    sys.stdout = Logger()
    sys.stderr = Logerr()
except:
    print_exc()



if __name__ == "__main__":
    # prints "1 2" to <stdout>
    print "%i - %i - %i - %i.... Houston" % ( 1, 2, 1, 2 )
    #print not PRINT_DEBUG
    try: import Houston
    except:
        print_exc()
        print
        print "bypass: putain je suis dans la merdre ! :(", "bypass_debug: %s" % repr( not PRINT_DEBUG )
        print "bypass: putain je suis dans la merdre ! :(", "bypass_comment: %s" % repr( not PRINT_DEBUG )
    sys.stdout = sys.stdout.terminal
    sys.stderr = sys.stderr.terminal
