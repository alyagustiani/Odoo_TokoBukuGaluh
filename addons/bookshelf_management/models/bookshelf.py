from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Bookshelf(models.Model):
    _name = 'bookshelf.bookshelf'
    _description = 'Rak Buku'
    _order = 'name'

    name = fields.Char(
        string='Nama Rak',
        required=True,
        help='Nama atau kode rak buku'
    )
    
    description = fields.Text(
        string='Deskripsi',
        help='Deskripsi detail rak buku'
    )
    
    location = fields.Char(
        string='Lokasi',
        required=True,
        help='Lokasi fisik rak dalam toko'
    )
    
    category_id = fields.Many2one(
        'bookshelf.category',
        string='Kategori Rak',
        help='Kategori atau jenis rak buku'
    )
    
    capacity = fields.Integer(
        string='Kapasitas',
        default=100,
        help='Jumlah maksimal buku yang bisa ditampung'
    )
    
    current_books = fields.Integer(
        string='Jumlah Buku Saat Ini',
        default=0,
        help='Jumlah buku yang sedang ada di rak'
    )
    
    available_space = fields.Integer(
        string='Ruang Tersedia',
        compute='_compute_available_space',
        store=True,
        help='Sisa ruang kosong di rak'
    )
    
    is_full = fields.Boolean(
        string='Rak Penuh',
        compute='_compute_is_full',
        store=True
    )
    
    active = fields.Boolean(
        string='Aktif',
        default=True
    )
    
    color = fields.Integer(
        string='Warna',
        help='Warna untuk tampilan kanban'
    )

    @api.depends('capacity', 'current_books')
    def _compute_available_space(self):
        for record in self:
            record.available_space = record.capacity - record.current_books

    @api.depends('capacity', 'current_books')
    def _compute_is_full(self):
        for record in self:
            record.is_full = record.current_books >= record.capacity

    @api.constrains('current_books', 'capacity')
    def _check_capacity(self):
        for record in self:
            if record.current_books > record.capacity:
                raise ValidationError(
                    f'Jumlah buku ({record.current_books}) tidak boleh melebihi kapasitas rak ({record.capacity})'
                )

    @api.constrains('capacity')
    def _check_positive_capacity(self):
        for record in self:
            if record.capacity <= 0:
                raise ValidationError('Kapasitas rak harus lebih dari 0')

    def name_get(self):
        result = []
        for record in self:
            name = f'{record.name} - {record.location}'
            result.append((record.id, name))
        return result
    
    def action_view_books(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Buku di Rak',
            'res_model': 'product.product',  # atau model buku yang Anda pakai
            'view_mode': 'list,form',
            'domain': [('bookshelf_id', '=', self.id)],  # sesuaikan field
        }

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        
        domain = args[:]
        if name:
            domain += ['|', '|', 
                      ('name', operator, name),
                      ('location', operator, name),
                      ('description', operator, name)]
        
        records = self.search(domain, limit=limit)
        return records.name_get()


class BookshelfCategory(models.Model):
    _name = 'bookshelf.category'
    _description = 'Kategori Rak Buku'
    _order = 'name'

    name = fields.Char(
        string='Nama Kategori',
        required=True
    )
    
    code = fields.Char(
        string='Kode',
        help='Kode singkat kategori'
    )
    
    description = fields.Text(
        string='Deskripsi'
    )
    
    bookshelf_ids = fields.One2many(
        'bookshelf.bookshelf',
        'category_id',
        string='Rak-rak'
    )
    
    bookshelf_count = fields.Integer(
        string='Jumlah Rak',
        compute='_compute_bookshelf_count'
    )

    @api.depends('bookshelf_ids')
    def _compute_bookshelf_count(self):
        for record in self:
            record.bookshelf_count = len(record.bookshelf_ids)

    def action_view_bookshelves(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rak dalam Kategori',
            'res_model': 'bookshelf.bookshelf',
            'view_mode': 'list,form',
            'domain': [('category_id', '=', self.id)],
        }
    
from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    bookshelf_id = fields.Many2one('bookshelf.bookshelf', string='Rak Buku')