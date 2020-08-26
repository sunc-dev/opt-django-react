from django.db import models
import uuid


# Create your models here.
class Endpoints(models.Model):
    '''The endpoint model represents the ILP API endpoint'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now=True, blank=True)


class Algorithms(models.Model):
    ''' The ILP algorithm model represents ILP algorithm object,
    the object shows descriptive information about our ILP algorithms '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    algorithm_name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoints, on_delete=models.CASCADE)


class AlgorithmStatus(models.Model):
    ''' The ILP algorithm status objects
    represents the status of the given ILP algorithm '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=128)
    active = models.BooleanField()
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_algorithm = models.ForeignKey(Algorithms,
                                         on_delete=models.CASCADE,
                                         related_name="status")


class Requests(models.Model):
    ''' The ILP request object will keep all information
     related to requests against the ILP algorithm. Helps track
     requests sent to the model.'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.CharField(max_length=10000)
    full_response = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    feedback = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_algorithm = models.ForeignKey(Algorithms, on_delete=models.CASCADE)


class ModelConstraints(models.Model):
    ''' The model constraints object will be
    the request body that stores constraint inputs of the ILP model '''
    class Meta:
        verbose_name_plural = "Model constraints"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    proximity = models.DecimalField(max_digits=12, decimal_places=2)
    endangerment = models.DecimalField(max_digits=12, decimal_places=2)
    trees = models.DecimalField(max_digits=12, decimal_places=2)
    water = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.DecimalField(max_digits=12, decimal_places=2)
