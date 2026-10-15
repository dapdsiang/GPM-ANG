import csv
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count,Sum,Q
from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
CFG={'site':(Site,SiteForm,'Sites et bâtiments','sites'),'organisation':(Organisation,OrganisationForm,'Directions et commissions','organisations'),'room':(Room,RoomForm,'Bureaux et salles','rooms'),'equipment':(Equipment,EquipmentForm,'Équipements et inventaire','equipment'),'it':(ITAsset,ITAssetForm,'Parc informatique','it_assets'),'vehicle':(Vehicle,VehicleForm,'Parc automobile','vehicles'),'maintenance':(Maintenance,MaintenanceForm,'Maintenance et réparations','maintenance')}
LISTS={'sites':(Site,'sites.html','site'),'organisations':(Organisation,'organisations.html','organisation'),'rooms':(Room,'rooms.html','room'),'equipment':(Equipment,'equipment.html','equipment'),'it_assets':(ITAsset,'it_assets.html','it'),'vehicles':(Vehicle,'vehicles.html','vehicle'),'maintenance':(Maintenance,'maintenance.html','maintenance')}
def audit(request,action,obj): AuditLog.objects.create(utilisateur=request.user,action=action,objet=str(obj)[:180])
@login_required
def dashboard(request):
 return render(request,'patrimoine/dashboard.html',{'counts':[('Sites',Site.objects.count(),'sites'),('Directions',Organisation.objects.count(),'organisations'),('Bureaux et salles',Room.objects.count(),'rooms'),('Équipements',Equipment.objects.count(),'equipment'),('Parc informatique',ITAsset.objects.count(),'it_assets'),('Véhicules',Vehicle.objects.count(),'vehicles'),('Maintenances ouvertes',Maintenance.objects.exclude(statut__in=['terminee','annulee']).count(),'maintenance')],'categories':Equipment.objects.values('categorie').annotate(total=Count('id')).order_by('-total'),'recent':Maintenance.objects.select_related('equipment')[:6]})
@login_required
def list_page(request,key):
 model,template,kind=LISTS[key]; qs=model.objects.all(); q=request.GET.get('q','').strip()
 if q:
  cond=Q()
  for f in model._meta.fields:
   if f.get_internal_type() in ('CharField','TextField'): cond |= Q(**{f'{f.name}__icontains':q})
  qs=qs.filter(cond)
 p=Paginator(qs,25).get_page(request.GET.get('page')); return render(request,'patrimoine/'+template,{'items':p.object_list,'page_obj':p,'q':q,'title':CFG[kind][2],'kind':kind})
@login_required
def sites(request): return list_page(request,'sites')
@login_required
def organisations(request): return list_page(request,'organisations')
@login_required
def rooms(request): return list_page(request,'rooms')
@login_required
def equipment(request): return list_page(request,'equipment')
@login_required
def it_assets(request): return list_page(request,'it_assets')
@login_required
def vehicles(request): return list_page(request,'vehicles')
@login_required
def maintenance(request): return list_page(request,'maintenance')
@login_required
def create(request,kind):
 if kind not in CFG: raise Http404
 model,Form,title,route=CFG[kind]; form=Form(request.POST or None,request.FILES or None)
 if request.method=='POST' and form.is_valid(): obj=form.save(commit=False)
 else: obj=None
 if request.method=='POST' and form.is_valid():
  if kind=='maintenance': obj.cree_par=request.user
  obj.save(); form.save_m2m(); audit(request,'Création',obj); messages.success(request,'Enregistrement créé.'); return redirect(route)
 return render(request,'patrimoine/form.html',{'form':form,'title':'Ajouter — '+title,'route':route})
@login_required
def update(request,kind,pk):
 if kind not in CFG: raise Http404
 model,Form,title,route=CFG[kind]; obj=get_object_or_404(model,pk=pk); form=Form(request.POST or None,request.FILES or None,instance=obj)
 if request.method=='POST' and form.is_valid(): obj=form.save(); audit(request,'Modification',obj); messages.success(request,'Modification enregistrée.'); return redirect(route)
 return render(request,'patrimoine/form.html',{'form':form,'title':'Modifier — '+title,'route':route})
@login_required
def delete(request,kind,pk):
 if kind not in CFG: raise Http404
 model,Form,title,route=CFG[kind]; obj=get_object_or_404(model,pk=pk)
 if request.method=='POST': label=str(obj); audit(request,'Suppression',label); obj.delete(); messages.success(request,'Enregistrement supprimé.'); return redirect(route)
 return render(request,'patrimoine/delete.html',{'object':obj,'title':title,'route':route})
@login_required
def reports(request): return render(request,'patrimoine/reports.html',{'room_types':Room.objects.values('type').annotate(total=Count('id')),'cats':Equipment.objects.values('categorie').annotate(total=Count('id')),'states':Equipment.objects.values('etat').annotate(total=Count('id')),'orgs':Equipment.objects.values('organisation__nom').annotate(total=Count('id')),'vehicle_states':Vehicle.objects.values('etat_vehicule').annotate(total=Count('id')),'cost':Maintenance.objects.aggregate(total=Sum('cout'))['total'] or 0})


@login_required
def organisation_detail(request, pk):
 org=get_object_or_404(Organisation, pk=pk)
 rooms=Room.objects.filter(organisation=org).select_related('site').prefetch_related('equipements').order_by('site__nom','etage','code')
 equipment=Equipment.objects.filter(Q(organisation=org)|Q(bureau__organisation=org)).select_related('bureau','bureau__site').distinct().order_by('categorie','designation')
 occupant_count=0
 for room in rooms:
  names=[x.strip() for x in room.occupants.replace('\n', ',').split(',') if x.strip()]
  occupant_count += len(names)
 return render(request,'patrimoine/organisation_detail.html',{'organisation':org,'rooms':rooms,'equipment':equipment,'room_count':rooms.count(),'occupant_count':occupant_count,'equipment_count':equipment.count()})

@login_required
def room_detail(request, pk):
 room=get_object_or_404(Room.objects.select_related('site','organisation'),pk=pk)
 equipment=room.equipements.select_related('organisation').order_by('categorie','designation')
 occupants=[x.strip() for x in room.occupants.replace('\n', ',').split(',') if x.strip()]
 return render(request,'patrimoine/room_detail.html',{'room':room,'equipment':equipment,'occupants':occupants,'equipment_count':equipment.count(),'occupant_count':len(occupants)})
