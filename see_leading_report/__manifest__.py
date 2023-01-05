{
    "name": "see landing Reports",
    "version": "1.1",
    "category": "Generic Modules/sale",
    "description": """ Manage sales module

    """,
    "author": "See landing",
    "website": "",
    "depends":['sale_custom','l10n_sa_invoice'],
    "data": [

        'reports/report.xml',
        'reports/jornal_entry.xml',
        'reports/sale_order_report_inhrit.xml',
        'reports/delivery_stock_arabic.xml',
        'reports/delivery_stock_english_arabic.xml',
        'reports/invoice_sale_arabic.xml',
        'reports/invoice_sale_arabic_english.xml',
        'reports/invoice_tax_layout.xml',
        'reports/invoice_delivery.xml',
        
        

    
    ],
    "installable": True,
    "active": True,
    'license': 'LGPL-3',
}

