from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

num_only = RegexValidator(r'^[0-9]*$','only numbers are allowed')
role_choices = [
    ('Citoyen','Citoyen'),
    ('Admin','Admin'),
    ('Agent','Agent'),
    ('Association','Association'),
    ('Entrepreneur','Entrepreneur'),
]
topic_choices = [
    ('Sportif','Sportif'),
    ('Culturel','Culturel'),
    ('Audiance','Audiance'),
    ('Economique','Economique'),
]
activity_choices = [
    ('Politique','Politique'),
    ('Economique','Economique'),
]
accomagnement_choises = [
    ('Economique','Economique'),
    ('Politique', 'Politique'),

]
state_choices = [
    ('en traitement','en traitement'),
    ('validé','validé'),
    ('refusé','refusé'),
]
ecological_info_choices = [
    ('sensibilisation','sensibilisation'),
    ('valorisation','valorisation'),
]
product_action_choices = [
    ('Vente','Vente'),
    ('Echange','Echange'),
    ('Allocation','Allocation')
]
discussion_choices = [
    ('Politique','Politique'),
    ('Economique','Economique'),
    ('Danger','Danger'),
]
danger_types = [
    ('Alerte','Alerte'),
    ('Information','Information')
]
formation_types = [
    ('Social','Social'),
    ('Economique','Economique')
]
emergency_types = [
    ('Gaz','Gaz'),
    ('Incendie','Incendie')
]
actuality_types = [
    ('Realisation','Realisation'),
    ('Education','Education'),
    ('Entreprise','Entreprise'),
    ('Sport','Sport')
]

class Wilaya(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __str__(self) -> str:
        return self.name

class Commune(models.Model):
    name = models.CharField(max_length=20, null=False)
    wilaya = models.ForeignKey(Wilaya,related_name='communes',on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name+'_'+self.wilaya.name


class User(AbstractUser):

    phone = models.CharField(max_length=10 , validators=[num_only],blank=True,null=True)
    image = models.ImageField(upload_to='profile_images/', blank = True , null = True , verbose_name='user_img')
    role =  models.CharField(max_length=15 , choices=role_choices , default='Citoyen')
    otp = models.CharField(max_length=6, null=True, blank=True)
    commune = models.PositiveIntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True,blank=True)
    social_approved = models.BooleanField(default=False)
    document = models.ImageField(upload_to='profile_images/', blank = True , null = True , verbose_name='user_img')
    
    def __str__(self) -> str:
        return self.first_name+' '+self.last_name

class BaseModel(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class Formation(BaseModel): 
    owner = models.ForeignKey(User, related_name='formations', on_delete=models.CASCADE, null=False)  
    date = models.DateTimeField()
    localisation = models.CharField(max_length=50)
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')
    type = models.CharField(max_length=15, choices=formation_types, null=True, blank=True)#non null
    def __str__(self) -> str:
        return f'{self.owner} {self.title}'

class Accompagnement(BaseModel):
    owner = models.ForeignKey(User, related_name='accompagnements', on_delete=models.CASCADE, null=False)
    image = models.ImageField(null=True, blank=True, upload_to='accompagnements_images')
    type = models.CharField(max_length=15, choices=accomagnement_choises,null=True, blank=True) #non null
    def __str__(self) -> str:
        return f'{self.owner} {self.title}'

class Topic(BaseModel):
    owner = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE, null=False)
    image = models.ImageField(null=True, blank=True, upload_to='topics_images')
    type = models.CharField(max_length=15,choices=topic_choices, null=True, blank=True) #non null
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')
    def __str__(self) -> str:
        return f'{self.owner} {self.title}'


class Discussion(BaseModel):
    owner = models.ForeignKey(User, related_name='discussions', on_delete=models.CASCADE, null=False)
    image = models.ImageField(null=True, blank=True, upload_to='discussion_images')
    type = models.CharField(max_length=15,choices=discussion_choices)
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')

    def __str__(self) -> str:
        return f'{self.owner} {self.title}'
        

class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE)
    content = models.TextField(max_length=300, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    discussion = models.ForeignKey(Discussion, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.owner} {self.topic}'

class Activity(BaseModel):
    owner = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE, null=False)
    directed_by = models.CharField(max_length=50)
    date = models.DateTimeField()
    type = models.CharField(max_length=15,choices=activity_choices,null=True,blank=True)
    
    def __str__(self) -> str:
        return f'{self.owner} {self.title}'

class EcologicalInformation(BaseModel):
    owner = models.ForeignKey(User, related_name='ecological_informations', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='ecological_infos_images')
    type = models.CharField(max_length=15, choices=ecological_info_choices)
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')

    def __str__(self) -> str:
        return f'{self.owner} {self.title}'

class Product(models.Model):
    owner = models.ForeignKey(User, related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=False, blank=True)
    price = models.IntegerField()
    image = models.ImageField(null=True, blank=True, upload_to='products_images')
    action_type = models.CharField(max_length=15,choices=product_action_choices)
    created_at = models.DateTimeField(auto_now_add=True)

class AudianceDemand(BaseModel):
    owner = models.ForeignKey(User, related_name='audiance_demands', on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    person = models.CharField(max_length=50, blank=True)  # Make the person field optional
    state = models.CharField(max_length=20, choices=state_choices, default='en traitement')


class Agenda(BaseModel):
    owner = models.ForeignKey(User, related_name='agendas', on_delete=models.CASCADE, null=False)
    date = models.DateTimeField()
    localisation = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to='agenda_images')
    def __str__(self) -> str:
        return f'{self.owner} {self.title}'

class SocialInformation(BaseModel):
    owner = models.ForeignKey(User, related_name='social_informations', on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f'{self.owner} {self.title}'

class DangerInformation(BaseModel):
    owner = models.ForeignKey(User, related_name='danger_informations', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='ecological_infos_images')
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')
    type = models.CharField(max_length=15, choices=danger_types)

    def __str__(self) -> str:
        return f'{self.owner} {self.title}'

class Visite(BaseModel):
    owner = models.ForeignKey(User, related_name='visits', on_delete=models.CASCADE)
    localisation = models.CharField(max_length=50)
    commune = models.IntegerField()
    image = models.ImageField(null=True, blank=True, upload_to='visites_images')
    liked_by = models.ManyToManyField(User, blank=True)  # Allow an empty liked_by list
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')

    def __str__(self) -> str:
        return f'{self.owner} {self.title}'

class Album(models.Model):
    image = models.ImageField(upload_to='visites_images')
    name = models.CharField(max_length=50)
    commune = models.IntegerField()
    owner = models.ForeignKey(User, related_name='albums', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, blank=True)
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')

    def __str__(self) -> str:
        return f'{self.name} {self.owner}'


class Historique(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    commune = models.IntegerField()
    owner = models.ForeignKey(User,related_name='historique', on_delete=models.CASCADE)
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')

    def __str__(self):
        return self.title


class EmergencyFunctions(BaseModel):
    owner = models.ForeignKey(User, related_name='emergency_functions', on_delete=models.CASCADE)
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')
    type = models.CharField(max_length=20, choices=emergency_types)

    def __str__(self) -> str:
        return f'{self.owner} {self.title}'

class Actuality(BaseModel):
    owner = models.ForeignKey(User, related_name='actualities', on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    file = models.FileField(upload_to='videos/', null=True, blank=True)
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')
    type = models.CharField(max_length=20,choices=actuality_types)

    def __str__(self) -> str:
        return f'{self.title} {self.owner}'

class Study(BaseModel):
    owner = models.ForeignKey(User, related_name='studies', on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=20,choices=state_choices,default='en traitement')

    def __str__(self) -> str:
        return f'{self.title} {self.owner}'

class Survey(BaseModel):
    owner = models.ForeignKey(User, related_name='surveys', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title} {self.owner}'
    
class Choice(models.Model):
    name = models.CharField(max_length=50)
    votes_number = models.PositiveIntegerField()
    survey = models.ForeignKey(Survey, related_name='choices', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.survey.title} {self.name}'

class CompanyCreation(BaseModel):
    owner = models.ForeignKey(User, related_name='companies_creation', on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f'{self.owner} {self.title}'