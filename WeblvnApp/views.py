# Create your views here.
from django.template import Context,loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
#from Weblvn.WeblvnApp.models import Lvn_entry
#from Weblvn.WeblvnApp.models import Wiki_entry
#from Weblvn.WeblvnApp.models import Wikientry
from django import forms
from django.db.models import Q
from models import *
import subprocess
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions.models import Session
from django.core.context_processors import csrf
from django.template import RequestContext
from django.forms.models import modelformset_factory
#from django.core.context_processors import csrf
import re
import os
import time
import sys
from django.http import Http404
from Weblvn import settings
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

class UploadFileForm(forms.Form):

    my_title = forms.FileField(label='Select a file to upload',help_text='max. 5 megabytes')
    

def insert_and_upload(request):

    d = {}
    d.update(csrf(request))

    if request.method == 'POST':

        if 'my_title' in request.FILES.keys():
            
            arg_title = request.FILES['my_title']#arg_title is an UploadedFile object,thus has some useful methods...
            print 'File to upload is:------------>',arg_title.name
           
            my_lvn = request.POST.get('lvn','')
            my_rev = request.POST.get('rev_id','')
            my_team = request.POST.get('team','')
            my_feature = request.POST.get('feature','')
            my_other = request.POST.get('other','')
            my_affected_structures = request.POST.get('affected_structures','')

            if len(my_rev)==0 or not is_number(my_rev):
                return render_to_response('message.html',{'msg': 'Revision field must be a valid number','return_to':'/insert_LVN_feature_entry/'})  
            elif not is_number(my_lvn):
                return render_to_response('message.html',{'msg': 'LVN must be a valid number','return_to':'/insert_LVN_feature_entry/'})  
            else:
                new_lvn_feature_entry = LVN_Feature_Related(lvn=my_lvn,rev_id=my_rev,team=my_team,feature=my_feature,other=my_other,affected_structures=my_affected_structures, title=arg_title)
        
                new_lvn_feature_entry.save()


            return HttpResponseRedirect('/feature_related_table/')


        elif 'my_title' not in request.FILES.keys():
            
            my_lvn = request.POST.get('lvn','')
            my_rev = request.POST.get('rev_id','')
            my_team = request.POST.get('team','')
            my_feature = request.POST.get('feature','')
            my_other = request.POST.get('other','')
            my_affected_structures = request.POST.get('affected_structures','')

            if len(my_rev)==0 or not is_number(my_rev):
                return render_to_response('message.html',{'msg': 'Revision field must be a valid number','return_to':'/insert_LVN_feature_entry/'})  
            elif not is_number(my_lvn):
                return render_to_response('message.html',{'msg': 'LVN must be a valid number','return_to':'/insert_LVN_feature_entry/'})  
            else:
                new_lvn_feature_entry = LVN_Feature_Related(lvn=my_lvn,rev_id=my_rev,team=my_team,feature=my_feature,other=my_other,affected_structures=my_affected_structures)
        
                new_lvn_feature_entry.save()
            return HttpResponseRedirect('/feature_related_table/')
        else:

            print 'Dont know what brought us here'
 

    else:

        uploadform = UploadFileForm() #an empty unbound form for file uploading
       
        form = LVNFeatureresp()#an empty unbound form also for feature related uploading(integers,chars)

    files = Uploaded_Files.objects.all()


    return render_to_response('insert_LVN_feature_entry.html',{'files':files,'form':form,'uploadform':uploadform}, context_instance=RequestContext(request))#last field is needed for csrf authentication



def handle_uploaded_file(request):
    d = {}
    d.update(csrf(request))
    

    if request.method == 'POST':
        arg_title = request.FILES['my_title']#arg_title is an UploadedFile object,thus has some useful methods...
        print 'File to upload is:------------>',arg_title.name
        newfile = Uploaded_Files(title = arg_title)
        newfile.save()
        return HttpResponseRedirect('/handle_uploaded_file/')

    else:

        form = UploadFileForm() #an empty unbound form

    files = Uploaded_Files.objects.all()


    return render_to_response('list.html',{'files':files,'form':form}, context_instance=RequestContext(request))#last field is needed for csrf authentication




def delete_uploaded_file(request):

    
    arg_name = request.POST.get('x','')
    print 'At last the file name is:========>',os.path.basename(arg_name)
    file_to_delete = Uploaded_Files.objects.filter(Q(title = arg_name))
    print file_to_delete
    print 'queryset is of length:',len(file_to_delete)
    print 'Searched the db for name:',file_to_delete[0].title.name
    print 'Searched the db for title:',file_to_delete[0].title

    file_to_delete.delete()#delete from the db
    cmd = "rm my_media/documents/"+str(os.path.basename(arg_name))+""
    print cmd   
    
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print p
   
    return HttpResponseRedirect('/handle_uploaded_file/')



items_to_show = 15
#this function serves as a validation input handler for the lvn_affecting_table module in the Django project
#it accepts only strings that satisfy the regular expression below
#--------------------------------------------#--------------------------------------------------------------#
def validate_bfr_lvn(arg):

    pattern = re.compile(r'^\d{1,6}_\d{1,4}$')
    if pattern.search(arg):
        print 'Correct!'
        return True
    else:
        print 'not in XXX_YYY format..please try again'
        return False

def validate_iso(arg):
    
#    There are a lot of ways to go to Rome...
#    ...one... 
#    fext = os.path.splitext(arg)[1]
#    if fext == 'iso' or fext == 'ISO':
#        print 'success'
#        return True
#    else:
#        return False
#   or ...two...

    pattern = re.compile(r'^.+\.(iso|ISO)$')
    if pattern.search(arg):
        print 'success'
        return True
    else:
        print 'not in xxx.iso format..please try again'
        return False




def retrieve_form_id(arg):
    local_id = re.sub("\D", "", arg)
    if local_id:
        return local_id
    else: 
        return 0


#this function serves for the creation of the template where the user can write and submit it's data to the database
#----------------------------------------------#--------------------------------------------------------------------#
def insert_form(request):
    d = {}
    d.update(csrf(request))
    form = Wiki_insert_form()
    my_branch = request.GET.get('bname','')
    d['form']= form
    d['branch']= my_branch
    return render_to_response('insert_form.html', d)



#this function is called after the aforementioned module returns(insert_form).It is used to save the data to the database
#----------------------------------------------#------------------------------------------------------------------------#
def save_on_insert(request):
   
    if request.method == 'POST':
        arg_branch = request.POST.get('brname','')
        my_branch = Branch.objects.get(branch_name=arg_branch)
        my_bfr_lvn = request.POST.get('bfr_lvn','')
        my_rev = request.POST.get('rev_id','')
        my_author = request.POST.get('author','')
        my_adaptation = request.POST.get('adaptation','')
        my_other = request.POST.get('other','')
       
        if len(my_rev)==0 or not is_number(my_rev):
# or not validate_bfr_lvn(my_bfr_lvn):
            return render_to_response('message.html',{'msg': 'Revision field must be a valid number','branch':arg_branch,'return_to':'/lvnaffectingtable/'})  
        elif not validate_bfr_lvn(my_bfr_lvn):
            return render_to_response('message.html',{'msg': 'BFR_LVN must be in the form of XXXX_YYY','branch':arg_branch,'return_to':'/lvnaffectingtable/'})  
        else:
            wiki_ret=[]
            qset = Q()
            qset &= Q(rev_id=my_rev)
            qset &= Q(bfr_lvn=my_bfr_lvn)
            qset &= Q(author=my_author)
            wiki_ret = Wiki_entry.objects.filter(qset)
            wiki_entries_found = len(wiki_ret)
            if wiki_entries_found == 0:
                new_entry = Wiki_entry(bfr_lvn=my_bfr_lvn,branch_name=my_branch,rev_id=my_rev,author=my_author,adaptation=my_adaptation,other=my_other)
                new_entry.save()
            else:
                err_msg = 'Found ' + str(wiki_entries_found) + ' already existing entries for the same author ' + my_author + ' and the same bfr_lvn and revision. Please update existing entry'
                return render_to_response('message_resp.html',{'msg': err_msg, 'branch':my_branch, 'return_to':'/lvnaffectingtable/'})
    return render_to_response('success.html',{'branch':arg_branch})

def validate_formset(formset, res_list):
    validation_err = 0 
    validation_errmsg = ''
    lcounter = 0 
    for form in formset:
#        print form.as_table()
#        print form['id'].data, form['rev_id'].data
        lcounter +=1
        my_bfr_lvn = form['bfr_lvn'].data
        my_rev = form['rev_id'].data
        my_author = form['author'].data
        my_adaptation = form['adaptation'].data
        my_other = form['other'].data

        if (len(my_rev) == 0) or (not is_number(my_rev)):
            print 'at this point 1'
            validation_err = 1 
            validation_errmsg = 'Revision field must be a valid number'
        elif not validate_bfr_lvn(my_bfr_lvn):
            print 'at this point 2'
            validation_err = 1 
            validation_errmsg = 'BFR_LVN must be in the form of XXXX_YYY'
        else:
            print 'at this point 3'
            validation_errmsg = 'pass'
    res_list.append(validation_errmsg)
    res_list.append(lcounter)
    return validation_err

def validate_LVNFeature_formset(formset, res_list):
    validation_err = 0 
    validation_errmsg = ''
    lcounter = 0 
    for form in formset:
#        print form.as_table()
#        print form['id'].data, form['rev_id'].data
        lcounter +=1
        my_lvn = form['lvn'].data
        my_rev = form['rev_id'].data
#        my_author = form['author'].data
#        my_adaptation = form['adaptation'].data
#        my_other = form['other'].data

        if (len(my_rev) == 0) or (not is_number(my_rev)):
            validation_err = 1 
            validation_errmsg = 'Revision field must be a valid number'
        elif (len(my_lvn) == 0) or (not is_number(my_lvn)):
            print 'at this point 2'
            validation_err = 1 
            validation_errmsg = 'LVN field must be a valid number'
        else:
            print 'at this point 3'
            validation_errmsg = 'pass'
    res_list.append(validation_errmsg)
    res_list.append(lcounter)
    return validation_err

def validate_branch(branch):
    my_branch= ''
    try:
        my_branch = Branch.objects.get(branch_name=branch)
        return my_branch  
    except Branch.DoesNotExist:
        return ''


def manage_wiki_entries(request):
   
    d = {}
    d.update(csrf(request))
    delete_box = 0
    update_box = 0
    if request.method == 'POST':
        my_branch = request.POST.get('branch_name','tmp1')
        print 'POST my branch is: ', (my_branch)
        resp = request.POST.get('action')
        print 'resp is: %s' %  (resp)
        if resp:
            print 'entries to insert or update'
            if (resp == 'delete'):
                print 'at delete' 
                #do delete
                wikiFormset= modelformset_factory(Wiki_entry, extra=0, exclude=('branch_name'), form=Wikientryresp)
                formset = wikiFormset(request.POST)
                lcounter = 0
                for form in formset:
                    my_id = form['id'].data
                    upd_entry = Wiki_entry(pk=my_id)
                    darg_name = Wiki_entry.objects.filter(pk=my_id).values('title')
                    for x in darg_name:
                        arg_name = x['title']
                        if arg_name is not '':
                            cmd = "rm my_media/wikitabledocs/"+str(os.path.basename(str(arg_name)))+""
                            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    upd_entry.delete()
                    lcounter =+1
                err_msg = 'deleted ' + str(lcounter) + ' entries'
                return render_to_response('message_resp.html',{'msg': err_msg, 'branch':my_branch,'return_to':'/lvnaffectingtable/'})  
            elif (resp == 'update'):
                print 'at update'
                wikiFormset= modelformset_factory(Wiki_entry, extra=0, exclude=('branch_name'), form=Wikientryresp)
                formset = wikiFormset(request.POST,request.FILES)
                res_lst = [] 
                err     = validate_formset(formset, res_lst)

                if (err == 0):
                    #do update
                    print 'update'
                    my_branch = Branch.objects.get(branch_name=my_branch)
                    lcounter=0
                    for form in formset:
#                        print form['id'].data,  form['adaptation'].data
                        my_id = form['id'].data
                        upd_entry = Wiki_entry(pk=my_id)
                        upd_entry.branch_name = my_branch
                        upd_entry.bfr_lvn = form['bfr_lvn'].data
                        upd_entry.rev_id = form['rev_id'].data
                        upd_entry.author = form['author'].data
                        upd_entry.adaptation = form['adaptation'].data
                        upd_entry.other = form['other'].data
                        ltitle = 'form-'+str(lcounter)+'-title' 

                        if ltitle in request.FILES.keys():
                            print 'found title: %s' % str(form['title'].data) 
                            title = request.FILES[ltitle]
                            #old entry if exists should be removed django does not do it automatically...
                            darg_name = Wiki_entry.objects.filter(pk=my_id).values('title')
                            for x in darg_name:
                                arg_name = x['title']
                                print 'old fname is: ', str(arg_name)
                                if arg_name is not '':
                                    cmd = "rm my_media/wikitabledocs/"+str(os.path.basename(str(arg_name)))+""
#                                   print 'cmd is ', cmd 
                                    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                            #and now get to save new 
                            upd_entry.title = request.FILES[ltitle]
                        else:
                            dfile = 'form-'+str(lcounter)+'-delete_file'
                            print 'possibly deleting a file --'
                            if dfile in request.POST.keys():
                                print 'key found'
                                darg_name = Wiki_entry.objects.filter(pk=my_id).values('title')
                                for x in darg_name:
                                    arg_name = x['title']
#                                   print 'fname is: ', str(arg_name)
                                    cmd = "rm my_media/wikitabledocs/"+str(os.path.basename(str(arg_name)))+""
#                                   print 'cmd is ', cmd 
                                    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                                upd_entry.title = ''
                            else:
                                print 'key not found'
                                darg_name = Wiki_entry.objects.filter(pk=my_id).values('title')
                                for x in darg_name:
                                    arg_name = x['title']
#                                   print 'fname is: ', str(arg_name)
                                    upd_entry.title = arg_name
                        upd_entry.save()
                        lcounter += 1
                    err_msg = 'updated ' + str(lcounter) + ' entries'
                    print  err_msg
                    return render_to_response('message_resp.html',{'msg': err_msg, 'branch':my_branch,'return_to':'/lvnaffectingtable/'})  
                else:
                    return render_to_response('message_resp.html',{'msg': res_lst[0], 'branch':my_branch,'return_to':'/lvnaffectingtable/'})  
            else:
                 print 'some error occured'
        else:
            print 'select entries to update or delete '
            wikiFormset= modelformset_factory(Wiki_entry, extra=0, exclude=('branch_name'), form=Wikientry)
            for i in request.POST.keys():
                print i
            print '-----------'	
            cp = request.POST.copy()
            qset = Q()

            for entry in cp.items():
                if 'delete' in entry[0]:
                    delete_box+=1
                    local_id=retrieve_form_id(entry[0])
                    slocal_id ='form-'+str(local_id)+'-rev_id'
                    print '------', '%s', slocal_id
                    for e in cp.items():
                        if slocal_id in e[0]:
#                            print 'e[1]]=',  e[1]
                            qset |= Q(rev_id=e[1])
                if 'update' in entry[0]:
                    update_box+=1
                    local_id=entry[0]
                    local_id=retrieve_form_id(entry[0])
                    slocal_id ='form-'+str(local_id)+'-rev_id'
                    for e in cp.items():
                        if slocal_id in e[0]:
#                            print  'e[1]]=', e[1]
                            qset |= Q(rev_id=e[1])
            print('updates are ', update_box)
            print('deletes are ', delete_box)
 
            if ((update_box > 0) and (delete_box > 0)):
                return render_to_response('message_resp.html',{'msg':'group actions can be of only one type: update or delete not both','return_to':'/lvnaffectingtable/'})
            if (update_box > 0) :
                d['action'] = 'update'
            elif (delete_box > 0):
                d['action'] = 'delete'
            else:
                return render_to_response('message_resp.html',{'msg':'no single or group actions selected: update or delete Please try again','return_to':'/lvnaffectingtable/'})
            print '---------------' 
            cp['form-TOTAL_FORMS'] = int(request.POST.get('entries_len'))
            cp['form-INITIAL_FORMS']= 0 
            cp['form-MAX_NUM_FORMS']= items_to_show
            print 'queryset:'
            print "updates are %d" % (update_box)
            print "deletes are %d" % (delete_box)
            queryset = Wiki_entry.objects.filter(qset)
            wikiFormsetresp= modelformset_factory(Wiki_entry, extra=0, exclude=('branch_name'), form=Wikientryresp)
            respformset = wikiFormsetresp(queryset=Wiki_entry.objects.filter(qset))
            for form in respformset:
                print 'form is: ', form.as_table()
            d['entries']=respformset
            d['branch']=my_branch
            d['response']='response'
            return render_to_response('manage_wiki_entries.html',  d)
    else:
        my_branch = request.GET.get('branch_name', 'tmp')
        print 'my branch is: %s ' % (my_branch)
        page_index = int(request.GET.get('page', '1'))
#        print 'page is: ', page_index
        if page_index > 1:
            gbranch = request.session["branch"]
        else:  #first page
            if 'branch' not in request.session: 
#                print 'first time to visit page 1'
                if my_branch=='':
                    return render_to_response('message.html',{'msg':'Please narrow your search by using a specific branch','return_to':'/lvnaffectingtable/'})
                request.session['branch'] = my_branch
                gbranch = request.session["branch"]
            else:
#                print 'page 1 but not first time'
                if (my_branch == ''):
                    return render_to_response('message.html',{'msg':'Please narrow your search by using a specific branch','return_to':'/lvnaffectingtable/'})
                elif (my_branch == 'tmp'):
                    gbranch = request.session["branch"]
                else:
                    request.session['branch'] = my_branch
                    gbranch = request.session["branch"]
#                    print 'start a new search using the back button in browser...'
        print '---------------------------------'
        print 'session branch id is :', (gbranch)
        print 'start branch id is :', (my_branch)
        print '---------------------------------'

        if gbranch:
#            print 'at here 1'  
            d['branch']=gbranch
            wikiFormset= modelformset_factory(Wiki_entry, extra=0, exclude=('branch_name'), form=Wikientry)
            formset = wikiFormset(queryset=Wiki_entry.objects.filter(branch_name=gbranch).order_by('-rev_id', '-bfr_lvn'))
        else:
#            print 'at here 2'  
            d['branch']=my_branch
            wikiFormset= modelformset_factory(Wiki_entry, extra=0, exclude=('branch_name'), form=Wikientry)
            formset = wikiFormset(queryset=Wiki_entry.objects.filter(branch_name=my_branch).order_by('-rev_id', '-bfr_lvn'))

        lcounter=0  
        alink = [] 
        for x in formset.get_queryset():
            if x.title:
               doc_path=os.path.abspath(os.path.join('..', x.title.url))
            else:
               doc_path=''#os.path.abspath(os.path.join('..', "/templates/no_file_associated.html"))
            alink.append(doc_path)

        bform = [] 
        for form in formset:
             bform.append(form)

        entries=zip(alink, bform)


#         paginator = Paginator(formset, items_to_show) # show 5 items per pagea
        paginator = Paginator(entries, items_to_show) # show 5 items per pagea
#        for form in formset:
#            print form.as_table()
        d['initial']='initial'
#        print '---------------------'  
        print 'entries found: ', (paginator.count)
        try:
            entries = paginator.page(page_index)
#            print '---- current entries %d',  entries
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            entries = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            entries = paginator.page(paginator.num_pages)
        d["entries"]=entries
#        print 'count is %d ', (int(len(entries.object_list)))
        d['entries_len']=str(len(entries.object_list))
        return render_to_response('manage_wiki_entries.html',  d)




def clean_session_data(request):
     print 'before cleaning'
     request.session.clear()
     print 'after cleaning' 


class author_commits_form(forms.Form):
    author = forms.CharField()
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label='all')
     

def search_author_commits(request):
    form = author_commits_form()
    clean_session_data(request)
    print 'in search form request'
    return render_to_response('search_author_commits.html', {
        'form': form,
    })


def listing(request, page_index=1):
    page_index = int(request.GET.get('page', '1'))


    my_author = request.GET.get('author', 'tmp')
    my_branch = request.GET.get('branch', 'tmp')

    print 'start branch id is :', (my_branch)
    print 'start author is :', (my_author)    

    print '-----entering func listing -----'
    print '--- with the following values --'
    print 'page ', '%d', page_index
    print 'author and branch', '%s %s', my_author, my_branch
 
    if page_index > 1:
        gauthor = request.session["author"]
        gbranch = request.session["branch"]
    else:  #first page
        if 'author' not in request.session and 'branch' not in request.session: 
            print 'first time to visit page 1'
            if not my_author:
                msg_txt = 'Incorrect name for author. Please provide a name to try again'
                return render_to_response('message.html',{'msg': msg_txt, 'return_to':'/search-author-commits/'})                
            else: 
                request.session['author'] = my_author
                request.session['branch'] = my_branch
                gauthor = request.session["author"]
                gbranch = request.session["branch"]
        else:
            print 'page 1 but not first time'
            if my_author == 'tmp' and my_branch == 'tmp':
                gauthor = request.session["author"]
                gbranch = request.session["branch"]
            else:
                request.session['author'] = my_author
                request.session['branch'] = my_branch
                gauthor = request.session["author"]
                gbranch = request.session["branch"]
                print 'start a new search using the back button in browser...'

#                msg_txt = 'You should not not use back buttons for a new search'
#                return render_to_response('message.html',{'msg': msg_txt, 'return_to':'/search-author-commits/'})                


#    else:
#        msg_txt = 'If you want to conduct another search use the links provied not the back button. Otherwise you will work with stale data'
#        return render_to_response('message.html',{'msg': msg_txt, 'return_to':'/search-author-commits/'})
                   

    print 'session branch id is :', (gbranch)
    print 'session author is :', (gauthor)    
    print 'start branch id is :', (my_branch)
    print 'start author is :', (my_author)    

#    global gauthor
#    global gbranch 
#    print 'starting global branch id is :', (gbranch)
#    print 'starting global author is :', (gauthor)    
       
    
    author = '%'+gauthor+'%'
    lvn_ret=[]
    for lvn_entry in Lvn_entry.objects.raw('select distinct author, id from weblvnapp_lvn_entry where author like %s group by author', [author]):
        lvn_ret.append(lvn_entry)
        print lvn_entry.author
    authors_found = len(lvn_ret)
         
    print gauthor, str(authors_found)
    if authors_found > 1:
        msg_txt = 'Found: '+ str(authors_found) +' authors with a name like : ' + gauthor + '. Narrow your search and try again'
            #msg_txt = 'Found: more than one authors. Narrow your search and try again'
        return render_to_response('multiple_authors_list.html',{'lvn_ret': lvn_ret, 'msg': msg_txt, 'return_to':'/search-author-commits/'})
    else:
        if authors_found == 0:
            msg_txt = 'No such author found. Please try again'
            return render_to_response('message.html',{'msg': msg_txt, 'return_to':'/search-author-commits/'})
          

    print '----------------' 
    print 'final lvn entry author is :', (lvn_entry.author)
#    global gauthor
#    gauthor=lvn_entry.author
#    my_author = gauthor
    gauthor = lvn_entry.author  
    request.session["author"] = gauthor
    
    print '===================' 

    if gbranch:
#        print 'at here 1'  
        branch_name=Branch.objects.get(pk=gbranch)
        author_list = Lvn_entry.objects.filter(author=gauthor, branch_name=branch_name).order_by('branch_name', '-rev_id')
    else:
#        print 'at here 2'  
        author_list = Lvn_entry.objects.filter(author=gauthor).order_by('branch_name', '-rev_id')
 
#    from django.db.models import Q
#    author_list = Lvn_entry.objects.filter(author=my_author,branch_name=branch_name).order_by('branch_name', '-rev_id')
    
    for lvn in author_list:
      print gauthor, lvn.lvn, lvn.branch_name, lvn.rev_id
    paginator = Paginator(author_list, items_to_show) # show 5 items per page

    print 'entries found: ', (paginator.count)
    
    #print 'received page at point 3 = ', (page_index)
    try:
        authorslist = paginator.page(page_index)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        authorslist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        authorslist = paginator.page(paginator.num_pages)
 #   for item in authorslist.object_list:
#        print 'layout_rev %s VS to rev_id %s' % (item.layout_rev,item.rev_id)
    return render_to_response('author_commits_list.html', {"authorslist": authorslist, 'author': gauthor, 'entries': str(len(author_list))})


def main(request):
    last_upd=[]
    for lupd in DBUpdate.objects.all():
      last_upd.append(lupd)  
      print lupd.lastUpdDate		
    return render_to_response('main.html', {'last_upd':last_upd})

def search_current(request):
    lvn_ret=[]
    for lvn_entry in Lvn_entry.objects.raw('select max(lvn), branch_name_id, author, rev_id, commit_date, a.id, layout_rev from weblvnapp_lvn_entry a, weblvnapp_branch b where a.branch_name_id = b.branch_name and b.display_flag=1 group by branch_name_id order by branch_name_id desc'):
        if lvn_entry.rev_id != lvn_entry.layout_rev:
           print 'rev: %d layout_rev: %d' % (lvn_entry.rev_id, lvn_entry.layout_rev)  
           lvn_entry.layout_rev = 0
        lvn_ret.append(lvn_entry)
        print lvn_entry.lvn, lvn_entry.branch_name, lvn_entry.author
    return render_to_response('search_current_lvn_results.html', {'lvn_ret':lvn_ret})

class Lvn_entry_current_form(forms.Form):
      pass

def search_current_lvn(request):
    form = Lvn_entry_current_form()
    return render_to_response('search_current_lvn.html', {'form':form,})


class Lvn_entry_form(forms.Form):

    lvn = forms.IntegerField()
    #revision = forms.IntegerField()
    #author = forms.CharField()      
    revision = forms.IntegerField()
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label='all')
def search_lvn(request):
    form = Lvn_entry_form()
    return render_to_response('search_lvn.html', {
        'form': form,
    })


class Revision_entry_form(forms.Form):

    revision = forms.IntegerField()


#this function actually instantiates a Revision_entry_form(check the class above) object in order to create a template where only the revision field is editable
#----------------------------------------------------------------------#----------------------------------------------------------------------------------------
def changedrevision(request):

    form = Revision_entry_form()
    return render_to_response('search_for_revision.html', {
        'form': form,
    })



#same as above
#-----------------------------------------------------------------------#---------------------------------------------------------------------------------------
def lvn_affecting_table(request):
    clean_session_data(request)

    form = Wiki_form()#this Class is defined in models.py instead of views.py.This is better approach.
    return render_to_response('lvn_affecting_table.html',{'form':form,

    })    

#-----------------------------------------------------------------------#---------------------------------------------------------------------------------------
def builds_table(request):
#    clean_session_data(request)

    form = Build_form()
    return render_to_response('builds_table.html',{'form':form,})




#validate the first form --check if a valid number is submitted in the lvn field
#another validation handler 
#-------------------------------------------------------------------------#---------------------------------------------------------------------------------------
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#function that gets a list as input and returns a new list with unique elements inside
#------------------------------------------------------------------------#--------------------------------------------------------------------------------------
def unique(inlist):
    blind_unique = []
    uniques = []
    for item in inlist:
        if item.branch_name not in blind_unique:
            blind_unique.append(item.branch_name)
            uniques.append(item)
    return uniques










###########################################################################################



#this function will be called when end user will submit the LVN and the branch that wants to search for.
#it returns info about who is the responsible user that increased the LVN with the Change reason
#--------------------------------------------------------#------------------------------------------------------------------------------

def uniqueLvn(request):
    
    arg_lvn = request.GET['lvn']
    arg_branch = request.GET['branch']
    arg_revision = request.GET['revision']


  #### code for input validation ####

    if arg_lvn and arg_revision:
        return render_to_response('message.html',{'msg':'You must select either lvn OR revision field.Not both.','return_to':'/search-lvn/'})



    if len(arg_lvn)==0 and len(arg_branch)>0:


        qs = []
        qs.append(Q(branch_name__id=arg_branch))
        qry =  Q()
        for q in qs:
            qry = qry & q
        branch_set = Lvn_entry.objects.filter(qry)[:1]
        print 'BRANCH NAME',arg_branch
        print branch_set
        print branch_set[0].branch_name
        cmd = "ls my_media/isu_compact/*|grep "+str(branch_set[0].branch_name)+'.'+'txt'+" |awk -F: '{print $1}'|awk -F/ '{print $NF}'"
       
        output = []
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = p.communicate()[0].strip()
       
        return render_to_response('search_results.html', {
        'branch_set':output  
       })

                 

#return the page.txt here
   
    elif len(arg_lvn) == 0 and len(arg_branch) == 0 and not arg_revision:#if len(arg_branch) == 0 means that we choose the 'all' option in the drop-down menu
            return render_to_response('message.html',{'msg':'Please narrow your search by using a specific branch','return_to':'/search-lvn/'})



################################################################   code if we are requesting the revision field only #################################


    elif len(arg_lvn) == 0 and arg_revision:
        return fetch_revision_change(request)

################################################################ code only if we are requesting LVN field   #####################################################
    else:
        if len(arg_lvn)>0:
           
           val = is_number(arg_lvn)
           if val == False:
               return render_to_response('message.html',{'msg': 'Please provide a valid number in the LVN field', 'return_to':'/search-lvn/'})
           else:
           
                qs = []
                #if len(arg_lvn)>0:
                qs.append(Q(lvn=arg_lvn))
                if len(arg_branch)>0 and arg_branch!='all':
                    qs.append(Q(branch_name__id=arg_branch))

                qry = Q()
                for q in qs:
                    qry = qry & q
                lvn_set = Lvn_entry.objects.filter(qry)


                if lvn_set:#django returns the unique lvn(changed) per branch
                    my_set = unique(lvn_set)
                    tmp_qs = []
                    for item in my_set:
                        branch_obj = Branch.objects.filter(Q(branch_name=item.branch_name))
                        tmp_qs.append(branch_obj[0].bfr_id) ####### branch_obj is a list and not an object.so i operate on the first item on this list.
                    f_list = zip(my_set,tmp_qs) 

        ######  code here for LVN change reason output   #######
                    change_reason = []
                    for el in f_list:
                        cmd = "ls my_media/lvn_change/*|grep "+str(el[1])+'_'+str(el[0].lvn)+'.'+'txt'+" |awk -F: '{print $1}'|awk -F/ '{print $NF}' 2>/dev/null"
                        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                        outp = p.communicate()[0].strip()
           
                        change_reason.append(outp)
                    f_list1 = zip(f_list,change_reason)  
       
                    return render_to_response('search_results.html', {
       'lvn_set': my_set , 'bfr_set':tmp_qs , 'f_set': f_list, 'f_set1':f_list1  
       })

                else:
                    if not lvn_set:
    
                        return render_to_response('message.html',{'msg': 'There is not such LVN in the branches.Try again', 'return_to':'/search-lvn/'})        



################################################################################################





def feature_related_table(request):
    #this is a direct copy from manage_wiki_entries 
    #since that fuction seemed to work this should also work ...
    #added necessary modifications and removed paginator
    d = {}
    d.update(csrf(request))
    delete_box = 0
    update_box = 0
    if request.method == 'POST':
        resp = request.POST.get('action')
        print 'resp is: ',  resp
        if resp:
            print 'entries to insert or update'
            if (resp == 'delete'):
#                print 'at here' 
                lvnFeatureFormset= modelformset_factory(LVN_Feature_Related, extra=0, form=LVNFeatureresp)
                formset = lvnFeatureFormset(request.POST)
                #do delete
                lcounter=0 
                for form in formset:
#                    print form['lvn'].data
                    my_id = form['id'].data
                    upd_entry = LVN_Feature_Related(pk=my_id)
                    darg_name = LVN_Feature_related.objects.filter(pk=my_id).values('title')
                    for x in darg_name:
                        arg_name = x['result_file']
                        if arg_name is not '':
                            cmd = "rm my_media/documents/"+str(os.path.basename(str(arg_name)))+""
                            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    upd_entry.delete()
                    lcounter =+1
                uentries = request.POST.get('entries_len')
                err_msg = 'deleted ' + str(uentries) + ' entries'
                return render_to_response('message_resp.html',{'msg': err_msg, 'return_to':'/feature_related_table/'})  
            elif (resp == 'update'):
                print 'at update '
                lvnFeatureFormset= modelformset_factory(LVN_Feature_Related, extra=0, form=LVNFeatureresp)
                formset = lvnFeatureFormset(request.POST, request.FILES)
                res_lst = [] 
                err     = validate_LVNFeature_formset(formset, res_lst)
                if err == 0:
 
                    lcounter=0
                    for form in formset:
                        my_id = form['id'].data
                        print 'my id is ', my_id
                        upd_entry = LVN_Feature_Related(pk=my_id)
                        upd_entry.lvn = form['lvn'].data
                        upd_entry.rev_id = form['rev_id'].data
                        upd_entry.team = form['team'].data
                        upd_entry.feature = form['feature'].data
                        upd_entry.affected_structures = form['affected_structures'].data
                        upd_entry.other = form['other'].data
                        ltitle = 'form-'+str(lcounter)+'-title' 


                        if ltitle in request.FILES.keys():
                           print 'found title: %s' % str(form['title'].data) 
                           title = request.FILES[ltitle]

                           #old entry if exists should be removed django does not do it automatically...
                           darg_name = LVN_Feature_Related.objects.filter(pk=my_id).values('title')
                           for x in darg_name:
                               arg_name = x['title']
                               print 'old fname is: ', str(arg_name)
                               if arg_name is not '':
                                   cmd = "rm my_media/documents/"+str(os.path.basename(str(arg_name)))+""
#                                  print 'cmd is ', cmd 
                                   p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                            #and now get to save new 

                           upd_entry.title = request.FILES[ltitle]
                        else:
                           dfile = 'form-'+str(lcounter)+'-delete_file'
#                           print 'deleting a file' , dfile
#                           print form['title'].data, form['delete_file'].data  
                           if dfile in request.POST.keys():
                               darg_name= LVN_Feature_Related.objects.filter(pk=my_id).values('title')
                               for x in darg_name:
                                   arg_name = x['title']
                               print 'fname is: ', str(arg_name)
                               cmd = "rm my_media/documents/"+str(os.path.basename(str(arg_name)))+""
                               print 'cmd is ', cmd 
                               p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                               upd_entry.title=''
                           else:
                               print 'key not found'
                               darg_name = LVN_Feature_Related.objects.filter(pk=my_id).values('title')
                               for x in darg_name:
                                   arg_name = x['title']
#                                  print 'fname is: ', str(arg_name)
                                   upd_entry.title = arg_name

                        upd_entry.save()
                        lcounter =+1
                    print ' update '
                    uentries = request.POST.get('entries_len')
                    err_msg = 'updated ' + str(uentries) + ' entries'
                    print  err_msg
                    return render_to_response('message_resp.html',{'msg': err_msg, 'return_to':'/feature_related_table/'})  
                else:
                    return render_to_response('message_resp.html',{'msg': res_lst[0], 'return_to':'/feature_related_table/'})  
            else:
                 print 'some error occured'
        else:
            print 'select entries to update or delete '
            print 'before loop 1'
            cp = request.POST.copy()
            qset = Q()
            for entry in cp.items():
                if 'delete' in entry[0]:
                    delete_box+=1
                    local_id=retrieve_form_id(entry[0])
                    slocal_id ='form-'+str(local_id)+'-rev_id'
                    print '------', '%s', slocal_id
                    for e in cp.items():
                        if slocal_id in e[0]:
                            qset |= Q(rev_id=e[1])
                if 'update' in entry[0]:
                    update_box+=1
                    local_id=entry[0]
                    local_id=retrieve_form_id(entry[0])
                    slocal_id ='form-'+str(local_id)+'-rev_id'
                    print '------' '%s' %slocal_id
                    for e in cp.items():
                        if slocal_id in e[0]:
                            qset |= Q(rev_id=e[1])
            print('updates are ', update_box)
            print('deletes are ', delete_box)
            if ((update_box > 0) and (delete_box > 0)):
                return render_to_response('message_resp.html',{'msg':'group actions can be of only one type: update or delete not both','return_to':'/feature_related_table/'})
            if (update_box > 0) :
                d['action'] = 'update'
                d['entries_len'] = update_box
            elif (delete_box > 0):
                d['action'] = 'delete'
                d['entries_len'] = delete_box
            else:
                return render_to_response('message_resp.html',{'msg':'no single or group actions selected: update or delete Please try again','return_to':'/feature_related_table/'})
            print("updates are ", update_box)
            print("deletes are ", delete_box)
            queryset = LVN_Feature_Related.objects.filter(qset)
            lvnFeatureformsetresp= modelformset_factory(LVN_Feature_Related, extra=0, form=LVNFeatureresp)
            formset = lvnFeatureformsetresp(queryset=LVN_Feature_Related.objects.filter(qset))
            d['entries']=formset
            d['response']='response'
            return render_to_response('manage_LVN_feature_entries.html',  d)
    else:
        lvnFeatureFormset = modelformset_factory(LVN_Feature_Related, extra=0, form=LVNFeature)
        formset = lvnFeatureFormset(queryset=LVN_Feature_Related.objects.all().order_by('-rev_id', '-lvn'))
        lcounter=0  
        alink = [] 
        for x in formset.get_queryset():
            if x.title:
                doc_path=os.path.abspath(os.path.join('..', x.title.url))
            else:
                doc_path=''#os.path.abspath(os.path.join('..', "/templates/no_file_associated.html"))
            alink.append(doc_path)

        bform = [] 
        for form in formset:
            bform.append(form)
#            print form.fields['alink'].initial #, form.fields['other'].initial  

        entries=zip(alink, bform)
        d['initial']='initial'
        d['entries']=entries
        return render_to_response('manage_LVN_feature_entries.html',  d)





#function that takes a revision number as input and returns info about the LVN change,with svn log for this revision
#------------------------------------------------------------------------#---------------------------------------------------------------------------------



def fetch_revision_change(request):


    print 'Entered the fetch function with',request.GET['revision']
  #### code for input validation ####


    arg_revision = request.GET['revision']
    val = is_number(arg_revision)
    if val == False:
        return render_to_response('message.html',{'msg': 'Please provide a valid number in the revision field','arg_rev':arg_revision, 'return_to':'/changedrevision/'})
        
    qs = []
    tmp_qs = []
    if len(arg_revision)>0:
        qs.append(Q(rev_id=arg_revision))
   # if len(arg_branch)>0 and arg_branch!='all':
    #    qs.append(Q(branch_name__id=arg_branch))

    qry = Q()
    for q in qs:
        qry = qry & q
    revision_set = Lvn_entry.objects.filter(qry)

    if revision_set and len(arg_revision)>0:#django returns if this commit(revision number)caused LVN change
        #my_set = unique(lvn_set)
        for item in revision_set:
            if item.layout_rev == item.rev_id:
                my_branch = Branch.objects.filter(Q(branch_name=item.branch_name))
                tmp_qs.append(my_branch[0].bfr_id) ####### branch_obj is a list and not an object.so i operate on the first item on this list.
                #f_list = zip(my_set,tmp_qs) 


                return render_to_response('search_results_revision.html', {
       'revision_set': revision_set,'arg_rev':arg_revision,'bfr_set':tmp_qs })
            else:
                my_branch = Branch.objects.filter(Q(branch_name=item.branch_name))
                tmp_qs.append(my_branch[0].bfr_id)
                return render_to_response('message.html',{'msg': 'This commit did not cause LVN change in any branch', 'return_to':'/changedrevision/','revision_set':revision_set,'arg_rev':arg_revision,'bfr_set':tmp_qs })

    elif not revision_set:
        return render_to_response('message.html',{'msg': 'This commit is not made in code or it does not exist yet.', 'return_to':'/changedrevision/','arg_rev':arg_revision })


def error_detail(request,revision_):


    '''This function is used in conjuction with the relevant url in urls.py
     When requesting from django a url of that form /svnhistory/XXXXXX.txt
     django loads this function and passes to it the XXXXX arg (revision_)'''

    try:
        f = open(settings.MEDIA_ROOT+'/svnhistory/'+revision_+'.txt','r')
    
    except IOError,e:
        print e
        raise Http404
    f.close()
    return HttpResponseRedirect('/my_media/svnhistory/'+revision_+'.txt')


def isu_path_table(request):
    d = {}
    d.update(csrf(request))
    delete_box = 0
    update_box = 0
    print 'in isu_path_table'
    if request.method == 'POST':
        resp = request.POST.get('action')
        print 'resp is: ',  resp
        if resp:
            print 'entries to insert or update'
            if (resp == 'delete'):
                ISUFormset= modelformset_factory(ISU_working_path, extra=0, form=ISUFeature)
                formset = ISUFormset(request.POST)
                lcounter=0 
                for form in formset:
                    my_id = form['id'].data
                    print 'myid: ', my_id  
                    upd_entry = ISU_working_path(pk=my_id)
                    darg_name = ISU_working_path.objects.filter(pk=my_id).values('result_file')
                    for x in darg_name:
                        arg_name = x['result_file']
                        if arg_name is not '':
                            cmd = "rm my_media/documents/"+str(os.path.basename(str(arg_name)))+""
                            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    upd_entry.delete()
                    lcounter += 1
                uentries = request.POST.get('entries_len')
                err_msg = 'deleted ' + str(lcounter) + ' entries'
                return render_to_response('message_resp.html',{'msg': err_msg, 'return_to':'/manage_ISU_paths/'})  
            elif (resp == 'update'):
                ISUFormset= modelformset_factory(ISU_working_path, extra=0, form=ISUresp)
                formset = ISUFormset(request.POST, request.FILES)
                lcounter=0
                for form in formset:
#                    print '-------------------------at here'
                    my_id = form['id'].data
                    print 'id is ' , my_id
                    upd_entry = ISU_working_path(pk=my_id)

                    #Date and tester do not change
                    print 'date and tester', form['test_date'].data, form['tester'].data 
                    upd_entry.test_date = form['test_date'].data
                    upd_entry.tester    = form['tester'].data  
                    upd_entry.src_iso = form['src_iso'].data
                    if not validate_iso(upd_entry.src_iso):
                        return render_to_response('message.html',{'msg': 'src iso should contain a .iso','return_to':'/insert_ISU_path_form/'})  
                    upd_entry.src_build_name = form['src_build_name'].data
#                    if len(upd_entry.src_build_name) == 0 or not is_number(upd_entry.src_build_name):
#                        return render_to_response('message.html',{'msg': 'source build field must be a valid number','return_to':'/manage_ISU_paths/'})  
                    sbranch_name = form['src_branch_name'].data
                    my_branch = ''
                    my_branch = validate_branch(sbranch_name)   
                    if my_branch is not '':
                        upd_entry.src_branch_name = my_branch
                    else:
                        return render_to_response('message.html',{'msg': 'source branch name invalid','return_to':'/manage_ISU_paths/'})  
                        
#                    print '-------------'
#                    print 'source ', upd_entry.src_branch_name
#                    print '-------------' 

                    upd_entry.trg_iso = form['trg_iso'].data
                    if not validate_iso(upd_entry.trg_iso):
                        return render_to_response('message.html',{'msg': 'trg iso should contain a .iso','return_to':'/insert_ISU_path_form/'})  
                    upd_entry.trg_build_name = form['trg_build_name'].data
#                    if len(upd_entry.trg_build_name) == 0 or not is_number(upd_entry.trg_build_name):
#                        return render_to_response('message.html',{'msg': 'target build field must be a valid number','return_to':'/manage_ISU_paths/'})  

                    tbranch_name = form['trg_branch_name'].data
                    my_branch = ''
                    my_branch = validate_branch(tbranch_name)   
                    if my_branch is not '':
                        upd_entry.trg_branch_name = my_branch
                    else:
                        return render_to_response('message.html',{'msg': 'target branch name invalid','return_to':'/manage_ISU_paths/'})  
 
#                    print '-------------'
#                    print 'target ', upd_entry.trg_branch_name
#                    print '-------------' 
                    upd_entry.success = form['success'].data 
                    upd_entry.type_of = form['type_of'].data 
                    if len(upd_entry.type_of) == 0:
                        return render_to_response('message.html',{'msg': 'ISU or RU must be selected','return_to':'/insert_ISU_path_form/'})  
                    upd_entry.otherInfo = form['otherInfo'].data

                    ltitle = 'form-'+str(lcounter)+'-result_file'
                    if ltitle in request.FILES.keys():
                        print 'found title: %s' % str(form['result_file'].data) 
                        title = request.FILES[ltitle]
                        #old entry if exists should be removed django does not do it automatically...
                        darg_name = ISU_working_path.objects.filter(pk=my_id).values('result_file')
                        for x in darg_name:
                            arg_name = x['result_file']
                            print 'old fname is: ', str(arg_name)
                            if arg_name is not '':
                                cmd = "rm my_media/documents/"+str(os.path.basename(str(arg_name)))+""
#                                print 'cmd is ', cmd 
                                p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                        #and now get to save new 
                        upd_entry.result_file = request.FILES[ltitle]
                    else:
                        dfile = 'form-'+str(lcounter)+'-delete_file'
                        print 'possibly deleting a file --'
                        if dfile in request.POST.keys():
                            print 'key found'
                            darg_name= ISU_working_path.objects.filter(pk=my_id).values('result_file')
                            for x in darg_name:
                                arg_name = x['result_file']
#                                print 'fname is: ', str(arg_name)
                            cmd = "rm my_media/documents/"+str(os.path.basename(str(arg_name)))+""
#                            print 'cmd is ', cmd 
                            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                            upd_entry.result_file=''
                        else:
                            print 'key not found'
                            darg_name= ISU_working_path.objects.filter(pk=my_id).values('result_file')
                            for x in darg_name:
                                arg_name = x['result_file']
#                                print 'fname is: ', str(arg_name)
                            upd_entry.result_file=arg_name
                    upd_entry.save()
                    lcounter += 1
                uentries = request.POST.get('entries_len')
                err_msg = 'updated ' + str(lcounter) + ' entries'
                print  err_msg
                return render_to_response('message_resp.html',{'msg': err_msg, 'return_to':'/manage_ISU_paths/'})  
            else:
                print 'some error occured'
        else:
            print 'select entries to update or delete '
            print 'before loop 1'
            cp = request.POST.copy()
            qset = Q()
            for entry in cp.items():
                local_id=retrieve_form_id(entry[0])
                tmp_str = 'form-'+str(local_id)+'-id' 
                if '-delete' in entry[0]:
                    delete_box+=1
                    for e in cp.items():
                        if tmp_str in e[0]:
                            qset |= Q(id=e[1])
                            break
                elif '-update' in entry[0]:
                    update_box+=1
                    for e in cp.items():
                        if tmp_str in e[0]:
                            qset |= Q(id=e[1])
                            break
            print('updates are ', update_box)
            print('deletes are ', delete_box)
            if ((update_box > 0) and (delete_box > 0)):
                return render_to_response('message_resp.html',{'msg':'group actions can be of only one type: update or delete not both','return_to':'/manage_ISU_paths/'})
            if (update_box > 0) :
                d['action'] = 'update'
                d['entries_len'] = update_box
            elif (delete_box > 0):
                d['action'] = 'delete'
                d['entries_len'] = delete_box
            else:
                return render_to_response('message_resp.html',{'msg':'no single or group actions selected: update or delete Please try again','return_to':'/manage_ISU_paths/'})
            print("updates are ", update_box)
            print("deletes are ", delete_box)
            ISUformsetresp= modelformset_factory(ISU_working_path, extra=0, form=ISUresp)
            formset = ISUformsetresp(queryset=ISU_working_path.objects.filter(qset))
            d['entries']=formset
            d['response']='response'
            return render_to_response('manage_ISU_paths.html',  d)
    else:
        ISUFeatureFormset = modelformset_factory(ISU_working_path, extra=0, form=ISUFeature)
        formset = ISUFeatureFormset(queryset=ISU_working_path.objects.all().order_by('-test_date','-tester'))
        lcounter=0  
        alink = []
        print '----1---'
        for x in formset.get_queryset():
            if x.result_file:
                doc_path=os.path.abspath(os.path.join('..', x.result_file.url))
            else:
                doc_path=''#os.path.abspath(os.path.join('..', "/templates/no_file_associated.html"))
            alink.append(doc_path)
            print '   ' , doc_path
        bform = [] 
        for form in formset:
            bform.append(form)
        entries=zip(alink, bform)
        d['initial']='initial'
        d['entries']=entries
        print '----2---'
        return render_to_response('manage_ISU_paths.html',  d)

def insert_ISU_path_form(request):
    d = {}
    d.update(csrf(request))
    print 'in insert ISU'
    if request.method == 'POST':
         src_iso = request.POST.get('src_iso','')
         if not validate_iso(src_iso):
             return render_to_response('message.html',{'msg': 'src iso should contain a .iso','return_to':'/insert_ISU_path_form/'})  
         tbranch = request.POST.get('src_branch','')
         print 'tbranch 1:', tbranch
         if len(tbranch) != 0: 
             src_branch_name=Branch.objects.get(pk=int(tbranch))
         else:
             return render_to_response('message.html',{'msg': 'src branch name invalid','return_to':'/insert_ISU_path_form/'})  
         print 'src ', src_branch_name
         src_build = request.POST.get('src_build_name','')
#         if len(src_build) == 0 or not is_number(src_build):
#             return render_to_response('message.html',{'msg': 'src build field must be a valid number','return_to':'/insert_ISU_path_form/'})  
         trg_iso = request.POST.get('trg_iso','')
         if not validate_iso(trg_iso):
             return render_to_response('message.html',{'msg': 'trg iso should contain a .iso','return_to':'/insert_ISU_path_form/'})  
         tbranch = request.POST.get('trg_branch','')
         print 'tbranch 2:', tbranch
         if len(tbranch) != 0: 
             trg_branch_name = Branch.objects.get(pk=int(tbranch))
         else:
             return render_to_response('message.html',{'msg': 'trg branch name invalid','return_to':'/insert_ISU_path_form/'})  
         trg_branch_name = Branch.objects.get(pk=int(tbranch))
         print 'trg ', trg_branch_name
         trg_build = request.POST.get('trg_build_name','')
 #        if len(trg_build) == 0 or not is_number(trg_build):
 #            return render_to_response('message.html',{'msg': 'trg build field must be a valid number','return_to':'/insert_ISU_path_form/'})  
         tester = request.POST.get('tester','')
         test_date = request.POST.get('date','')
         if len(test_date) == 0:
             return render_to_response('message.html',{'msg': 'a test date should be entered','return_to':'/insert_ISU_path_form/'})  
         print 'src and trg are : %s %s date is: %s' % (src_branch_name, trg_branch_name, test_date)
         try:
             date_obj = datetime.strptime(test_date, '%d-%m-%Y %H:%M')
         except ValueError:
             date_obj = datetime.strptime('01-01-1970 00:00', '%d-%m-%Y %H:%M')
         print 'date is', date_obj
         test_success = request.POST.get('success','') 
         test_type = request.POST.get('type_of','') 
         test_info = request.POST.get('otherInfo','') 
         if len(test_type) == 0:
             return render_to_response('message.html',{'msg': 'ISU or RU must be selected','return_to':'/insert_ISU_path_form/'})  
         if 'result_file' in request.FILES.keys():
            arg_title = request.FILES['result_file']#arg_title is an UploadedFile object,thus has some useful methods...
            print 'File to upload is:------------>',arg_title.name
            new_ISU_path_entry = ISU_working_path(src_iso=src_iso,src_branch_name=src_branch_name,src_build_name=src_build,trg_iso=trg_iso,trg_branch_name=trg_branch_name,trg_build_name=trg_build,tester=tester,test_date=date_obj, result_file=arg_title,success=test_success, type_of=test_type, otherInfo=test_info)
         else:
            new_ISU_path_entry = ISU_working_path(src_iso=src_iso,src_branch_name=src_branch_name,src_build_name=src_build,trg_iso=trg_iso,trg_branch_name=trg_branch_name,trg_build_name=trg_build,tester=tester,test_date=date_obj, success=test_success, type_of=test_type, otherInfo=test_info)
         new_ISU_path_entry.save()
         err_msg = "inserted 1 entry"
         return render_to_response('message_resp.html',{'msg': err_msg, 'return_to':'/manage_ISU_paths/'})  
    else:  
         form = ISU_path_insert_form()
    return render_to_response('insert_ISU_path_form.html',{'form':form}, context_instance=RequestContext(request))




def fetch_row(request):

    my_lvn = request.GET.get('lvn')
    my_branch = request.GET.get('bname')
  
    result = Wiki_entry.objects.filter(bfr_lvn__endswith='_'+my_lvn,branch_name=my_branch)
    if result:
        revision=result[0].rev_id
        return render_to_response('fetched_lvn_row.html',{'res':result,'rev':revision})

    else:
        error='No match for LVN in database'
        return render_to_response('message.html',{'msg':error,'return_to':'/manage_wiki_entries/'})



    
def show_build_info(request):

    pattern = re.compile(r'(\w+)(?=:(\d{5,6}))')
    my_rev = request.GET.get('revision')
    if is_number(my_rev):
        res = Lvn_entry.objects.filter(rev_id=my_rev)
        if res:
            return render_to_response('build_information.html',{'res':res})

        else:
            try:
                f = open(settings.MEDIA_ROOT+'svnhistory/'+my_rev+'.txt','r') 
            
            except IOError as e:
                print e
                error = 'Revision does not match any subversion id'
                return render_to_response('message.html',{'msg':error,'return_to':'/search-lvn/'})
            else:
                green_tag = [pattern.search(line).group(2) for line in f if pattern.search(line) ]
                res = Lvn_entry.objects.filter(rev_id=green_tag[0])
                f.close()

        return render_to_response('build_information.html',{'res':res,'my_rev':my_rev})


    else:

        error = 'Not a valid revision'
        return render_to_response('message.html',{'msg':error,'return_to':'/search-lvn/'})





def prefilled_insert_wiki_form(request,branch_name,bfr_lvn,author,revision):

    
    d = {}
    d.update(csrf(request))
    form = Wiki_insert_form()
    d['form']= form
    d['branch'] = branch_name
    d['bfr_lvn']= bfr_lvn
    d['author']=author
    d['revision']=revision
    return render_to_response('insert_prefilled_form.html', d)



def fetch_range(request):

    start_rev = request.GET.get('start_revision')
    end_rev   = request.GET.get('end_revision')
    my_branch = request.GET.get('bname')
    if not is_number(start_rev) and not is_number(end_rev) or start_rev > end_rev:
        error='starting revision must be smaller than the ending one'
        return render_to_response('message.html',{'msg':error})

    else:
        result = Wiki_entry.objects.filter(rev_id__range=[start_rev,end_rev],branch_name=my_branch).order_by('rev_id')
        if result:
            return render_to_response('fetched_lvn_range.html',{'res':result})
        else:
            return render_to_response('message.html',{'msg':'No results in the db'})

def insert_KBEntry_form(request):
    d = {}
    d.update(csrf(request))
    print 'in insert KBentry'
    if request.method == 'POST':
        category = request.POST.get('category','')
        if len(category) == 0:
            return render_to_response('message.html',{'msg': 'category should not be empty','return_to':'/insert_KBEntry_form/'})  
        brief_desc = request.POST.get('brief_desc','')
        if len(brief_desc) == 0:
            return render_to_response('message.html',{'msg': 'brief description should not be empty','return_to':'/insert_KBEntry_form/'})  
        det_desc = request.POST.get('det_desc','-')
#        if 'result_file' in request.FILES.keys():
#            arg_title = request.FILES['result_file']
#            print 'File to upload is:------------>', arg_title.name
#            new_KBEntry = KBEntry(category = category, brief_desc = brief_desc, det_desc = det_desc , result_file=arg_title)
#        else:
#            new_KBEntry = KBEntry(category = category, brief_desc = brief_desc, det_desc = det_desc)
        print brief_desc, '--', category, '--', det_desc
        new_KBEntry = KBEntry(category=category, brief_desc=brief_desc, det_desc=det_desc)
        new_KBEntry.save()
        err_msg = "inserted 1 entry"
        return render_to_response('message_resp.html',{'msg': err_msg, 'return_to':'/manage_KBEntries/'})  
    else:  
        form = KBEntry_insert_form()
    return render_to_response('insert_KBEntry_form.html',{'form':form}, context_instance=RequestContext(request))

def kbentry_table(request):
    d = {}
    d.update(csrf(request))
    delete_box = 0
    update_box = 0
    print 'in kbentry_table'
    if request.method == 'POST':
        resp = request.POST.get('action')
        print 'resp is: ',  resp
        if resp:
            print 'entries to insert or update'
            if (resp == 'delete'):
                KBFormset= modelformset_factory(KBEntry, extra=0, form=KBEntryDisp)
                formset = KBFormset(request.POST)
                lcounter=0 
                for form in formset:
                    my_id = form['id'].data
                    print 'myid: ', my_id  
                    upd_entry = KBEntry(pk=my_id)
                    darg_name = KBEntry.objects.filter(pk=my_id).values('result_file')
                    for x in darg_name:
                        arg_name = x['result_file']
                        if arg_name is not '':
                            cmd = "rm my_media/kbentries/"+str(os.path.basename(str(arg_name)))+""
                            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    upd_entry.delete()
                    lcounter += 1
                uentries = request.POST.get('entries_len')
                err_msg = 'deleted ' + str(lcounter) + ' entries'
                return render_to_response('message_resp.html',{'msg': err_msg, 'return_to':'/manage_KBEntries/'})  
            elif (resp == 'update'):
                KBFormset= modelformset_factory(KBEntry, extra=0, form=KBEntryResp)
                formset = KBFormset(request.POST, request.FILES)
                lcounter=0
                for form in formset:
#                    print '-------------------------at here'
                    my_id = form['id'].data
                    print 'id is ' , my_id
                    upd_entry = KBEntry(pk=my_id)

                    upd_entry.brief_desc = form['brief_desc'].data  
                    upd_entry.det_desc   = form['det_desc'].data
                    print 'update ', upd_entry.brief_desc, upd_entry.det_desc  
                    if len(upd_entry.brief_desc) == 0: 
                        return render_to_response('message.html',{'msg': 'brief desc must be non empty','return_to':'/manage_KBEntries/'})  
                    upd_entry.category = form['category'].data 
                    if len(upd_entry.category) == 0:
                        return render_to_response('message.html',{'msg': 'some non-empty category must be selected','return_to':'/manage_KB_Entries/'})  
                    ltitle = 'form-'+str(lcounter)+'-result_file'
 
                    if ltitle in request.FILES.keys():
                        print 'found title: %s' % str(form['result_file'].data) 
                        title = request.FILES[ltitle]
                        #old entry if exists should be removed django does not do it automatically...
                        darg_name = KBEntry.objects.filter(pk=my_id).values('result_file')
                        for x in darg_name:
                            arg_name = x['result_file']
                            print 'old fname is: ', str(arg_name)
                            if arg_name is not '':
                                cmd = "rm my_media/kbentries/"+str(os.path.basename(str(arg_name)))+""
#                                print 'cmd is ', cmd 
                                p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                        #and now get to save new 
                        upd_entry.result_file = request.FILES[ltitle]
                    else:
                        dfile = 'form-'+str(lcounter)+'-delete_file'
                        print 'possibly deleting a file --'
                        if dfile in request.POST.keys():
                            print 'key found'
                            darg_name= KBEntry.objects.filter(pk=my_id).values('result_file')
                            for x in darg_name:
                                arg_name = x['result_file']
#                                print 'fname is: ', str(arg_name)
                            cmd = "rm my_media/kbentries/"+str(os.path.basename(str(arg_name)))+""
#                            print 'cmd is ', cmd 
                            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                            upd_entry.result_file=''
                        else:
                            print 'key not found'
                            darg_name= KBEntry.objects.filter(pk=my_id).values('result_file')
                            for x in darg_name:
                                arg_name = x['result_file']
#                                print 'fname is: ', str(arg_name)
                            upd_entry.result_file=arg_name
                    upd_entry.save()
                    lcounter += 1
                uentries = request.POST.get('entries_len')
                err_msg = 'updated ' + str(lcounter) + ' entries'
                print  err_msg
                return render_to_response('message_resp.html',{'msg': err_msg, 'return_to':'/manage_KBEntries/'})  
            else:
                print 'some error occured'
        else:
            print 'select entries to update or delete '
            print 'before loop 1'
            cp = request.POST.copy()
            qset = Q()
            for entry in cp.items():
                local_id=retrieve_form_id(entry[0])
                tmp_str = 'form-'+str(local_id)+'-id' 
                if '-delete' in entry[0]:
                    delete_box+=1
                    for e in cp.items():
                        if tmp_str in e[0]:
                            qset |= Q(id=e[1])
                            break
                elif '-update' in entry[0]:
                    update_box+=1
                    for e in cp.items():
                        if tmp_str in e[0]:
                            qset |= Q(id=e[1])
                            break
            print('updates are ', update_box)
            print('deletes are ', delete_box)
            if ((update_box > 0) and (delete_box > 0)):
                return render_to_response('message_resp.html',{'msg':'group actions can be of only one type: update or delete not both','return_to':'/manage_KBEntries/'})
            if (update_box > 0) :
                d['action'] = 'update'
                d['entries_len'] = update_box
                print("updates are ", update_box)
            elif (delete_box > 0):
                d['action'] = 'delete'
                d['entries_len'] = delete_box
                print("deletes are ", delete_box)
            else:
                return render_to_response('message_resp.html',{'msg':'no single or group actions selected: update or delete Please try again','return_to':'/manage_KBEntries/'})
            KBformsetresp= modelformset_factory(KBEntry, extra=0, form=KBEntryResp)
            formset = KBformsetresp(queryset=KBEntry.objects.filter(qset))
#            print 'at here -------' 
#            for form in formset:
#                print form.as_table()
            d['entries']=formset
            d['response']='response'
            return render_to_response('manage_KBEntries.html',  d)
    else:
        print 'get action at kbentry table ----' 
        KBEntryDispFormset = modelformset_factory(KBEntry, extra=0, form=KBEntryDisp)
        formset = KBEntryDispFormset(queryset=KBEntry.objects.all())
#        for form in formset:
#            print form.as_table()
        lcounter=0  
        alink = []
        print '----1---'
        for x in formset.get_queryset():
            if x.result_file:
                doc_path=os.path.abspath(os.path.join('..', x.result_file.url))
            else:
                doc_path=''#os.path.abspath(os.path.join('..', "/templates/no_file_associated.html"))
            alink.append(doc_path)
            print '   ' , doc_path
        bform = [] 
        for form in formset:
            bform.append(form)
        entries=zip(alink, bform)
        print '---- entries ----'
        print entries
        print '-----------------'
        d['initial']='initial'
        d['entries']=entries
        for entry in entries:
            print '----2---', entry[0], entry[1]
        return render_to_response('manage_KBEntries.html', d)


def do_svndiff(request):

    my_rev = request.GET.get('revision')
    my_rev = my_rev.strip('r')
    print 'revision is:',my_rev
    pattern = re.compile(r'/(\w+)(?=:(\d{5,6}))')
    URL = 'svn+ssh://ngman@svne1.access.nokiasiemensnetworks.com/isource/svnroot/flexi_bng/'
    #:find the delivery from revision :#

    if is_number(my_rev):
        res = Lvn_entry.objects.filter(rev_id=my_rev)
        if res:
        #: if the revision exists in the database and is not from green tags :#
            branch_in_question = res[0].branch_name
            if os.path.exists(settings.MEDIA_ROOT+'/deliveries/diff_for_'+my_rev+'.txt'):
                #: show the diff immediately.no need to look again in svn :#
                return render_to_response('diff_info.html',{'my_rev':my_rev})

            else:
                #: look at svn if this revision is never searched before :#
               # cmd = "cd my_media/deliveries/"+str(branch_in_question)+" && svn diff -c "+my_rev
                cmd = "svn diff -c "+my_rev + " " +URL
                print cmd
                p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                stdOut = p.communicate()[0]
                f = open(settings.MEDIA_ROOT+'/deliveries/diff_for_'+my_rev+'.txt','w')
                f.write(stdOut)
                f.close()
                return render_to_response('diff_info.html',{'my_rev':my_rev})

         #: if the revision is not written in the db (it is an ngman's commit for green tags) :#
        else:
            try:
                f = open(settings.MEDIA_ROOT+'svnhistory/'+my_rev+'.txt','r') 
            
            except IOError as e:
                print e
                error = 'Revision does not match any subversion id yet'
                return render_to_response('message.html',{'msg':error,'return_to':'/search-lvn/'})
            else:
                branch_name = [pattern.search(line).group(1) for line in f if pattern.search(line) ]          
                f.close()
                print 'here',str(branch_name).strip('],[,"')
                error = 'Nothing to diff for... add/rm green tag by ngman or under tags/ ,'+str(branch_name)
                return render_to_response('message.html',{'msg':error,'return_to':'/search-lvn/'})


    else:

        error = 'Not a valid revision'
        return render_to_response('message.html',{'msg':error,'return_to':'/search-lvn/'})
   
    
def manage_build_entries(request):
    print 'at build entries' 
    d = {}
#    d.update(csrf(request))
    if request.method == 'POST':
       print 'POST request received' 
    else:
        branch = request.GET.get('branch_name', 'tmp')
 #       print 'my branch is: %s ' % (branch)

        buildsFormset= modelformset_factory(Build_entry, extra=0, exclude=('branch_name'), form=Buildentry)
        formset = buildsFormset(queryset=Build_entry.objects.filter(branch_name=branch).order_by('-rev', '-build'))
        count = 0
        for e in formset:
            count += 1

        if count > 0:
           print 'found ', count 
           d['initial']='initial'
           d['branch'] = branch
           d["formset"]=formset
           return render_to_response('manage_build_entries.html',  d)
        else:
           return render_to_response('message.html',{'msg': 'no entries exist for this branch','return_to':'/buildstable/'})  

    
