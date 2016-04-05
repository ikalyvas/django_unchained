# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ISU_working_path'
        db.create_table('WeblvnApp_isu_working_path', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('src_iso', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('src_build_name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('src_branch_name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='src_branch_name', to_field='branch_name', to=orm['WeblvnApp.Branch'])),
            ('trg_iso', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('trg_build_name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('trg_branch_name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trg_branch_name', to_field='branch_name', to=orm['WeblvnApp.Branch'])),
            ('tester', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('test_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('success', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('result_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('WeblvnApp', ['ISU_working_path'])


    def backwards(self, orm):
        
        # Deleting model 'ISU_working_path'
        db.delete_table('WeblvnApp_isu_working_path')


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
        'WeblvnApp.isu_working_path': {
            'Meta': {'object_name': 'ISU_working_path'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'src_branch_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'src_branch_name'", 'to_field': "'branch_name'", 'to': "orm['WeblvnApp.Branch']"}),
            'src_build_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'src_iso': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'success': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'test_date': ('django.db.models.fields.DateTimeField', [], {}),
            'tester': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trg_branch_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trg_branch_name'", 'to_field': "'branch_name'", 'to': "orm['WeblvnApp.Branch']"}),
            'trg_build_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'trg_iso': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'adaptation': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'bfr_lvn': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'branch_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['WeblvnApp.Branch']", 'to_field': "'branch_name'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'rev_id': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['WeblvnApp']
