from django.db import models
from django.forms import ModelForm, Textarea
from django import forms


# Create your models here.
#
#
#

class DBUpdate(models.Model):
  lastUpdDate = models.DateTimeField('date updated')
  
  def __str__(self):
    return 'lastDbUpdate' 

  
  class Admin:
    pass

class Branch(models.Model):
  branch_name  = models.CharField(max_length=50, unique=True)
  bfr_id       = models.IntegerField()

  class Meta:
    verbose_name_plural = "Branches"
    ordering = ["branch_name"]

  def __str__(self):
    return self.branch_name

  class Admin:
    pass

class Lvn_entry(models.Model):
  lvn             = models.IntegerField()
  branch_name     = models.ForeignKey(Branch,to_field='branch_name')
  rev_id          = models.IntegerField(unique=True) 
  src_dir_change  = models.IntegerField()
  h_file_change   = models.IntegerField()
  inc_file_change = models.IntegerField()
  layout_check    = models.IntegerField(null=True)
  layout_done     = models.IntegerField()
  layout_status   = models.IntegerField(null=True) 
  md5sum_str      = models.CharField(max_length=50, null=True)
  commit_date     = models.DateTimeField('date commit')
  author          = models.CharField(max_length=10)
  layout_rev      = models.IntegerField()

  class Meta:
    verbose_name_plural = "Lvn_entries"

  def __unicode__(self):
    return u'lvn %s:%s' % (self.branch_name, self.lvn)
  def __string__(self):
    return '%s:%s' % (self.lvn, self.branch_name)


  def __slvn__(self):
    return self.lvn
  def __sbranch__(self):
    return self.branch_name
 
  class Admin:
    pass
 
class Wiki_entry(models.Model):
  bfr_lvn         = models.CharField(max_length=12)
  branch_name     = models.ForeignKey(Branch,to_field='branch_name')
  rev_id          = models.IntegerField() 
  author          = models.CharField(max_length=15)
  adaptation      = models.CharField(max_length=500, null=True, default='-', blank=True)
  other           = models.CharField(max_length=500, null=True, default='-', blank=True) 
  title           = models.FileField(upload_to='wikitabledocs/', null=True)#, blank=True)

  class Meta:
    verbose_name_plural = "Wiki_entries"

  def __unicode__(self):
    return u'Wiki_%s:%s' % (self.branch_name, self.bfr_lvn)
  def __string__(self):
    return 'Wiki_%s:%s' % (self.bfr_lvn, self.branch_name)


  def __sbfrlvn__(self):
    return self.bfr_lvn
  def __sbranch__(self):
    return self.branch_name
 
  class Admin:
    pass

class Wiki_form(ModelForm):
    class Meta:
        model = Wiki_entry
        exclude = ('bfr_lvn','rev_id','author','adaptation','other', 'title')

class Wiki_insert_form(ModelForm):
    class Meta:
        model = Wiki_entry
        exclude = ('branch_name')
        widgets = {
			'bfr_lvn': Textarea(attrs={'cols':10, 'rows':1}),
			'rev_id': Textarea(attrs={'cols':8, 'rows':1}),
			'author': Textarea({'cols':5, 'rows':1}),
			'adaptation': Textarea({'cols':20, 'rows':10}),
			'other': Textarea({'cols':20,'rows':10}),
        }


class Wikientry(ModelForm):
    delete_box = forms.BooleanField()
    update_box = forms.BooleanField()
    class Meta:
        model = Wiki_entry
        fields=('bfr_lvn', 'rev_id', 'author', 'adaptation', 'other')
        ordering = ["-rev_id", "-bfr_lvn"]
        widgets = {
			'bfr_lvn': Textarea(attrs={'cols':10, 'rows':1, 'readonly':"readonly"}),
			'rev_id': Textarea(attrs={'cols':8, 'rows':1, 'readonly':"readonly"}),
			'author': Textarea({'cols':8, 'rows':1, 'readonly':"readonly"}),
			'adaptation': Textarea({'cols':25,'rows':2, 'readonly':"readonly",'style':'width:535px;height:114px;'}),
                        'other':Textarea({'cols':25,'rows':2, 'readonly':"readonly",'style':'width:300px;height:114px;'}),
        }
class Wikientryresp(ModelForm):
    delete_file = forms.BooleanField()
    class Meta:
        model = Wiki_entry
        fields=('bfr_lvn', 'rev_id', 'author', 'adaptation', 'other', 'title')
        ordering = ["-rev_id", "-bfr_lvn"]
        widgets = {
			'bfr_lvn': Textarea(attrs={'cols':10, 'rows':1}),
			'rev_id': Textarea(attrs={'cols':8, 'rows':1}),
			'author': Textarea({'cols':8, 'rows':1}),
			'adaptation': Textarea({'cols':25,'rows':2,'style':'width:535px;height:114px;'}),
            'other':Textarea({'cols':25,'rows':2,'style':'width:300px;height:114px;'}),
        }
class LVN_Feature_Related(models.Model):
 # branch_name     = models.ForeignKey(Branch,to_field='branch_name')
    rev_id                   = models.IntegerField() 
    lvn                      = models.IntegerField()
    feature                  = models.CharField(max_length=100)
    team                     = models.CharField(max_length=35)
    affected_structures      = models.CharField(max_length=500)
    other                    = models.CharField(max_length=500) 
    title                    = models.FileField(upload_to='documents/', null=True)

    class Meta:   
        verbose_name_plural = "LVN_Feature_Related_Entries"
    def __string__(self):
		return 'LVN_Feature_%s:%s:%s' % (self.feature, self.team, self.rev_id)
    def __unicode__(self):
        return u'LVN_Feature_%s:%s:%s' % (self.feature, self.team, self.rev_id) 

    class Admin:
        pass

class LVNFeature(ModelForm):
    delete_box = forms.BooleanField()
    update_box = forms.BooleanField()
    class Meta:
        model =LVN_Feature_Related
        fields=('rev_id', 'lvn', 'feature', 'team', 'affected_structures', 'other')
        ordering = ["-feature", "-rev_id", "-lvn"]
        widgets = {
            'lvn': Textarea(attrs={'cols':5, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
            'rev_id': Textarea(attrs={'cols':8, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
            'feature': Textarea(attrs={'cols':15, 'rows':1, 'readonly':"readonly",'style':'width:217px;height:30px;'}),
            'team': Textarea(attrs={'cols':10, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
            'affected_structures': Textarea(attrs={'cols':25,'rows':3, 'readonly':"readonly",'style':'width:371px;height:90px;'}),
            'other': Textarea(attrs={'cols':25,'rows':3, 'readonly':"readonly",'style':'width:370px;height:90px;'}),
        }
class LVNFeatureresp(ModelForm):
    delete_file = forms.BooleanField()
    class Meta:
        model =LVN_Feature_Related
        fields=('rev_id', 'lvn', 'feature', 'team', 'affected_structures', 'other', 'title')
        ordering = ["-feature", "-rev_id", "-lvn"]
        widgets = {
            'lvn': Textarea(attrs={'cols':5, 'rows':1,'style':'height:22px;'}),
            'rev_id': Textarea(attrs={'cols':8, 'rows':1,'style':'height:22px;'}),
            'feature': Textarea(attrs={'cols':15, 'rows':1,'style':'width:217px;height:30px;'}),
            'team': Textarea(attrs={'cols':10, 'rows':1,'style':'height:22px;'}),
            'affected_structures': Textarea(attrs={'cols':25,'rows':3,'style':'width:371px;height:90px;'}),
            'other': Textarea(attrs={'cols':25,'rows':3,'style':'width:370px;height:90px;'}),
        }

class Uploaded_Files(models.Model):
    title = models.FileField(upload_to='documents/')
    rev_id = models.IntegerField(null=True)

class ISU_working_path(models.Model):
    TYPES_OF  = (('RU', 'RU'), ('ISU','ISU'),)
    SUCCESS   = (('Y','Yes'), ('N', 'No'),) 
    src_iso               = models.CharField(max_length=100)
    src_build_name        = models.CharField(max_length=10)
    src_branch_name       = models.ForeignKey(Branch, to_field='branch_name', related_name='src_branch_name')
    trg_iso               = models.CharField(max_length=100)
    trg_build_name        = models.CharField(max_length=10)
    trg_branch_name       = models.ForeignKey(Branch, to_field='branch_name', related_name='trg_branch_name')
    tester                = models.CharField(max_length=30)
    test_date             = models.DateField('date updated')
    success               = models.CharField(max_length=4, choices=SUCCESS, default='N')     
    type_of               = models.CharField(max_length=4, choices=TYPES_OF)     
    result_file           = models.FileField(upload_to='documents/', null=True)

    class Meta:
        verbose_name_plural = "ISU_working_paths"

    def __unicode__(self):
        return u'ISU_%s_%s_To_%s_%s' % (self.src_branch_name, self.src_build_name, self.trg_branch_name, self.trg_build_name)
    def __string__(self):
        return 'ISU_%s_%s_To_%s_%s' % (self.src_branch_name, self.src_build_name, self.trg_branch_name, self.trg_build_name)

    class Admin:
        pass

class ISUFeature(ModelForm):
    delete_box = forms.BooleanField()
    update_box = forms.BooleanField()
    class Meta:
        model =ISU_working_path
        fields=('src_iso', 'src_build_name', 'src_branch_name', 'trg_iso', 'trg_build_name', 'trg_branch_name', 'tester', 'test_date', 'success', 'type_of', 'result_file')
        ordering = ["-test_date", "tester"]
        widgets = {
            'src_iso': Textarea(attrs={'cols':20, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
            'src_build_name': Textarea(attrs={'cols':8, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
            'src_branch_name': Textarea(attrs={'cols':10, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
            'trg_iso': Textarea(attrs={'cols':20, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
            'trg_build_name': Textarea(attrs={'cols':8, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
            'trg_branch_name': Textarea(attrs={'cols':10, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
            'tester': Textarea(attrs={'cols':8, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
            'test_date': Textarea(attrs={'cols':15, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
        }

class ISUresp(ModelForm):
    delete_file = forms.BooleanField()

    class Meta:
        model =ISU_working_path
        fields=('src_iso', 'src_build_name', 'src_branch_name', 'trg_iso', 'trg_build_name', 'trg_branch_name', 'tester', 'test_date', 'success', 'type_of', 'result_file')
        ordering = ["-test_date", "tester"]
        widgets = {
            'src_iso': Textarea(attrs={'cols':20, 'rows':1, 'style':'height:22px;'}),
            'src_build_name': Textarea(attrs={'cols':8, 'rows':1, 'style':'height:22px;'}),
            'src_branch_name': Textarea(attrs={'cols':10, 'rows':1, 'style':'height:22px;'}),
            'trg_iso': Textarea(attrs={'cols':20, 'rows':1, 'style':'height:22px;'}),
            'trg_build_name': Textarea(attrs={'cols':8, 'rows':1, 'style':'height:22px;'}),
            'trg_branch_name': Textarea(attrs={'cols':10, 'rows':1, 'style':'height:22px;'}),
            'tester': Textarea(attrs={'cols':8, 'rows':1, 'style':'height:22px;'}),
            'test_date': Textarea(attrs={'cols':15, 'rows':1, 'readonly':"readonly",'style':'height:22px;'}),
        }


class ISU_path_insert_form(ModelForm):
    src_branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label='')
    trg_branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label='')  
    class Meta:
        model = ISU_working_path
        exclude = ('src_branch_name', 'trg_branch_name') 
        widgets = {
            'src_iso': Textarea(attrs={'cols':30, 'rows':1, 'style':'height:22px;'}),
            'src_build_name': Textarea(attrs={'cols':10, 'rows':1, 'style':'height:22px;'}),
            'trg_iso': Textarea(attrs={'cols':30, 'rows':1, 'style':'height:22px;'}),
            'trg_build_name': Textarea(attrs={'cols':10, 'rows':1, 'style':'height:22px;'}),
            'tester': Textarea(attrs={'cols':8, 'rows':1, 'style':'height:22px;'}),
        }



