
# Modules general
import os
import sys
import ftplib
from traceback import print_exc
from ConfigParser import ConfigParser

# Modules XBMC
import xbmcgui


#FONCTION POUR RECUPERER LES LABELS DE LA LANGUE.
_ = sys.modules[ "__main__" ].__language__

# variable qui peut etre modifie a partir du __main__ e.g.:
# import CHECKMAJ
# CHECKMAJ.UPDATE_STARTUP = False
# CHECKMAJ.go()
UPDATE_STARTUP = True
# print depend of output.PRINT_DEBUG is True or False
print "*" * 85
print "Automatic Update script".center( 85 )
print "*" * 85


class CheckMAJ:
    def __init__(self):

        self.rootdir = os.getcwd().replace(';','')

        ##############################################################################
        #                   Initialisation conf.cfg                                  #
        ##############################################################################
        global UPDATE_STARTUP

        self.fichier = os.path.join( sys.modules[ "__main__" ].SPECIAL_SCRIPT_DATA, "conf.cfg" )
        #self.fichier = os.path.join(self.rootdir, "resources", "conf.cfg")

        import CONF
        self.localConfParser = CONF.ReadConfig()
        ##############################################################################
        #                   Initialisation parametres locaux                         #
        ##############################################################################
        self.cacheDir   = self.localConfParser.get('InstallPath','CacheDir')
        self.scriptDir  = self.localConfParser.get('InstallPath','ScriptsDir')
        self.curversion = self.localConfParser.get('Version','version')

        ##############################################################################
        #                   Verification des repertoires et creation si besoin
        ##############################################################################
        self.verifrep(self.cacheDir)

        ##############################################################################
        #                   Initialisation parametres serveur                        #
        ##############################################################################
        self.host               = self.localConfParser.get('ServeurID','host')
        self.user               = self.localConfParser.get('ServeurID','user')
        self.password           = self.localConfParser.get('ServeurID','password')
        self.remoteversionDir   = self.localConfParser.get('ServeurID','updatescriptdir')

        self.filetodl = ""
        self.newversionfile = ""
        self.newversion = ""
        self.filedst = ""
        self.completedfile = ""
        self.versiontodl = ""
        self.confmaj = os.path.join(self.cacheDir, "confmaj.cfg")
        self.archive = ""
        self.scripttolaunch = os.path.join(self.rootdir, "default.py")

        #########################################################
        # DEMARRAGE DE LA CONNEXION                             #
        #########################################################
        if UPDATE_STARTUP:
            try:
                self.ftp = ftplib.FTP(self.host,self.user,self.password)
                self.remoteDirLst = self.ftp.nlst(self.remoteversionDir)
            except:
                print "bypass_debug: CheckMAJ - init - Exception creating CheckMAJ - cancelling update ..."
                UPDATE_STARTUP = False
                print_exc()
        else:
            self.ftp = UPDATE_STARTUP
            self.remoteDirLst = list()

    def verifrep(self,folder):
        """
        verifrep (de myCine)
        verifie que le repertoire existe et le cree si besoin
        """
        try:
            if not os.path.exists(folder):
                os.makedirs(folder)

        except:
            print "verifrep - Exception while creating folder %s" % folder
            print_exc()

    def download(self):
        """
        Fonction de telechargement commune : version, archive, script de mise a jour
        """
        self.ftp = ftplib.FTP(self.host,self.user,self.password)
        self.filedst = self.filetodl[len(self.remoteversionDir):]
        self.completedfile = os.path.join(self.cacheDir, self.filedst)
        localFile = open(str(self.completedfile), "wb")
        self.ftp.retrbinary('RETR ' + self.filetodl, localFile.write)
        localFile.close()
        self.ftp.quit()

    def orientation(self):
        """
        Oriente le script vers une mise a jour ou non
        """
        self.delFiles(self.cacheDir) # on vide le cache pour etre sur d'etre plus propre

        if UPDATE_STARTUP:
            for file in self.remoteDirLst:
                #On isole les fichiers qu'il faudra telecharger
                if file.endswith('zip'):
                    self.newscript = self.remoteversionDir + file
                elif file.endswith('py'):
                    self.installmaj = self.remoteversionDir + file
                elif file.endswith('cfg'):
                    self.versiontodl = self.remoteversionDir + file
                #print self.remoteversionDir + file

            #Telechargement du nouveau fichier de version
            self.filetodl = self.versiontodl
            self.download()

            #Lecture des parametres du nouveau fichier de version
            remoteConfParser = ConfigParser()
            remoteConfParser.read(self.completedfile)
            self.newversion = remoteConfParser.get('Lastversion','lastversion')

            # Suppression de l'instance du config parser de remoteConf
            del remoteConfParser
        else:
            self.newversion = self.curversion

        if self.newversion == self.curversion:
            #version a jour
            self.localConfParser.set("Version", "UPDATING", False)
            self.localConfParser.write(open(self.fichier,'w'))
        else:
            # version non a jour - Demande a l'utlisateur
            # Message a l'utilisateur pour l'update
            dialog = xbmcgui.Dialog()
            if dialog.yesno( _( 0 ), _( 105 ), _( 106 ) ):

                #Telechargement de la nouvelle archive
                self.filetodl = self.newscript
                self.download()
                self.archive = self.completedfile
                #Telechargement du script d'extraction
                self.filetodl = self.installmaj
                self.download()
                scriptmaj = self.completedfile

                self.localConfParser.set("Version", "UPDATING", True)
                self.localConfParser.set("Version", "scriptMAJ", scriptmaj)
                self.localConfParser.write(open(self.fichier,'w'))
                self.configmaj()
            else:
                #L'utilisateur a REFUSE la mise a jour
                self.localConfParser.set("Version", "UPDATING", False)
                self.localConfParser.write(open(self.fichier,'w'))

    def configmaj(self):
        """
        Creation du fichier de conf qui servira au script de mise a jour
        """
        configMAJParser = ConfigParser()
        configMAJParser.add_section('Localparam')
        configMAJParser.set('Localparam', 'PassionDir', self.rootdir)
        configMAJParser.set('Localparam', 'Archive', self.archive)
        configMAJParser.set('Localparam','Scripttolaunch',self.scripttolaunch)
        configMAJParser.set("Localparam", "scriptDir", self.scriptDir)
        configMAJParser.write(open(self.confmaj,'w'))
        # Suppression de l'instance de configMAJParser
        del configMAJParser


    def delFiles(self,folder):
        for root, dirs, files in os.walk(folder , topdown=False):
            for name in files:
                print "bypass_debug: Effaccement de %s en cours ..." % name
                try:
                    os.remove(os.path.join(root, name))
                except:
                    print_exc()

#TODO: QUESTION : ne devrait t'on pas faire "self.localConfParser.write(open(self.fichier,'w'))" qu'une seule fois a la fin plutot que plusieurs fois dans le code?

def go():
    CkMAJ = CheckMAJ()
    CkMAJ.orientation()
    del CkMAJ

