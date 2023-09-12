from odoo import models, fields, api

# Implementação de currency_id e função de conversão de moeda estrangeira


class AccountMove(models.Model):
    _inherit = 'account.move'

    currency_id = fields.Many2one('res.currency', string='Currency')

    @api.onchange('currency_id', 'amount_total')
    def _onchange_currency_id(self):
        if self.currency_id and self.currency_id != self.company_id.currency_id:
            # Encontrar a taxa de câmbio correspondente
            exchange_rate = self.env['account.foreign.exchange.rate'].search([
                ('currency_from_id', '=', self.currency_id.id),
                ('currency_to_id', '=', self.company_id.currency_id.id),
                ('date', '<=', self.date),
            ], order='date DESC', limit=1)

            if exchange_rate:
                # Converter o valor da moeda estrangeira para a moeda base
                self.amount_total = self.amount_total / exchange_rate.exchange_rate

    @api.model
    def create(self, vals):
        # Chamar o método _onchange_currency_id ao criar um novo lançamento
        move = super(AccountMove, self).create(vals)
        move._onchange_currency_id()
        return move


# Novo modelo para moedas estrangeiras
class AccountForeignExchangeRate(models.Model):
    _name = 'account.foreign.exchange.rate'
    _description = 'Foreign Exchange Rates'

    date = fields.Date(string='Date', required=True)
    currency_from_id = fields.Many2one(
        'res.currency', string='From Currency', required=True)
    currency_to_id = fields.Many2one(
        'res.currency', string='To Currency', required=True)
    exchange_rate = fields.Float(string='Exchange Rate', required=True)
