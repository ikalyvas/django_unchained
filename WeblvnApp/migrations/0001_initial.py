# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DBUpdate'
        db.create_table('WeblvnApp_dbupdate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lastUpdDate', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('WeblvnApp', ['DBUpdate'])

        # Adding model 'Branch'
        db.create_table('WeblvnApp_branch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('bfr_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('WeblvnApp', ['Branch'])

        # Adding model 'Lvn_entry'
        db.create_table('WeblvnApp_lvn_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lvn', self.gf('django.db.models.fields.IntegerField')()),
            ('branch_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['WeblvnApp.Branch'], to_field='branch_name')),
            ('rev_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('src_dir_change', self.gf('django.db.models.fields.IntegerField')()),
            ('h_file_change', self.gf('django.db.models.fields.IntegerField')()),
            ('inc_file_change', self.gf('django.db.models.fields.IntegerField')()),
            ('layout_check', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('layout_done', self.gf('django.db.models.fields.IntegerField')()),
            ('layout_status', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('md5sum_str', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('commit_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('layout_rev', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('WeblvnApp', ['Lvn_entry'])


    def backwards(self, orm):
        
        # Deleting model 'DBUpdate'
        db.delete_table('WeblvnApp_dbupdate')

        # Deleting model 'Branch'
        db.delete_table('WeblvnApp_branch')

        # Deleting model 'Lvn_entry'
        db.delete_table('WeblvnApp_lvn_entry')


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
        }
    }

    complete_apps = ['WeblvnApp']
