# action_feedback
from odoo import _, api, fields, models
from odoo.tools.misc import clean_context


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    def aaction_done(self):
        res = super(MailActivity, self).aaction_done()
        case = ['PO Received','Contract Signed','Contract Signed / PO Received','11. Contract Signed / PO Received','11.Contract Signed / PO Received']
        if any(self.activity_type_id.name in n for n in case) and self.res_model == 'crm.lead':
            crm_id = self.env["crm.lead"].search([("id", "=",self.res_id)])
            crm_id.probability += self.activity_type_id.progress
            crm_id.is_po_receive = True
        return res

    def action_close_dialog(self):
        res = super(MailActivity, self).action_close_dialog()
        case = ['PO Received','Contract Signed','Contract Signed / PO Received','11. Contract Signed / PO Received','11.Contract Signed / PO Received']
        if any(self.activity_type_id.name in n for n in case) and self.res_model == 'crm.lead':
            crm_id = self.env["crm.lead"].search([("id", "=",self.res_id)])
            crm_id.is_po_receive = True
        return res
    
    def action_feedback(self, feedback=False, attachment_ids=None):
        if self.res_model == 'crm.lead':
            crm_id = self.env[self.res_model].browse(self.res_id)
            progress = self.activity_type_id.progress * 100
            crm_id.probability += progress
        res = super().action_feedback(feedback=False, attachment_ids=None)
        return res
        