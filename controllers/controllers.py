# -*- coding: utf-8 -*-
# from odoo import http


# class Taxes01(http.Controller):
#     @http.route('/taxes01/taxes01', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/taxes01/taxes01/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('taxes01.listing', {
#             'root': '/taxes01/taxes01',
#             'objects': http.request.env['taxes01.taxes01'].search([]),
#         })

#     @http.route('/taxes01/taxes01/objects/<model("taxes01.taxes01"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('taxes01.object', {
#             'object': obj
#         })

