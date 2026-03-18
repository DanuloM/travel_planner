from django.db import models

# Create your models here.
class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Place(models.Model):
    project = models.ForeignKey(TravelProject, related_name='places', on_delete=models.CASCADE)
    external_id = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    is_visited = models.BooleanField(default=False)

    def __str__(self):
        return f"Place {self.external_id} in {self.project.name}"