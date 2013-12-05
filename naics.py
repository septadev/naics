# -*- coding: utf-8 -*-
##############################################################################
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time

#class tax_id_number(osv.osv):
	#""" Tax Identification Number """
	#_name = "tax.id.number"
    #_description = "Tax Identification Number"
    #_auto = True
    #_order = 'id asc'
    #_log_access = False
    #_columns = {
		#'name':fields.char('Tax ID Number', size=30,  translate=False,  required=True,  readonly=False, help="Tax Identification Number or VAT"),
		#'country_id':fields.many2one('res.country', 'Country'),
		#'regex':fields.text('Regular Expression Validator', required=False,  readonly=False, help="Python Regular Expression for validating tax ID"),
		#'fixme':fields.boolean('Incorrect Format', readonly=True, help="If TRUE this tax ID must be corrected by user."),
	#}
	
    
    
class naics_code(osv.osv):
    """  NAICS Code """
    _name = "naics.code"
    _description = "NAICS Code"
    _auto = False
    _table = "naics_structure"
    _order = 'id asc'
    _log_access = True
    _columns = {
        'code': fields.char('NAICS Code', size=255,  translate=False,  required=False,  readonly=True),
        'title':fields.char('NAICS Title', size=255,  translate=True,  required=False, readonly=True), 
        'id':fields.integer('NAICS Id',  required=True, readonly=True), 
        'sequence':fields.integer('Sequence',  required=False, readonly=True),
        'write_date':fields.date('Last Changed',   required=False, readonly=True), 
        'write_uid':fields.many2one('res.users',  'Last Change User'), 
        'create_date':fields.date('Created',   required=False, readonly=True), 
        'create_uid':fields.many2one('res.users',  'Owner')
    }

class commodity_category(osv.osv):
    """ SEPTA Commodity Code Categories """
    _name = "commodity.category"
    _description = "Commodity Code Categories"
    _auto = False
    _table = "commodity_category"
    _order = 'category_parent_prefix asc'
    _log_access = True
    _columns = {
        'id':fields.integer('Commodity Category Id',  required=True, readonly=True),
        'category_parent_prefix':fields.char('Prefix', size=1),
        'category_parent_name':fields.char('Category', size=128),
        'category_child_prefix':fields.char('Code', size=3),
        'category_child_name':fields.char('Subcategory', size=128),
        'write_date':fields.date('Last Changed',   required=False, readonly=True), 
        'write_uid':fields.many2one('res.users',  'Last Change User'), 
        'create_date':fields.date('Created',   required=False, readonly=True), 
        'create_uid':fields.many2one('res.users',  'Owner')   
    }  

    def name_get(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		if isinstance(ids, (int, long)):
			ids = [ids]
			
		res = []
		for record in self.browse(cr, uid, ids, context=context):
			name = record.category_child_prefix
			res.append((record.id, name))
			
		return res
    
class commodity_code(osv.osv):
    """ SEPTA Commodity Code """
    _name = "commodity.code"
    _description = "SEPTA Commodity Code"
    _auto = False
    _table = "commodity_code"
    _order = 'id asc'
    _log_access = True
    _columns = {    
        'code': fields.char('Commodity Code', size=255,  translate=False,  required=True,  readonly=False),
        'title':fields.char('Commodity Title', size=255,  translate=True,  required=True, readonly=False), 
        'id':fields.integer('Commodity Code Id',  required=True, readonly=True), 
        'category_id':fields.many2one('commodity.category', 'Category Id', ondelete='restrict', required=False, readonly=False),
        'category_child_prefix':fields.related('category_id', 'category_child_prefix', string="Prefix", type='char', relation='commodity.category', readonly=False),
        'category_child_name':fields.related('category_id', 'category_child_name', string="Subcategory", type='char', relation='commodity.category', readonly=False),
        'write_date':fields.date('Last Changed',   required=False, readonly=True), 
        'write_uid':fields.many2one('res.users',  'Last Change User', readonly=True), 
        'create_date':fields.date('Created',   required=False, readonly=True), 
        'create_uid':fields.many2one('res.users',  'Owner', readonly=True)
    }   

    def onchange_category_id(self, cr, uid, category_id, context=None):
        """Returns new category child prefix and child name values based on category_id
        @param category_id: The new category id selected by user
        @return dictionary with dictionary of values with key ['value']
        """
        data = {'value': {'category_child_prefix': False, 'category_child_name': False}}
        cat = None
        if category_id:
            cat = self.pool.get('commodity.category').browse(cr, uid, category_id)
            data['value'] = {'category_child_prefix': cat[0].category_child_prefix,
                             'category_child_name': cat[0].category_child_name}

        return data
        
    def name_get(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		if isinstance(ids, (int, long)):
			ids = [ids]
			
		res = []
		for record in self.browse(cr, uid, ids, context=context):
			name = record.category_child_prefix + record.code
			res.append((record.id, name))
			
		return res



#class septa_commodity(osv.osv):
    #""" SEPTA Commodity """
    #_name = "septa.commodity"
    #_description = "SEPTA Commodity"
    #_order = 'id asc'
    #_log_access = True
    #_columns = {    
        #'vendor_id':fields.many2one('dbe.vendor', 'Vendor', ondelete='restrict', required=False, readonly=False),
        #'naics_code_id':fields.many2many('naics.code', 'naics_to_commodity', 'id', 'commodity_id',  'Naics Code Ids', ondelete='restrict', required=True, readonly=False),
        #'naics_code':fields.related('naics_code_id', 'code', string="NAICS Code", type='many2one', relation='naics.code', readonly=True),
        #'naics_title':fields.related('naics_code_id', 'title', string="NAICS Title", type='many2one', relation='naics.code', readonly=True),
        #'commodity_code_id':fields.many2many('commodity.code', 'commodity_code_to_commodity', 'id', 'commodity_id', 'Commodity Code Ids', ondelete='restrict', required=True, readonly=False),
        #'commodity_code':fields.related('commodity_code_id', 'code', string="Commodity Code", type='many2one', relation='commodity.code', readonly=True),
        #'commodity_title':fields.related('commodity_code_id', 'title', string="Commodity Title", type='many2one', relation='commodity.code', readonly=True),
        #'commodity_category_id':fields.related('commodity_code_id', 'category_id', string="Commodity Category", type='many2one', relation='commodity.code', readonly=True),
        #'category_child_prefix':fields.related('commodity_category_id', 'id', string="Commodity Prefix", type='many2one', relation='commodity.category', readonly=True),
        #'active':fields.boolean('Active', required=False),
        #'note':fields.text('Notes'),
        #'write_date':fields.date('Last Changed',   required=False, readonly=True), 
        #'write_uid':fields.many2one('res.users',  'Last Change User', readonly=True), 
        #'create_date':fields.date('Created',   required=False, readonly=True), 
        #'create_uid':fields.many2one('res.users',  'Owner', readonly=True)
    #} 
                             
class commodity_commodity(osv.osv):
    """ SEPTA Commodity """
    _name = "commodity.commodity"
    _description = "SEPTA Commodity"
    _order = 'id asc'
    _log_access = True
    _columns = {    
        'vendor_id':fields.integer('Vendor Id'), 
        'naics_code_id':fields.many2many('naics.code', 'naics_to_commodity', 'id', 'commodity_id',  'Naics Code Ids', ondelete='restrict', required=True, readonly=False),
        'naics_code':fields.related('naics_code_id', 'code', string="NAICS Code", type='many2one', relation='naics.code', readonly=True),
        'naics_title':fields.related('naics_code_id', 'title', string="NAICS Title", type='many2one', relation='naics.code', readonly=True),
        'commodity_code_id':fields.many2many('commodity.code', 'commodity_code_to_commodity', 'id', 'commodity_id', 'Commodity Code Ids', ondelete='restrict', required=True, readonly=False),
        'commodity_code':fields.related('commodity_code_id', 'code', string="Commodity Code", type='many2one', relation='commodity.code', readonly=True),
        'commodity_title':fields.related('commodity_code_id', 'title', string="Commodity Title", type='many2one', relation='commodity.code', readonly=True),
        'commodity_category_id':fields.related('commodity_code_id', 'category_id', string="Commodity Category", type='many2one', relation='commodity.code', readonly=True),
        'category_child_prefix':fields.related('commodity_category_id', 'id', string="Commodity Prefix", type='many2one', relation='commodity.category', readonly=True),
        'active':fields.boolean('Active', required=False),
        'note':fields.text('Notes'),
        'write_date':fields.date('Last Changed',   required=False, readonly=True), 
        'write_uid':fields.many2one('res.users',  'Last Change User', readonly=True), 
        'create_date':fields.date('Created',   required=False, readonly=True), 
        'create_uid':fields.many2one('res.users',  'Owner', readonly=True)
    }   
        
