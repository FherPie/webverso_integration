from odoo import models
from odoo.exceptions import UserError
import base64


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def webverso_download_pdf(self):
        self.ensure_one()

        report = self.env.ref("sale.action_report_saleorder")

        try:
            pdf, _ = report._render_qweb_pdf(report_ref=report.report_name, res_ids=self.ids)

            return {
                "success": True,
                "filename": f"{self.name}.pdf",
                "content": base64.b64encode(pdf).decode(),
                "mimeType": "application/pdf"
            }

        except Exception as e:
            message = str(e)

            if "Wkhtmltopdf" in message:
                raise UserError(
                    "El servidor Odoo no tiene instalado wkhtmltopdf. No es posible generar PDFs."
                )

            raise UserError(
                f"Error generando el PDF de la cotización SIIII {self.name}: {message}"
            )