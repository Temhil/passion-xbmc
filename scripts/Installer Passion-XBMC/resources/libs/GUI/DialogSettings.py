
# Modules general
import os
import sys
from collections import deque
from traceback import print_exc

# Modules XBMC
import xbmc
import xbmcgui

# Modules custom
from utilities import *

# set our xbmc.settings path for xbmc get '/resources/settings.xml'
XBMC_SETTINGS = xbmc.Settings( os.getcwd() )

#FONCTION POUR RECUPERER LES LABELS DE LA LANGUE.
_ = sys.modules[ "__main__" ].__language__

current_skin, force_fallback = getUserSkin()
XBMCGUI_WINDOW_XML = ( "xbmcgui.WindowXMLDialog", "xbmcgui.WindowXML" )[ current_skin == "Default.HD" ]


class ScriptSettings( eval( XBMCGUI_WINDOW_XML ) ):
    SERVERS     = [ "Passion XBMC", "Passion XBMC FTP", "XBMC Zone" ]
    TOPIC_LIMIT = [ "5", "10", "15", "20", "25", "50", "100" ]
    TSIZE_LIMIT = [ "192", "256", "384", "512", "1024" ]

    # control id's
    CONTROL_RESET_BUTTON            = 1001
    CONTROL_OK_BUTTON               = 1002
    CONTROL_CANCEL_BUTTON           = 1003
    CONTROL_CANCEL2_BUTTON          = 320 # bouton for mouse only
    CONTROLS_CANCEL                 = ( CONTROL_CANCEL_BUTTON, CONTROL_CANCEL2_BUTTON )
    # GENERAL
    CONTROL_RSS_FEEDS_LIST          = 9102
    CONTROL_DECREASE_RSS_BUTTON     = 9121
    CONTROL_INCREASE_RSS_BUTTON     = 9122
    CONTROLS_RSS                    = ( CONTROL_RSS_FEEDS_LIST, CONTROL_DECREASE_RSS_BUTTON, CONTROL_INCREASE_RSS_BUTTON )
    CONTROL_HIDE_FORUM_BUTTON       = 9103
    CONTROL_EXTENTION_BUTTON        = 9105
    CONTROL_PARENT_DIR_BUTTON       = 9106
    CONTROL_SERVERS_LIST            = 9107
    CONTROL_DECREASE_SERVERS_BUTTON = 9171
    CONTROL_INCREASE_SERVERS_BUTTON = 9172
    CONTROLS_SERVERS                = ( CONTROL_SERVERS_LIST, CONTROL_DECREASE_SERVERS_BUTTON, CONTROL_INCREASE_SERVERS_BUTTON )
    # APPEARANCE
    CONTROL_SKIN_LIST               = 9502
    CONTROL_DECREASE_SKIN_BUTTON    = 9521
    CONTROL_INCREASE_SKIN_BUTTON    = 9522
    CONTROLS_SKIN                   = ( CONTROL_SKIN_LIST, CONTROL_DECREASE_SKIN_BUTTON, CONTROL_INCREASE_SKIN_BUTTON )
    CONTROL_SYNCHRO_COLORS_LISTS    = 9507
    CONTROL_SKIN_COLOR_LIST         = 9503
    CONTROL_DECREASE_COLOR_BUTTON   = 9531
    CONTROL_INCREASE_COLOR_BUTTON   = 9532
    CONTROLS_SKIN_COLOR             = ( CONTROL_SKIN_COLOR_LIST, CONTROL_DECREASE_COLOR_BUTTON, CONTROL_INCREASE_COLOR_BUTTON )
    CONTROL_LABELS_COLOR_LIST       = 9506
    CONTROL_DECREASE_LCOLOR_BUTTON  = 9561
    CONTROL_INCREASE_LCOLOR_BUTTON  = 9562
    CONTROLS_LABELS_COLOR           = ( CONTROL_LABELS_COLOR_LIST, CONTROL_DECREASE_LCOLOR_BUTTON, CONTROL_INCREASE_LCOLOR_BUTTON )
    CONTROL_THUMB_SIZE_LIST         = 9505
    CONTROL_DECREASE_TSIZE_BUTTON   = 9551
    CONTROL_INCREASE_TSIZE_BUTTON   = 9552
    CONTROLS_THUMB_SIZE             = ( CONTROL_THUMB_SIZE_LIST, CONTROL_DECREASE_TSIZE_BUTTON, CONTROL_INCREASE_TSIZE_BUTTON )
    # FORUM
    CONTROL_LIMIT_TOPIC_LIST        = 9202
    CONTROL_DECREASE_TOPIC_BUTTON   = 9221
    CONTROL_INCREASE_TOPIC_BUTTON   = 9222
    CONTROLS_TOPIC                  = ( CONTROL_LIMIT_TOPIC_LIST, CONTROL_DECREASE_TOPIC_BUTTON, CONTROL_INCREASE_TOPIC_BUTTON  )
    CONTROL_WEB_BUTTON              = 9204
    #HELP
    CONTROL_EN_SUPPORT_BUTTON       = 9408
    CONTROL_FR_SUPPORT_BUTTON       = 9405

    # SYSTEM
    # this button moved into settings.xml
    CONTROL_UPDATE_STARTUP_BUTTON   = 140
    CONTROL_SCRIPT_DEBUG_BUTTON     = 150
    CONTROL_SHOW_SPLASH_BUTTON      = 180

    # OLD BUTTON
    CONTROL_CUSTOM_BG_BUTTON        = 230
    CONTROL_RSS_FEEDS_LABEL         = 120 # changed for CONTROL_RSS_FEEDS_LIST
    CONTROL_SKIN_COLOR_LABEL        = 220 # changed for CONTROL_SKIN_COLOR_LIST
    CONTROL_THUMB_SIZE_LABEL        = 280 # changed for CONTROL_THUMB_SIZE_LIST
    CONTROL_SKIN_LABEL              = 292 # changed for CONTROL_SKIN_LIST
    CONTROL_LIMIT_TOPIC_LABEL       = 320 # changed for CONTROL_LIMIT_TOPIC_LIST

    # DEPRECATED
    CONTROL_WIN32_WAIT_BUTTON       = 9205
    CONTROL_SHOW_FANART_BUTTON      = 250
    CONTROL_XML_UPDATE_BUTTON       = 130

    def __init__( self, *args, **kwargs ):
        exec "%s.__init__( self, *args, **kwargs )" % XBMCGUI_WINDOW_XML
        if "Dialog" in XBMCGUI_WINDOW_XML:
            xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
            xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
        # __init__ normal de python
        # On recupere le "self" de le fenetre principal pour benificier de ces variables.
        self.mainwin       = kwargs[ "mainwin" ]
        self.homeLastPosition = kwargs.get( "homeLastPosition" )
        self.reload_script = False
        self.last_control_colors_focused = 0

        # recupere la valeur sur le demarrage, utiliser pour rafraifir en temps reel, si l'etat est pas le meme
        self.passion_show_fanart   = xbmc.getCondVisibility( "!Skin.HasSetting(PassionShowFanart)" )
        self.use_custom_background = xbmc.getCondVisibility( "!Skin.HasSetting(use_passion_custom_background)" )
        self.custom_background     = unicode( xbmc.getInfoLabel( 'Skin.String(passion_custom_background)' ), 'utf-8')

    def onInit( self ):
        # onInit est pour le windowXML seulement
        try:
            self._get_settings()
            self._set_skin_colours()
            self._set_controls_values()

            # recupere la valeur sur le demarrage, utiliser pour rafraifir en temps reel, si l'etat est pas le meme
            self.coulour_on_load = self.settings[ "skin_colours_path" ]
            self.rss_on_load     = self.settings[ "rss_feed" ]
            self.skin_on_load    = self.settings.get( "current_skin", "Default.HD" )

        except:
            print_exc()
            self._close_dialog()

    def _get_settings( self, defaults=False  ):
        """ reads settings """
        self.topic_limit  = deque( self.TOPIC_LIMIT )
        self.skin_colours = getSkinColors()
        self.settings     = Settings().get_settings( defaults=defaults )
        self.settings[ "script_debug" ] = ( XBMC_SETTINGS.getSetting( "script_debug" ) == "true" )
        if defaults:
            xbmc.executebuiltin( "Skin.Reset(use_passion_custom_background)" )
            xbmc.executebuiltin( "Skin.Reset(passion_custom_background)" )
            xbmc.executebuiltin( "Skin.Reset(PassionShowFanart)" )
        self.settings[ "labels_colours" ] = ( self.settings[ "labels_colours" ] or get_default_hex_color( "Blue Confluence" ) )

    def _set_skin_colours( self ):
        try:
            xbmc.executebuiltin( "Skin.SetString(PassionSkinColourPath,%s)" % ( self.settings[ "skin_colours_path" ], ) )
            xbmc.executebuiltin( "Skin.SetString(PassionSkinHexColour,%s)"  % ( ( self.settings[ "skin_colours" ] or get_default_hex_color() ), ) )
            xbmc.executebuiltin( "Skin.SetString(PassionLabelHexColour,%s)" % ( ( self.settings[ "labels_colours" ] or get_default_hex_color( "Blue Confluence" ) ), ) )
        except:
            xbmc.executebuiltin( "Skin.SetString(PassionLabelHexColour,ffffffff)" )
            xbmc.executebuiltin( "Skin.SetString(PassionSkinHexColour,ffffffff)" )
            xbmc.executebuiltin( "Skin.SetString(PassionSkinColourPath,default)" )
            print_exc()

    def _set_controls_values( self ):
        xbmcgui.lock()
        try:
            #le bouton valider les changements ont le desactive, il va etre reactiver seulement s'il y a un changement dans les settings
            self.getControl( self.CONTROL_OK_BUTTON ).setVisible( False )

            # GENERAL
            # boutons pour le flux rss
            self._set_control_rss_feeds()
            # servers shortcut bouton Installer in Home
            self._set_control_servers()
            #selon l'etat de self.settings[ "hide_forum" ], l'image du radiobutton sera blanc ou non visible
            try: self.getControl( self.CONTROL_HIDE_FORUM_BUTTON ).setSelected( self.settings.get( "hide_forum", False ) )
            except: pass
            #selon l'etat de self.settings[ "hide_extention" ], l'image du radiobutton sera blanc ou non visible
            try: self.getControl( self.CONTROL_EXTENTION_BUTTON ).setSelected( self.settings.get( "hide_extention", True ) )
            except: pass
            #selon l'etat de self.settings[ "pardir_not_hidden" ], l'image du radiobutton sera blanc ou non visible
            try: self.getControl( self.CONTROL_PARENT_DIR_BUTTON ).setSelected( not self.settings.get( "pardir_not_hidden", 1 ) )
            except: pass

            # APPEARANCE
            self._set_control_skins()
            # boutons pour la couleur du theme et la couleur des labels
            self._set_control_colors()
            #boutons pour la taille des vignettes
            self._set_control_tbn_size()

            # FORUM
            # boutons pour la limitation des topics
            self._set_control_limit_topics()
            # boutons pour le web
            self._set_control_web_visibility()

            # SYSTEM, moved in setting.xml, but work with Default skin
            #selon l'etat de self.settings[ "update_startup" ], l'image du radiobutton sera blanc ou non visible
            try: self.getControl( self.CONTROL_UPDATE_STARTUP_BUTTON ).setSelected( self.settings[ "update_startup" ] )
            except: pass
            #selon l'etat de self.settings[ "script_debug" ], l'image du radiobutton sera blanc ou non visible
            try: self.getControl( self.CONTROL_SCRIPT_DEBUG_BUTTON ).setSelected( self.settings[ "script_debug" ] )
            except: pass
            #selon l'etat de self.settings[ "show_plash"], l'image du radiobutton sera blanc ou non visible
            try: self.getControl( self.CONTROL_SHOW_SPLASH_BUTTON ).setSelected( self.settings.get( "show_plash", False ) )
            except: pass

            # DEPRECATED
            # pour bouton activer desactiver la modification du fichier sources.xml, si la version d'xbmc est compatible atlantis
            #atlantis = not bool( re.search( "\\b(pre-8.10|8.10)\\b", xbmc.getInfoLabel( "System.BuildVersion" ) ) )
            #bouton pour activer desactiver la modification du fichier sources.xml
            #selon l'etat de self.settings[ "xbmc_xml_update" ], l'image du radiobutton sera blanc ou non visible
            # xbmc_xml_update: DEPRECATED
            try: self.getControl( self.CONTROL_XML_UPDATE_BUTTON ).setSelected( self.settings[ "xbmc_xml_update" ] )#atlantis )
            except: pass
        except Exception, e:
            if not "Non-Existent Control" in str( e ):
                print_exc()
        xbmcgui.unlock()

    def _set_control_rss_feeds( self ):
        try:
            self.rss_feeds = parse_rss_xml()
            if self.rss_feeds:
                self.getControl( self.CONTROL_RSS_FEEDS_LIST ).reset()
                listitem = xbmcgui.ListItem( _( 511 ), "Aucun" )
                listitem.setProperty( "url_set", "0" )
                self.getControl( self.CONTROL_RSS_FEEDS_LIST ).addItem( listitem )
                for key, value in sorted( self.rss_feeds.items(), key=lambda k: k[ 0 ] ):
                    listitem = xbmcgui.ListItem( _( 511 ), value.get( "title", _( 506 ) ) )
                    #print key
                    listitem.setProperty( "url_set", str( key ) )
                    self.getControl( self.CONTROL_RSS_FEEDS_LIST ).addItem( listitem )
                pos = int( self.settings[ "rss_feed" ] )
                self.getControl( self.CONTROL_RSS_FEEDS_LIST ).selectItem( pos )
        except:
            print_exc()

    def _set_control_servers( self ):
        try:
            self.getControl( self.CONTROL_SERVERS_LIST ).reset()
            for server in self.SERVERS:
                self.getControl( self.CONTROL_SERVERS_LIST ).addItem( xbmcgui.ListItem( _( 522 ), server ) )
            pos = self.SERVERS.index( self.settings.get( "server_shortcut_button", self.SERVERS[ 0 ] ) )
            self.getControl( self.CONTROL_SERVERS_LIST ).selectItem( int( pos ) )
        except:
            print_exc()

    def _set_control_skins( self ):
        try:
            self.current_skin  = self.settings.get( "current_skin", "Default.HD" )
            self.skins_listing = getSkinsListing()
            total_skins = len( self.skins_listing )
            self.getControl( self.CONTROL_SKIN_LIST ).reset()
            for count, skin in enumerate( self.skins_listing ):
                listitem = xbmcgui.ListItem( "Skin", skin )
                listitem.setProperty( "skinname", skin )
                listitem.setProperty( "position", "(%i/%i)" % ( count+1, total_skins ) )
                self.getControl( self.CONTROL_SKIN_LIST ).addItem( listitem )
            pos = self.skins_listing.index( self.settings.get( "current_skin", "Default.HD" ) )
            self.getControl( self.CONTROL_SKIN_LIST ).selectItem( pos )
        except:
            print_exc()

    def _set_control_colors( self ):
        try:
            pos1 = pos2 = 0
            total_colors = len( self.skin_colours )
            listitems1 = []
            listitems2 = []
            for count, color in enumerate( self.skin_colours ):
                if self.settings[ "skin_colours_path" ] == color[ 0 ]:#self.settings[ "skin_colours" ] == color[ 1 ] and 
                    pos1 = count
                if self.settings[ "labels_colours" ] == color[ 1 ]:
                    pos2 = count

                listitem = xbmcgui.ListItem( color[ 0 ], _( 505 ) )
                listitem.setProperty( "color", color[ 1 ] )
                listitem.setProperty( "colorname", color[ 0 ] )
                listitem.setProperty( "position", "(%i/%i)" % ( count+1, total_colors ) )
                listitems1.append( listitem )

                label = "[COLOR=%s]%s[/COLOR]" % ( color[ 1 ], color[ 0 ] )
                listitem = xbmcgui.ListItem( label, _( 523 ) )
                listitem.setProperty( "color", color[ 1 ] )
                listitem.setProperty( "colorname", color[ 0 ] )
                listitem.setProperty( "position", "(%i/%i)" % ( count+1, total_colors ) )
                listitems2.append( listitem )

            self.getControl( self.CONTROL_SKIN_COLOR_LIST ).reset()
            self.getControl( self.CONTROL_LABELS_COLOR_LIST ).reset()
            # addItems(...); Large lists benefit considerably, than using the standard addItem()
            self.getControl( self.CONTROL_SKIN_COLOR_LIST ).addItems( listitems1 )
            self.getControl( self.CONTROL_LABELS_COLOR_LIST ).addItems( listitems2 )
            self.getControl( self.CONTROL_SKIN_COLOR_LIST ).selectItem( pos1 )
            self.getControl( self.CONTROL_LABELS_COLOR_LIST ).selectItem( pos2 )
        except:
            print_exc()

    def _set_control_tbn_size( self ):
        try:
            self.getControl( self.CONTROL_THUMB_SIZE_LIST ).reset()
            for tsize in self.TSIZE_LIMIT:
                self.getControl( self.CONTROL_THUMB_SIZE_LIST ).addItem( xbmcgui.ListItem( _( 517 ), tsize ) )
            pos = self.TSIZE_LIMIT.index( self.settings[ "thumb_size" ] )
            self.getControl( self.CONTROL_THUMB_SIZE_LIST ).selectItem( int( pos ) )
        except:
            print_exc()

    def _set_control_limit_topics( self ):
        try:
            self.getControl( self.CONTROL_LIMIT_TOPIC_LIST ).reset()
            for limit in self.TOPIC_LIMIT:
                self.getControl( self.CONTROL_LIMIT_TOPIC_LIST ).addItem( xbmcgui.ListItem( _( 502 ), limit ) )
            pos = self.TOPIC_LIMIT.index( self.settings[ "topics_limit" ] )
            self.getControl( self.CONTROL_LIMIT_TOPIC_LIST ).selectItem( int( pos ) )
        except:
            print_exc()

    def _set_control_web_visibility( self ):
        try:
            compatible = ( SYSTEM_PLATFORM in ( "windows", "linux", "osx" ) )
            web_title = self.settings.get( "web_title", "" ) or  _( 506 )
            self.getControl( self.CONTROL_WEB_BUTTON ).setLabel( _( 518 ), label2=web_title )
            self.getControl( self.CONTROL_WEB_BUTTON ).setEnabled( compatible )
            self.getControl( self.CONTROL_WEB_BUTTON ).setVisible( compatible )
            self.getControl( self.CONTROL_WIN32_WAIT_BUTTON ).setSelected( self.settings[ "win32_exec_wait" ] )
            self.getControl( self.CONTROL_WIN32_WAIT_BUTTON ).setEnabled( bool( self.settings[ "web_navigator" ] ) )
        except Exception, e:
            if not "Non-Existent Control" in str( e ):
                print_exc()

    def onFocus( self, controlID ):
        #cette fonction n'est pas utiliser ici, mais dans les XML si besoin
        #Note: Mais il faut la declarer :)
        pass

    def onClick( self, controlID ):
        try:
            if controlID in self.CONTROLS_CANCEL:
                # bouton annuler on ferme le dialog
                self._close_dialog()

            elif controlID in self.CONTROLS_RSS:
                self.toggle_rss_control( controlID )

            elif controlID in self.CONTROLS_SERVERS:
                self.toggle_servers_control()

            elif controlID in self.CONTROLS_SKIN:
                self.toggle_skin_control( controlID )

            elif controlID in self.CONTROLS_SKIN_COLOR:
                self.toggle_color_control( controlID )

            elif controlID in self.CONTROLS_LABELS_COLOR:
                self.toggle_labels_color_control()

            elif controlID in self.CONTROLS_THUMB_SIZE:
                self.toggle_tbn_size_control( controlID )

            elif controlID in self.CONTROLS_TOPIC:
                self.toggle_topic_control( controlID )

            elif controlID == self.CONTROL_HIDE_FORUM_BUTTON:
                #bouton pour masquer le bouton forum du menu principal
                self._set_bool_setting( "hide_forum" )

            elif controlID == self.CONTROL_PARENT_DIR_BUTTON:
                #bouton pour activer desactiver le repertoire parent dans les listes
                self._set_bool_setting( "pardir_not_hidden" )

            elif controlID == self.CONTROL_EXTENTION_BUTTON:
                #bouton pour activer desactiver les extentions dans les noms des items
                self._set_bool_setting( "hide_extention" )

            elif controlID == self.CONTROL_WEB_BUTTON:
                #bouton pour choisir le navigateur web
                self._set_web_navigator()

            elif controlID == self.CONTROL_EN_SUPPORT_BUTTON:
                # english support
                self._url_launcher( "%s..." % _( 551 ), "http://passion-xbmc.org/supportIPX.html?lang=en" )

            elif controlID == self.CONTROL_FR_SUPPORT_BUTTON:
                # french support
                self._url_launcher( "%s..." % _( 550 ), "http://passion-xbmc.org/supportIPX.html?lang=fr" )

            elif controlID == self.CONTROL_RESET_BUTTON:
                #bouton reset settings, ont recup les settings par default
                self._reset_settings()

            elif controlID == self.CONTROL_OK_BUTTON:
                #bouton ok on save les changements.
                self._save_settings()

            elif controlID == self.CONTROL_WIN32_WAIT_BUTTON:
                #bouton pour activer desactiver wait state win32 seulement
                self._set_bool_setting( "win32_exec_wait" )

            elif controlID == self.CONTROL_SHOW_FANART_BUTTON:
                #bouton fanart background a ete activer depuis le xml
                #balise utiliser: <onclick>Skin.ToggleSetting(PassionShowFanart)</onclick>
                self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )

            elif controlID == self.CONTROL_CUSTOM_BG_BUTTON:
                #bouton custom background a ete activer depuis le xml
                #balise utiliser: <onclick>Skin.ToggleSetting(use_passion_custom_background)</onclick>
                self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )

            elif controlID == self.CONTROL_XML_UPDATE_BUTTON:
                #bouton pour activer desactiver la modification du fichier sources.xml
                self._set_bool_setting( "xbmc_xml_update" )

            elif controlID == self.CONTROL_UPDATE_STARTUP_BUTTON:
                #bouton pour activer desactiver la verification de la mise a jour au demarrage
                self._set_bool_setting( "update_startup" )

            elif controlID == self.CONTROL_SCRIPT_DEBUG_BUTTON:
                #bouton pour activer desactiver la mode debug du script seulement
                self._set_bool_setting( "script_debug" )

            elif controlID == self.CONTROL_SHOW_SPLASH_BUTTON:
                #bouton pour activer desactiver le spalsh
                self._set_bool_setting( "show_plash" )

            elif controlID == self.CONTROL_SYNCHRO_COLORS_LISTS:
                self.synchronize_colors_controls()

            else:
                pass
        except Exception, e:
            if not "Non-Existent Control" in str( e ):
                print_exc()

    def _set_bool_setting( self, str_setting ):
        if not self.settings[ str_setting ]:
            #Active
            self.settings[ str_setting ] = True
        else:
            #Desactive
            self.settings[ str_setting ] = False
        self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
        # delete le str
        del str_setting

    def toggle_rss_control( self, controlID ):
        try:
            xbmc.sleep( 5 )
            rss_id = self.getControl( self.CONTROL_RSS_FEEDS_LIST ).getSelectedItem().getProperty( "url_set" )
            self.settings[ "rss_feed" ] = str( int( rss_id ) )
            self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
        except: 
            print_exc()

    def toggle_servers_control( self ):
        try:
            xbmc.sleep( 5 )
            server = self.getControl( self.CONTROL_SERVERS_LIST ).getSelectedItem().getLabel2()
            self.settings[ "server_shortcut_button" ] = server
            self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
        except:
            print_exc()

    def toggle_skin_control( self, controlID ):
        try:
            xbmc.sleep( 5 )
            new_skin = self.getControl( self.CONTROL_SKIN_LIST ).getSelectedItem().getProperty( "skinname" )
            self.current_skin = new_skin
            self.settings[ "current_skin" ] = self.current_skin
            self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
        except: 
            print_exc()

    def synchronize_colors_controls( self ):
        try:
            if self.getControl( self.CONTROL_SYNCHRO_COLORS_LISTS ).isSelected():
                if self.last_control_colors_focused == self.CONTROLS_SKIN_COLOR:
                    synchro = self.getControl( self.CONTROL_SKIN_COLOR_LIST ).getSelectedPosition()
                    self.getControl( self.CONTROL_LABELS_COLOR_LIST ).selectItem( synchro )
                    color = self.getControl( self.CONTROL_LABELS_COLOR_LIST ).getSelectedItem().getProperty( "color" )
                    self.settings[ "labels_colours" ] = color
                    self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
                elif self.last_control_colors_focused == self.CONTROLS_LABELS_COLOR:
                    synchro = self.getControl( self.CONTROL_LABELS_COLOR_LIST ).getSelectedPosition()
                    self.getControl( self.CONTROL_SKIN_COLOR_LIST ).selectItem( synchro )
                    color = self.getControl( self.CONTROL_SKIN_COLOR_LIST ).getSelectedItem().getProperty( "color" )
                    colorname = self.getControl( self.CONTROL_SKIN_COLOR_LIST ).getSelectedItem().getProperty( "colorname" )
                    self.settings[ "skin_colours_path" ] = colorname
                    self.settings[ "skin_colours" ] = color
                    self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
        except:
            print_exc()

    def toggle_labels_color_control( self ):
        try:
            xbmc.sleep( 5 )
            color = self.getControl( self.CONTROL_LABELS_COLOR_LIST ).getSelectedItem().getProperty( "color" )
            self.settings[ "labels_colours" ] = color
            self.last_control_colors_focused = self.CONTROLS_LABELS_COLOR
            self.synchronize_colors_controls()
            self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
        except:
            print_exc()

    def toggle_color_control( self, controlID ):
        try:
            xbmc.sleep( 5 )
            color = self.getControl( self.CONTROL_SKIN_COLOR_LIST ).getSelectedItem().getProperty( "color" )
            colorname = self.getControl( self.CONTROL_SKIN_COLOR_LIST ).getSelectedItem().getProperty( "colorname" )
            self.settings[ "skin_colours_path" ] = colorname
            self.settings[ "skin_colours" ] = color
            self.last_control_colors_focused = self.CONTROLS_SKIN_COLOR
            self.synchronize_colors_controls()
            self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
        except:
            print_exc()

    def toggle_tbn_size_control( self, controlID ):
        try:
            xbmc.sleep( 5 )
            new_size = self.getControl( self.CONTROL_THUMB_SIZE_LIST ).getSelectedItem().getLabel2()
            self.settings[ "thumb_size" ] = str( int( new_size ) )
            self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
        except:
            print_exc()

    def toggle_topic_control( self, controlID ):
        try:
            xbmc.sleep( 5 )
            new_limit = self.getControl( self.CONTROL_LIMIT_TOPIC_LIST ).getSelectedItem().getLabel2()
            self.settings[ "topics_limit" ] = str( int( new_limit ) )
            self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
        except:
            print_exc()

    def _set_web_navigator( self ):
        web_navigator = set_web_navigator( self.settings[ "web_navigator" ] )
        if web_navigator:
            self.settings[ "web_title" ] = web_navigator[ 0 ]
            self.settings[ "web_navigator" ] = web_navigator[ 1 ]
            self.getControl( self.CONTROL_WEB_BUTTON ).setLabel( _( 518 ), label2=self.settings[ "web_title" ] )
            self.getControl( self.CONTROL_WIN32_WAIT_BUTTON ).setEnabled( True )
            self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )
        return web_navigator

    def _url_launcher( self, lang, url ):
        if not url: return
        if ( not SYSTEM_PLATFORM in ( "windows", "linux", "osx" ) ):
            print "bypass: DialogSettings::_url_launcher; Unsupported platform: %s" % SYSTEM_PLATFORM
            return
        try:
            if not self.settings[ "web_navigator" ]:
                if self._set_web_navigator():
                    OK = Settings().save_settings( self.settings )
                else:
                    return

            command = None
            if ( SYSTEM_PLATFORM == "windows" ):
                command = 'start "%s" "%s"' % ( self.settings[ "web_navigator" ], url, )
            else:
                url = self.get_redirected_url( url )
                command = '%s %s' % ( self.settings[ "web_navigator" ], url, )

            if command is not None:
                if xbmcgui.Dialog().yesno( "Installer Passion-XBMC", lang, "", "", _( 237 ), _( 3 ) ):
                    os.system( command )
        except:
            print_exc()

    def _reset_settings( self ):
        """ resets values to defaults """
        self._get_settings( defaults=True )
        self._set_controls_values()
        self.getControl( self.CONTROL_OK_BUTTON ).setVisible( True )

    def _save_settings( self ):
        """ save values settings """
        OK = Settings().save_settings( self.settings )
        self.mainwin._get_settings()
        if self.rss_on_load != self.settings[ "rss_feed" ]:
            self.mainwin._start_rss_timer()
        if self.coulour_on_load != self.settings[ "skin_colours_path" ]:
            self.mainwin._set_skin_colours()
        if self.skin_on_load != self.settings.get( "current_skin", "Default.HD" ):
            #required script reload
            if xbmcgui.Dialog().yesno( _( 532 ), _( 533 ), _( 534 ) ):
                self.reload_script = True
        XBMC_SETTINGS.setSetting( "script_debug", repr( self.settings[ "script_debug" ] ).lower() )
        self._close_dialog( OK )

    def onAction( self, action ):
        try:
            last_focus = self.getFocusId()
            if last_focus in self.CONTROLS_SKIN_COLOR:
                self.last_control_colors_focused = self.CONTROLS_SKIN_COLOR
            elif last_focus in self.CONTROLS_LABELS_COLOR:
                self.last_control_colors_focused = self.CONTROLS_LABELS_COLOR
            if last_focus in [ self.CONTROL_LABELS_COLOR_LIST, self.CONTROL_SKIN_COLOR_LIST ]:
                self.synchronize_colors_controls()
        except:
            self.last_control_colors_focused = 0
            print_exc()
        #( ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_CONTEXT_MENU, )
        if action in ( 9, 10, 117 ): self._close_dialog()

    def _close_dialog( self, OK=False ):
        # verifie si l'option default a ete utilise, si oui remets l'etat du custom backgroung
        if not OK:
            if ( self.passion_show_fanart != xbmc.getCondVisibility( "!Skin.HasSetting(PassionShowFanart)" ) ):
                xbmc.executebuiltin( "Skin.ToggleSetting(PassionShowFanart)" )
            if ( self.use_custom_background != xbmc.getCondVisibility( "!Skin.HasSetting(use_passion_custom_background)" ) ):
                xbmc.executebuiltin( "Skin.ToggleSetting(use_passion_custom_background)" )
            if ( self.custom_background != unicode( xbmc.getInfoLabel( 'Skin.String(passion_custom_background)' ), 'utf-8') ):
                xbmc.executebuiltin( "Skin.SetString(passion_custom_background,%s)" % ( self.custom_background, ) )

        if "Dialog" in XBMCGUI_WINDOW_XML:
            import time
            xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
            time.sleep( .1 ) # pour les fade plus que .1 pas beau :(
        else:
            xbmc.sleep( 100 )
        self.close()
        if self.homeLastPosition is not None:
            try:
                import Home
                Home.show_home( self.homeLastPosition )
            except:
                print_exc()
        if self.reload_script:
            self.mainwin._close_script()
            sys.modules[ "__main__" ].MAIN()
        sys.modules[ "__main__" ].output.PRINT_DEBUG = ( XBMC_SETTINGS.getSetting( "script_debug" ) == "true" )



def show_settings( mainwin, homeLastPosition=None ):
    dir_path = os.getcwd().rstrip( ";" )
    file_xml = "IPX-Settings.xml"

    w = ScriptSettings( file_xml, dir_path, current_skin, force_fallback, mainwin=mainwin, homeLastPosition=homeLastPosition )
    w.doModal()
    del w
