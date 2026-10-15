from django.db import models
from django.conf import settings
from django.utils import timezone
class Site(models.Model):
 nom=models.CharField(max_length=120,unique=True); adresse=models.CharField(max_length=255,blank=True); description=models.TextField(blank=True)
 def __str__(self): return self.nom

 class Meta: ordering=['nom']; verbose_name='Site / bâtiment'; verbose_name_plural='Sites et bâtiments'

class Organisation(models.Model):
 TYPES=[('direction','Direction'),('commission','Commission'),('service','Service'),('autre','Autre')]
 nom=models.CharField(max_length=160,unique=True); type=models.CharField(max_length=20,choices=TYPES,default='direction'); responsable=models.CharField(max_length=160,blank=True); telephone=models.CharField(max_length=40,blank=True)
 def __str__(self): return self.nom

class Room(models.Model):
 TYPES=[('bureau','Bureau'),('reunion','Salle de réunion'),('conference','Salle de conférence'),('stockage','Stockage'),('autre','Autre')]
 site=models.ForeignKey(Site,on_delete=models.PROTECT,related_name='locaux'); code=models.CharField(max_length=40); nom=models.CharField(max_length=160); type=models.CharField(max_length=20,choices=TYPES,default='bureau'); etage=models.CharField(max_length=30,blank=True); capacite=models.PositiveIntegerField(default=1); organisation=models.ForeignKey(Organisation,on_delete=models.SET_NULL,null=True,blank=True); occupants=models.TextField(blank=True); notes=models.TextField(blank=True)

 class Meta: constraints=[models.UniqueConstraint(fields=['site','code'],name='unique_room_code_site')]; ordering=['site','etage','code']
 def __str__(self): return f'{self.code} — {self.nom}'

class Equipment(models.Model):
 CATS=[('informatique','Informatique'),('audiovisuel','Audiovisuel'),('mobilier','Mobilier'),('climatisation','Climatisation'),('electrique','Électrique'),('roulant','Engin roulant'),('autre','Autre')]
 STATES=[('neuf','Neuf'),('bon','Bon état'),('moyen','État moyen'),('panne','En panne'),('reforme','À réformer'),('perdu','Perdu / introuvable')]
 code_inventaire=models.CharField(max_length=80,unique=True); designation=models.CharField(max_length=180); categorie=models.CharField(max_length=20,choices=CATS,default='autre'); marque=models.CharField(max_length=100,blank=True); modele=models.CharField(max_length=100,blank=True); numero_serie=models.CharField(max_length=120,blank=True); date_acquisition=models.DateField(null=True,blank=True); valeur=models.DecimalField(max_digits=14,decimal_places=2,null=True,blank=True); etat=models.CharField(max_length=20,choices=STATES,default='bon'); bureau=models.ForeignKey(Room,on_delete=models.SET_NULL,null=True,blank=True,related_name='equipements'); organisation=models.ForeignKey(Organisation,on_delete=models.SET_NULL,null=True,blank=True); responsable=models.CharField(max_length=160,blank=True); description=models.TextField(blank=True); photo=models.ImageField(upload_to='equipements/',blank=True,null=True); created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return f'{self.code_inventaire} — {self.designation}'

class ITAsset(models.Model):
 TYPES=[('ordinateur','Ordinateur'),('portable','Portable'),('imprimante','Imprimante'),('serveur','Serveur'),('reseau','Réseau'),('telephone','Téléphone'),('autre','Autre')]
 equipment=models.OneToOneField(Equipment,on_delete=models.CASCADE,related_name='informatique'); type_materiel=models.CharField(max_length=20,choices=TYPES,default='ordinateur'); systeme_exploitation=models.CharField(max_length=100,blank=True); nom_machine=models.CharField(max_length=100,blank=True); adresse_ip=models.GenericIPAddressField(null=True,blank=True); adresse_mac=models.CharField(max_length=40,blank=True); fin_garantie=models.DateField(null=True,blank=True); logiciels=models.TextField(blank=True)
 def __str__(self): return str(self.equipment)

class Vehicle(models.Model):
 STATES=[('disponible','Disponible'),('affecte','Affecté'),('maintenance','En maintenance'),('immobilise','Immobilisé'),('reforme','Réformé')]
 equipment=models.OneToOneField(Equipment,on_delete=models.CASCADE,related_name='vehicule'); immatriculation=models.CharField(max_length=40,unique=True); chassis=models.CharField(max_length=100,blank=True); type_vehicule=models.CharField(max_length=80,blank=True); kilometrage=models.PositiveIntegerField(default=0); carburant=models.CharField(max_length=30,blank=True); conducteur=models.CharField(max_length=160,blank=True); etat_vehicule=models.CharField(max_length=20,choices=STATES,default='disponible'); assurance_expiration=models.DateField(null=True,blank=True); visite_expiration=models.DateField(null=True,blank=True)
 def __str__(self): return f'{self.immatriculation} — {self.equipment}'

class Maintenance(models.Model):
 TYPES=[('preventive','Préventive'),('corrective','Corrective'),('reparation','Réparation'),('controle','Contrôle'),('autre','Autre')]; STATES=[('ouverte','Ouverte'),('cours','En cours'),('terminee','Terminée'),('annulee','Annulée')]
 equipment=models.ForeignKey(Equipment,on_delete=models.CASCADE,related_name='maintenances'); type=models.CharField(max_length=20,choices=TYPES,default='corrective'); statut=models.CharField(max_length=20,choices=STATES,default='ouverte'); date_signalement=models.DateField(default=timezone.localdate); date_intervention=models.DateField(null=True,blank=True); prestataire=models.CharField(max_length=180,blank=True); cout=models.DecimalField(max_digits=14,decimal_places=2,null=True,blank=True); kilometrage=models.PositiveIntegerField(null=True,blank=True); description_panne=models.TextField(); travaux_effectues=models.TextField(blank=True); prochaine_maintenance=models.DateField(null=True,blank=True); cree_par=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
 def __str__(self): return f'{self.equipment} — {self.date_signalement}'

class AuditLog(models.Model):
 utilisateur=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True); action=models.CharField(max_length=100); objet=models.CharField(max_length=180,blank=True); details=models.TextField(blank=True); date_action=models.DateTimeField(auto_now_add=True)

 class Meta: ordering=['-date_action']
