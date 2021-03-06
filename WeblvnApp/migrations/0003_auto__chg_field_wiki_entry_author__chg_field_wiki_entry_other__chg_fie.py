# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Wiki_entry.author'
        db.alter_column('WeblvnApp_wiki_entry', 'author', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'Wiki_entry.other'
        db.alter_column('WeblvnApp_wiki_entry', 'other', self.gf('django.db.models.fields.CharField')(max_length=500, null=True))

        # Changing field 'Wiki_entry.adaptation'
        db.alter_column('WeblvnApp_wiki_entry', 'adaptation', self.gf('django.db.models.fields.CharField')(max_length=500, null=True))


    def backwards(self, orm):
        
        # Changing field 'Wiki_entry.author'
        db.alter_column('WeblvnApp_wiki_entry', 'author', self.gf('django.db.models.fields.CharField')(max_length=10))

        # User chose to not deal with backwards NULL issues for 'Wiki_entry.other'
        raise RuntimeError("Cannot reverse this migration. 'Wiki_entry.other' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Wiki_entry.adaptation'
        raise RuntimeError("Cannot reverse this migration. 'Wiki_entry.adaptation' and its values cannot be restored.")


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
