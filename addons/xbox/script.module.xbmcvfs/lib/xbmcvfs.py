"""
    module xbmcvfs for xbox
"""

import os
import xbmc


def exists( filename ):
    """ exists(path)

        path        : file or folder
        example:
          success = xbmcvfs.exists(path)
    """
    msg = xbmc.executehttpapi( "FileExists(%s)" % ( filename ) ).replace( "<li>", "" ).lower()
    xbmc.log( "[xbmcvfs] %s, exists(%s)" % ( msg, filename ), xbmc.LOGDEBUG )
    return ( msg == 'true' )


def copy( source, destination ):
    """ copy(source, destination) -- copy file to destination, returns true/false.

        source          : file to copy.
        destination     : destination file
        example:
          success = xbmcvfs.copy(source, destination)
    """
    msg = xbmc.executehttpapi( "FileCopy(%s,%s)" % ( source, destination ) ).replace( "<li>", "" )
    xbmc.log( "[xbmcvfs] %s, copy(%s,%s)" % ( msg, source, destination ), xbmc.LOGDEBUG )
    return exists( destination )


def delete( filename ):
    """ delete(file)

        file        : file to delete
        example:
          xbmcvfs.delete(file)
    """
    msg = xbmc.executehttpapi( "FileDelete(%s)" % ( filename ) ).replace( "<li>", "" )
    xbmc.log( "[xbmcvfs] %s, delete(%s)" % ( msg, filename ), xbmc.LOGDEBUG )
    return ( not exists( filename ) )


def mkdir( path ):
    """ mkdir(path) -- Create a folder.

        path        : folder
        example:
         - success = xbmcvfs.mkdir(path)
    """
    try:
        #os.mkdir( path )
        os.makedirs( path )
        msg = "OK"
    except Exception, e:
        xbmc.log( "[xbmcvfs] %s" % str( e ), xbmc.LOGERROR )
        msg = "ERROR"
    xbmc.log( "[xbmcvfs] %s, mkdir(%s)" % ( msg, path ), xbmc.LOGDEBUG )
    return os.path.exists( path )


def rename( oldName, newName ):
    """ rename(file, newFileName)

        file        : file to rename newFileName : new filename, including the full path
        example:
          success = xbmcvfs.rename(file,newFileName)
    """
    try:
        os.rename( oldName, newName )
        msg = "OK"
    except Exception, e:
        xbmc.log( "[xbmcvfs] %s" % str( e ), xbmc.LOGERROR )
        msg = "ERROR"
    xbmc.log( "[xbmcvfs] %s, rename(%s,%s)" % ( msg, oldName, newName ), xbmc.LOGDEBUG )
    return exists( newName )


def rmdir( path ):
    """ rmdir(path) -- Remove a folder.

        path        : folder
        example:
         - success = xbmcvfs.rmdir(path)
    """
    try:
        os.rmdir( path )
        msg = "OK"
    except Exception, e:
        xbmc.log( "[xbmcvfs] %s" % str( e ), xbmc.LOGERROR )
        msg = "ERROR"
    xbmc.log( "[xbmcvfs] %s, rmdir(%s)" % ( msg, path ), xbmc.LOGDEBUG )
    return ( not os.path.exists( path ) )