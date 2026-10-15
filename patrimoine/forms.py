from django import forms
from .models import Site,Organisation,Room,Equipment,ITAsset,Vehicle,Maintenance
class StyledForm(forms.ModelForm):
 def __init__(self,*a,**kw):
  super().__init__(*a,**kw)
  for f in self.fields.values(): f.widget.attrs['class']='form-control'
class SiteForm(StyledForm):
 class Meta: model=Site; fields='__all__'
class OrganisationForm(StyledForm):
 class Meta: model=Organisation; fields='__all__'
class RoomForm(StyledForm):
 class Meta: model=Room; fields='__all__'
class EquipmentForm(StyledForm):
 class Meta: model=Equipment; fields='__all__'
class ITAssetForm(StyledForm):
 class Meta: model=ITAsset; fields='__all__'
class VehicleForm(StyledForm):
 class Meta: model=Vehicle; fields='__all__'
class MaintenanceForm(StyledForm):
 class Meta: model=Maintenance; fields='__all__'
