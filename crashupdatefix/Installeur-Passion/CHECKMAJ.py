import ftplib, os
import shutil
import ConfigParser
import zipfile
import xbmc
import xbmcgui

print "****************************************************************"
print "                 Script de mise a jour auto                     "
print "****************************************************************"

class CheckMAJ:
    def __init__(self):

        self.rootdir = os.getcwd().replace(';','')

        ##############################################################################
        #                   Initialisation conf.cfg                                  #
        ##############################################################################
        self.fichier = os.path.join(self.rootdir, "conf.cfg")
        self.localConfParser = ConfigParser.ConfigParser()
        self.localConfParser.read(self.fichier)

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
        self.host        = self.localConfParser.get('ServeurID','host')
        self.user        = self.localConfParser.get('ServeurID','user')
        self.password    = self.localConfParser.get('ServeurID','password')
        self.remoteversionDir  = "/.passionxbmc/Installeur-Passion/"

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
        self.ftp = ftplib.FTP(self.host,self.user,self.password)
        self.remoteDirLst = self.ftp.nlst(self.remoteversionDir)
        
    def verifrep(self,folder):
        """
        verifrep (de myCine)
        verifie que le repertoire existe et le cree si besoin
        """
        try:
            if not os.path.exists(folder):
                os.makedirs(folder)

        except Exception, e:
            print("verifrep - Exception while creating folder " + folder)
            print(e)
            pass

    def download(self):
        """
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
        """
        self.delFiles(self.cacheDir) # on vide le cache pour etre sur d'etre plus propre

        for file in self.remoteDirLst:
        #On isole les fichiers qu'il faudra telecharger
            if file.endswith('zip'):
                self.newscript = file
            elif file.endswith('py'):
                self.installmaj = file
            elif file.endswith('cfg'):
                self.versiontodl = file

        #Telechargement du nouveau fichier de version
        print "telecharge version", self.versiontodl
        self.filetodl = self.versiontodl
        self.download()

        #Lecture des parametres du nouveau fichier de version
        print "lecture fichier"
        print 'self.completedfile = ',self.completedfile
        remoteConfParser = ConfigParser.ConfigParser()
        #self.newversionfile = open(self.completedfile,'r')
        remoteConfParser.read(self.completedfile)
        print remoteConfParser.read(self.newversionfile)
        self.newversion = remoteConfParser.get('Lastversion','lastversion')
        #print self.newversion
        #open(self.newversionfile,'r')
        #self.newversion = self.newversionfile.read()
        print self.newversion
        print self.curversion
        
        # Suppression de l'instance du config parser de remoteConf
        del remoteConfParser

        if self.newversion == self.curversion:
            print "version a jour"
            #self.config = ConfigParser.ConfigParser()
            #self.config.read(self.fichier)
            #self.config.remove_section('Lastversion')
            self.localConfParser.set("Version", "UPDATING", False)
            self.localConfParser.write(open(self.fichier,'w'))
        else:
            print "version non a jour - Demande a l'utlisateur"
            # Message a l'utilisateur pour l'update
            dialog = xbmcgui.Dialog()
            if (dialog.yesno("Installeur Passion - Mise a jour", "Une nouvelle version est disponible","Voulez vous faire une mise � jour?")):
                print "L'utilisateur a DEMANDE la mise a jour"
            
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
                print "L'utilisateur a REFUSE la mise a jour"
                self.localConfParser.set("Version", "UPDATING", False)
                self.localConfParser.write(open(self.fichier,'w'))

    def configmaj(self):
        configMAJParser = ConfigParser.ConfigParser()
        configMAJParser.add_section('Localparam')
        configMAJParser.set('Localparam', 'PassionDir', self.rootdir)
        configMAJParser.set('Localparam', 'Archive', self.archive)
        configMAJParser.set('Localparam','Scripttolaunch',self.scripttolaunch)
        configMAJParser.set("Localparam", "scriptDir", self.scriptDir)
        configMAJParser.write(open(self.confmaj,'w'))
        print "configMAJParser = ",configMAJParser
        # Suppression de configMAJParser
        del configMAJParser


    def delFiles(self,folder):
        print "Effacement des fichiers du repertoire: %s"%folder
        for root, dirs, files in os.walk(folder , topdown=False):
            for name in files:
                print "Effaccement de %s en cours ..."%name
                try:
                    os.remove(os.path.join(root, name))
                except Exception, e:
                    print e

#TODO: QUESTIOn : ne devrait t'on pas faire "self.localConfParser.write(open(self.fichier,'w'))" qu'une seule fois a la fin plutot que plusieurs fois dans le code?

def start():
    CkMAJ = CheckMAJ()
    CkMAJ.orientation()
    del CkMAJ

