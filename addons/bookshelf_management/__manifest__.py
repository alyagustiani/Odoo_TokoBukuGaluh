{
    'name': 'Bookshelf Management',
    'version': '1.0.0',
    'category': 'Inventory',
    'summary': 'Manajemen Rak Buku untuk Toko Buku',
    'description': """
        Module untuk mengelola rak buku di toko buku.
        Fitur:
        - Tambah/edit rak buku
        - Pencarian berdasarkan nama rak
        - Kategori rak buku
    """,
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'depends': ['base', 'stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/bookshelf_data.xml',
        'views/bookshelf_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}