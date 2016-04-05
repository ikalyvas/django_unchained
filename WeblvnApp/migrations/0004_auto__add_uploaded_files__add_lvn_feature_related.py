# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Uploaded_Files'
        db.create_table('WeblvnApp_uploaded_files', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('rev_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('WeblvnApp', ['Uploaded_Files'])

        # Adding model 'LVN_Feature_Related'
        db.create_table('WeblvnApp_lvn_feature_related', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rev_id', self.gf('django.db.models.fields.IntegerField')()),
            ('lvn', self.gf('django.db.models.fields.IntegerField')()),
            ('feature', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('team', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('affected_structures', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('other', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('title', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
        ))
        db.send_create_signal('WeblvnApp', ['LVN_Feature_Related'])


    def backwards(self, orm):
        
        # Deleting model 'Uploaded_Files'
        db.delete_table('WeblvnApp_uploaded_files')

        # Deleting model 'LVN_Feature_Related'
        db.delete_table('WeblvnApp_lvn_feature_related')


    models = {
        'WeblvnApp.branch': {
            'Meta': {'ordering': "['branch_name']", 'object_name': 'Branch'},
            'bfr_id': ('django.db.models.fields.IntegerField', [], {}),
            'branch_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'WeblvnApp.dbupdate': {
            'Meta': {'object_name': 'DBUpdate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastUpdDate': ('django.db.models.fields.DateTimeField', [], {})
        },
        'WeblvnApp.lvn_entry': {
            'Meta': {'object_name': 'Lvn_entry'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'branch_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['WeblvnApp.Branch']", 'to_field': "'branch_name'"}),
            'commit_date': ('django.db.models.fields.DateTimeField', [], {}),
            'h_file_change': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inc_file_change': ('django.db.models.fields.IntegerField', [], {}),
            'layout_check': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'layout_done': ('django.db.models.fields.IntegerField', [], {}),
            'layout_rev': ('django.db.models.fields.IntegerField', [], {}),
            'layout_status': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'lvn': ('django.db.models.fields.IntegerField', [], {}),
            'md5sum_str': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'rev_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'src_dir_change': ('django.db.models.fields.IntegerField', [], {})
        },
        'WeblvnApp.lvn_feature_related': {
            'Meta': {'object_name': 'LVN_Feature_Related'},
            'affected_structures': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lvn': ('django.db.models.fields.IntegerField', [], {}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'rev_id': ('django.db.models.fields.IntegerField', [], {}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'title': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'})
        },
        'WeblvnApp.uploaded_files': {
            'Meta': {'object_name': 'Uploaded_Files'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rev_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'WeblvnApp.wiki_entry': {
            'Meta': {'object_name': 'Wiki_entry'},
            'adaptation': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '500', 'null': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'bfr_lvn': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'branch_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['WeblvnApp.Branch']", 'to_field': "'branch_name'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '500', 'null': 'True'}),
            'rev_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['WeblvnApp']
