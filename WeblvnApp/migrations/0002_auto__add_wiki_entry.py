# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Wiki_entry'
        db.create_table('WeblvnApp_wiki_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bfr_lvn', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('branch_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['WeblvnApp.Branch'], to_field='branch_name')),
            ('rev_id', self.gf('django.db.models.fields.IntegerField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('adaptation', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('other', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('WeblvnApp', ['Wiki_entry'])


    def backwards(self, orm):
        
        # Deleting model 'Wiki_entry'
        db.delete_table('WeblvnApp_wiki_entry')


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
        'WeblvnApp.wiki_entry': {
            'Meta': {'object_name': 'Wiki_entry'},
            'adaptation': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'bfr_lvn': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'branch_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['WeblvnApp.Branch']", 'to_field': "'branch_name'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'rev_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['WeblvnApp']
