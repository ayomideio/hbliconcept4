from django.db import models
from django.db.models.fields import CharField

# Create your models here.
# "label": "icobbfhfhv", "icon": "pi pi-fw pi-align-left",
    
#     "items": [
#         {
#             "label": "ICONCEPT4FDNFDKN", "icon": "pi pi-fw pi-align-left",
#             "items": [
#                 {
#                     "label": "Submenu 1.1", "icon": "pi pi-fw pi-align-left",
#                     "items": [
#                         { "label": "Submenu 1.1.1", "icon": "pi pi-fw pi-align-left" },
#                         { "label": "Submenu 1.1.2", "icon": "pi pi-fw pi-align-left" },
#                         { "label": "Submenu 1.1.3", "icon": "pi pi-fw pi-align-left" }
#                     ]
#                 },
#                 {
#                     "label": "Submenu 1.2", "icon": "pi pi-fw pi-align-left",
#                     "items": [
#                         { "label": "Submenu 1.2.1", "icon": "pi pi-fw pi-align-left" },
#                         { "label": "Submenu 1.2.2", "icon": "pi pi-fw pi-align-left" }
#                     ]
#                 }
#             ]
#         },
class ic4promenus(models.Model):
    class Meta:
        db_table='IC4PROMENUSSSS'
    id=models.IntegerField(primary_key=True)
    label=models.CharField(max_length=30)
    icon=models.CharField(max_length=20)
    items=models.TextField()
    father=models.CharField(max_length=30)
    ic4proLanguage=models.CharField(max_length=3)
