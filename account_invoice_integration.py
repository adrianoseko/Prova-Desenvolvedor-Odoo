# account_invoice_integration/models/account_invoice_integration.py

from odoo import models, fields
import requests


class AccountInvoiceIntegration(models.Model):
    _name = 'account.invoice.integration'
    _description = 'Invoice Integration with External System'

    invoice_id = fields.Many2one(
        'account.move', string='Invoice', required=True)
    external_system_id = fields.Char(string='External Invoice ID')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('error', 'Error')
    ], string='Integration Status', default='pending')
    response_message = fields.Text(string='Response Message')

# account_invoice_integration/models/account_move.py


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        # Chama o método original para postar a fatura
        super(AccountMove, self).action_post()

        # Verifica se a fatura é uma fatura de venda (pode ser adaptado para outros tipos)
        if self.type == 'out_invoice':
            integration_record = self.env['account.invoice.integration'].create({
                'invoice_id': self.id,
                'external_system_id': '',  # Defina o ID da fatura no sistema externo aqui
            })

            # Chame uma função que envia os dados da fatura para o sistema externo via API REST
            # e recebe a resposta
            response = self.send_invoice_to_external_system(
                self, integration_record.external_system_id)

            # Atualiza o registro de integração com base na resposta do sistema externo
            if response['status'] == 'success':
                integration_record.write({
                    'status': 'success',
                    'response_message': response['message']
                })
            else:
                integration_record.write({
                    'status': 'error',
                    'response_message': response['message']
                })

    def send_invoice_to_external_system(self, invoice, external_id):

        # URL do sistema externo onde você deseja enviar a fatura
        url = 'https://exemplo.com/api/endpoint'

        # Dados da fatura que você deseja enviar (substitua pelos dados reais)
        dados_fatura = {
            'numero': '12345',
            'cliente': 'Nome do Cliente',
            'valor': 100.00,
            # Outros campos da fatura
        }

        # Enviar a fatura como um JSON na solicitação POST
        response = requests.post(url, json=dados_fatura)

        # Verificar a resposta do sistema externo
        if response.status_code == 200:
            print('Fatura integrada com sucesso!')
            resposta_json = response.json()
            return resposta_json
        else:
            print('Erro na integração da fatura!')
            print(f'Código de Status: {response.status_code}')
            print(f'Resposta do Sistema Externo: {response.text}')
